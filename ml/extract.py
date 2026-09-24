"""Compute YAMNet patch embeddings for every training/eval source and cache them.

Outputs (in WORK/cache):
  esc50.npz     per-patch embeddings/scores/levels for all 2,000 ESC-50 clips
  negatives.npz per-patch embeddings for speech + background negatives
Each patch row carries (clip index, fold, target) so folds stay separable.
"""
from __future__ import annotations

import glob
import random

import numpy as np
import pandas as pd

from common import CACHE, DATA, ESC50, SR, load_wav_16k
import yamnet_core as yc

MSC = DATA / "msc" / "mini_speech_commands"
SC_BG = DATA / "sc_bg" / "_background_noise_"
# running_tap sounds like ESC-50 "pouring_water"; dude_miaowing is a person imitating a cat.
# Both would be wrong-label negatives, so they are excluded.
BG_FILES = ["white_noise.wav", "pink_noise.wav", "exercise_bike.wav", "doing_the_dishes.wav"]


def speech_clips(n: int, seed: int = 0) -> list[np.ndarray]:
    """n five-second 'utterances': 3-6 random Speech Commands words with short gaps."""
    rng = random.Random(seed)
    words = sorted(glob.glob(str(MSC / "*" / "*.wav")))
    out = []
    for _ in range(n):
        parts = []
        for _ in range(rng.randint(3, 6)):
            w = load_wav_16k(rng.choice(words))
            parts += [w, np.zeros(int(rng.uniform(0.05, 0.35) * SR), np.float32)]
        clip = np.concatenate(parts)[: 5 * SR]
        out.append(np.pad(clip, (0, max(0, 5 * SR - len(clip)))))
    return out


def background_clips(seconds: int = 5) -> list[np.ndarray]:
    out = []
    for name in BG_FILES:
        w = load_wav_16k(SC_BG / name)
        for i in range(0, len(w) - seconds * SR, seconds * SR):
            out.append(w[i: i + seconds * SR])
    return out


def run_esc50() -> None:
    meta = pd.read_csv(ESC50 / "meta" / "esc50.csv")
    emb, sc, lvl, clip, fold, target = [], [], [], [], [], []
    for i, row in meta.iterrows():
        wav = load_wav_16k(ESC50 / "audio" / row.filename)
        s, e = yc.embed(wav)
        l = yc.patch_rms_db(wav)
        emb.append(e.astype(np.float16)); sc.append(s.astype(np.float16)); lvl.append(l)
        clip += [i] * len(e); fold += [row.fold] * len(e); target += [row.target] * len(e)
        if i % 200 == 0:
            print("esc50", i, flush=True)
    np.savez_compressed(
        CACHE / "esc50.npz",
        emb=np.concatenate(emb), scores=np.concatenate(sc), level=np.concatenate(lvl),
        clip=np.asarray(clip), fold=np.asarray(fold), target=np.asarray(target),
        categories=np.asarray(sorted(set(zip(meta.target, meta.category))), dtype=object),
    )


def run_negatives() -> None:
    groups = {"speech": speech_clips(600), "background": background_clips()}
    emb, sc, kind, clip = [], [], [], []
    for k, clips in groups.items():
        for j, wav in enumerate(clips):
            s, e = yc.embed(wav)
            emb.append(e.astype(np.float16)); sc.append(s.astype(np.float16))
            kind += [k] * len(e); clip += [j] * len(e)
        print("negatives", k, len(clips), flush=True)
    np.savez_compressed(
        CACHE / "negatives.npz", emb=np.concatenate(emb), scores=np.concatenate(sc),
        kind=np.asarray(kind), clip=np.asarray(clip),
    )


if __name__ == "__main__":
    run_esc50()
    run_negatives()
    print("EXTRACT_DONE")
