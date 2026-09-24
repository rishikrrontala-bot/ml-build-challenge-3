"""Shared paths and helpers for the Brackets training / evaluation pipeline.

Everything heavy (datasets, venv, cached embeddings) lives in WORK, outside the
repo. See PROGRESS.md "Resume guide" for how to recreate it.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

REPO = Path(__file__).resolve().parents[1]
WORK = Path(os.environ.get("BRACKETS_WORK", "/home/user/work"))
DATA = WORK / "data"
CACHE = WORK / "cache"
ESC50 = DATA / "ESC-50"
YAMNET_H5 = DATA / "yamnet.h5"
YAMNET_SRC = WORK / "tfmodels" / "research" / "audioset" / "yamnet"
CLASS_MAP_CSV = YAMNET_SRC / "yamnet_class_map.csv"
RESULTS = REPO / "ml" / "results"
PUBLIC_MODEL = REPO / "public" / "model"

SR = 16000
PATCH_HOP_S = 0.48
PATCH_WIN_S = 0.96

CACHE.mkdir(parents=True, exist_ok=True)
RESULTS.mkdir(parents=True, exist_ok=True)

if str(YAMNET_SRC) not in sys.path:
    sys.path.insert(0, str(YAMNET_SRC))


def load_wav_16k(path: Path | str) -> np.ndarray:
    """Load any wav, downmix to mono, resample to 16 kHz float32 in [-1, 1]."""
    import resampy
    import soundfile as sf

    wav, sr = sf.read(str(path), dtype="float32", always_2d=True)
    wav = wav.mean(axis=1)
    if sr != SR:
        wav = resampy.resample(wav, sr, SR)
    return wav.astype(np.float32)


def audioset_class_names() -> list[str]:
    import csv

    with open(CLASS_MAP_CSV) as f:
        r = csv.reader(f)
        next(r)
        return [row[2] for row in r]
