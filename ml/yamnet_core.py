"""YAMNet, split into the two halves Brackets ships.

1. The log-mel front end (waveform -> [N, 96, 64] patches). We keep a NumPy
   reference implementation here (`log_mel_patches`) because the browser runs a
   TypeScript port of exactly this code, and the TS unit tests compare against
   fixtures produced by this function.
2. The CNN backbone (patches -> 521 AudioSet scores + 1024-d embeddings),
   built from the official TensorFlow Models definition and weights.
"""
from __future__ import annotations

import numpy as np

from common import SR, YAMNET_H5

STFT_WIN = 400      # 25 ms
STFT_HOP = 160      # 10 ms
FFT_LEN = 512
MEL_BANDS = 64
MEL_MIN = 125.0
MEL_MAX = 7500.0
LOG_OFFSET = 0.001
PATCH_FRAMES = 96   # 0.96 s
PATCH_HOP = 48      # 0.48 s


def hertz_to_mel(f: np.ndarray) -> np.ndarray:
    # HTK mel scale, exactly as tf.signal.linear_to_mel_weight_matrix.
    return 1127.0 * np.log1p(np.asarray(f, dtype=np.float64) / 700.0)


def mel_matrix() -> np.ndarray:
    """[257, 64] weights; a float64 re-derivation of tf.signal.linear_to_mel_weight_matrix."""
    n_bins = FFT_LEN // 2 + 1
    nyquist = SR / 2.0
    lin_freqs = np.linspace(0.0, nyquist, n_bins)[1:]  # TF drops the DC bin
    spec_mel = hertz_to_mel(lin_freqs)[:, None]
    edges = np.linspace(hertz_to_mel(MEL_MIN), hertz_to_mel(MEL_MAX), MEL_BANDS + 2)
    lower, center, upper = edges[:-2], edges[1:-1], edges[2:]
    lower_slopes = (spec_mel - lower) / (center - lower)
    upper_slopes = (upper - spec_mel) / (upper - center)
    w = np.maximum(0.0, np.minimum(lower_slopes, upper_slopes))
    return np.pad(w, [[1, 0], [0, 0]])  # re-add the zeroed DC row


def pad_waveform(wav: np.ndarray) -> np.ndarray:
    """Zero-pad so we get >=1 patch and an integral number of patch hops (features.pad_waveform)."""
    min_samples = int((0.96 + 0.025 - 0.010) * SR)  # 15600
    n = len(wav)
    pad = max(0, min_samples - n)
    n = max(n, min_samples)
    hop = int(0.48 * SR)
    after = n - min_samples
    hops = int(np.ceil(after / hop))
    pad += hop * hops - after
    return np.pad(wav, (0, pad)).astype(np.float32)


def log_mel(wav: np.ndarray) -> np.ndarray:
    """[frames, 64] log-mel spectrogram (periodic Hann, |rfft| magnitude)."""
    n_frames = 1 + (len(wav) - STFT_WIN) // STFT_HOP
    idx = np.arange(STFT_WIN)[None, :] + STFT_HOP * np.arange(n_frames)[:, None]
    window = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(STFT_WIN) / STFT_WIN)  # periodic
    frames = wav[idx].astype(np.float64) * window
    mag = np.abs(np.fft.rfft(frames, n=FFT_LEN, axis=1))
    mel = mag @ mel_matrix()
    return np.log(mel + LOG_OFFSET).astype(np.float32)


def log_mel_patches(wav: np.ndarray) -> np.ndarray:
    """Waveform (16 kHz) -> [N, 96, 64] patches, matching YAMNet's framing."""
    lm = log_mel(pad_waveform(wav))
    n = 1 + (lm.shape[0] - PATCH_FRAMES) // PATCH_HOP
    return np.stack([lm[i * PATCH_HOP: i * PATCH_HOP + PATCH_FRAMES] for i in range(n)])


def patch_rms_db(wav: np.ndarray) -> np.ndarray:
    """Per-patch RMS level in dBFS, aligned with log_mel_patches."""
    w = pad_waveform(wav)
    n = 1 + (len(w) - 15600) // 7680
    out = []
    for i in range(n):
        seg = w[i * 7680: i * 7680 + 15360]
        out.append(10 * np.log10(np.mean(seg.astype(np.float64) ** 2) + 1e-10))
    return np.asarray(out, dtype=np.float32)


_backbone = None


def backbone():
    """tf_keras model: [N, 96, 64] patches -> (scores [N, 521], embeddings [N, 1024])."""
    global _backbone
    if _backbone is None:
        import params as yparams
        import yamnet as ymodel
        from tf_keras import Model, layers

        p = yparams.Params()
        frames = ymodel.yamnet_frames_model(p)
        frames.load_weights(str(YAMNET_H5))
        inp = layers.Input(shape=(PATCH_FRAMES, MEL_BANDS))
        scores, emb = ymodel.yamnet(inp, p)
        core = Model(inp, [scores, emb])
        # copy weights by layer name from the full frames model
        by_name = {l.name: l for l in frames.layers}
        dense_src = [l for l in frames.layers if isinstance(l, layers.Dense)]
        dense_dst = [l for l in core.layers if isinstance(l, layers.Dense)]
        assert len(dense_src) == len(dense_dst) == 1
        dense_dst[0].set_weights(dense_src[0].get_weights())
        for layer in core.layers:
            if layer.weights and not isinstance(layer, layers.Dense):
                layer.set_weights(by_name[layer.name].get_weights())
        _backbone = (core, frames)
    return _backbone[0]


def frames_model():
    backbone()
    return _backbone[1]


def embed(wav: np.ndarray, batch: int = 256) -> tuple[np.ndarray, np.ndarray]:
    """Waveform -> (AudioSet scores [N, 521], embeddings [N, 1024]) via our NumPy front end."""
    patches = log_mel_patches(wav)
    core = backbone()
    s, e = [], []
    for i in range(0, len(patches), batch):
        a, b = core(patches[i:i + batch], training=False)
        s.append(a.numpy())
        e.append(b.numpy())
    return np.concatenate(s), np.concatenate(e)
