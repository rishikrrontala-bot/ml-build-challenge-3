"""Export YAMNet's CNN for the browser: batch-norm folded into conv weights, float16.

Writes public/model/yamnet.json (layer list + byte offsets) and public/model/yamnet.bin.
The browser rebuilds the forward pass from these with plain TF.js ops
(src/model/backbone.ts), so no model converter is involved and every layer is
accounted for. Also writes a NumPy forward pass over the *exported* weights and
reports how far float16 + folding moves the outputs from the official model.
"""
from __future__ import annotations

import json

import numpy as np

from common import ESC50, PUBLIC_MODEL, RESULTS, audioset_class_names, load_wav_16k
import yamnet_core as yc

EPS = 1e-4  # params.batchnorm_epsilon


def fold(kernel: np.ndarray, bn: list[np.ndarray], depthwise: bool) -> tuple[np.ndarray, np.ndarray]:
    beta, mean, var = bn  # center=True, scale=False -> gamma == 1
    k = 1.0 / np.sqrt(var + EPS)
    if depthwise:   # [kh, kw, in, 1], per input channel
        w = kernel * k[None, None, :, None]
    else:           # [kh, kw, in, out], per output channel
        w = kernel * k[None, None, None, :]
    return w.astype(np.float32), (beta - mean * k).astype(np.float32)


def collect() -> list[dict]:
    from tf_keras import layers

    core = yc.backbone()
    by_name = {l.name: l for l in core.layers}
    specs = []
    from yamnet import _YAMNET_LAYER_DEFS  # (fn, kernel, stride, filters)

    for i, (fn, _kernel, stride, filters) in enumerate(_YAMNET_LAYER_DEFS, start=1):
        if fn.__name__ == "_conv":
            w, b = fold(by_name[f"layer{i}/conv"].get_weights()[0],
                        by_name[f"layer{i}/conv/bn"].get_weights(), depthwise=False)
            specs.append(dict(kind="conv", stride=stride, w=w, b=b))
        else:
            w, b = fold(by_name[f"layer{i}/depthwise_conv"].get_weights()[0],
                        by_name[f"layer{i}/depthwise_conv/bn"].get_weights(), depthwise=True)
            specs.append(dict(kind="depthwise", stride=stride, w=w, b=b))
            w, b = fold(by_name[f"layer{i}/pointwise_conv"].get_weights()[0],
                        by_name[f"layer{i}/pointwise_conv/bn"].get_weights(), depthwise=False)
            specs.append(dict(kind="conv", stride=1, w=w, b=b))
    dense = [l for l in core.layers if isinstance(l, layers.Dense)][0]
    w, b = dense.get_weights()
    specs.append(dict(kind="dense", stride=1, w=w.astype(np.float32), b=b.astype(np.float32)))
    return specs


def numpy_forward(specs: list[dict], patches: np.ndarray, f16: bool) -> tuple[np.ndarray, np.ndarray]:
    """Reference forward pass with TF 'same' padding, using float32 math."""
    import tensorflow as tf

    x = tf.constant(patches[..., None], tf.float32)
    for s in specs[:-1]:
        w = s["w"].astype(np.float16).astype(np.float32) if f16 else s["w"]
        b = s["b"].astype(np.float16).astype(np.float32) if f16 else s["b"]
        st = [1, s["stride"], s["stride"], 1]
        if s["kind"] == "conv":
            x = tf.nn.conv2d(x, w, st, "SAME")
        else:
            x = tf.nn.depthwise_conv2d(x, w, st, "SAME")
        x = tf.nn.relu(x + b)
    emb = tf.reduce_mean(x, axis=[1, 2])
    d = specs[-1]
    w = d["w"].astype(np.float16).astype(np.float32) if f16 else d["w"]
    b = d["b"].astype(np.float16).astype(np.float32) if f16 else d["b"]
    scores = tf.sigmoid(emb @ w + b)
    return scores.numpy(), emb.numpy()


def main() -> None:
    specs = collect()
    PUBLIC_MODEL.mkdir(parents=True, exist_ok=True)
    blobs, layers_json, offset = [], [], 0
    for s in specs:
        entry = dict(kind=s["kind"], stride=s["stride"], wShape=list(s["w"].shape), bShape=list(s["b"].shape))
        for key in ("w", "b"):
            arr = s[key].astype("<f2").tobytes()
            entry[key + "Offset"] = offset
            entry[key + "Length"] = s[key].size
            offset += len(arr)
            blobs.append(arr)
        layers_json.append(entry)
    (PUBLIC_MODEL / "yamnet.bin").write_bytes(b"".join(blobs))
    manifest = dict(
        name="YAMNet (Google, Apache-2.0), batch-norm folded, float16",
        source="https://github.com/tensorflow/models/tree/master/research/audioset/yamnet",
        weights="yamnet.bin", dtype="float16", inputShape=[96, 64], embeddingSize=1024,
        numClasses=521, layers=layers_json,
    )
    (PUBLIC_MODEL / "yamnet.json").write_text(json.dumps(manifest))
    (PUBLIC_MODEL / "audioset-classes.json").write_text(json.dumps(audioset_class_names()))

    # Fidelity check on real audio: exported float16 net vs the official Keras model.
    wav = np.concatenate([load_wav_16k(ESC50 / "audio" / f) for f in
                          ["1-100032-A-0.wav", "1-115545-A-48.wav", "2-102414-G-17.wav"]])
    patches = yc.log_mel_patches(wav)
    ref_s, ref_e = [t.numpy() for t in yc.backbone()(patches, training=False)]
    f32_s, f32_e = numpy_forward(specs, patches, f16=False)
    f16_s, f16_e = numpy_forward(specs, patches, f16=True)
    report = dict(
        patches=int(len(patches)),
        bytes=offset,
        folded_f32_max_abs_emb=float(np.abs(f32_e - ref_e).max()),
        folded_f32_max_abs_score=float(np.abs(f32_s - ref_s).max()),
        f16_max_abs_emb=float(np.abs(f16_e - ref_e).max()),
        f16_max_abs_score=float(np.abs(f16_s - ref_s).max()),
        f16_emb_cosine_min=float(min(
            np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12) for a, b in zip(f16_e, ref_e))),
        f16_top1_agreement=float(np.mean(f16_s.argmax(1) == ref_s.argmax(1))),
    )
    (RESULTS / "backbone_export.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
