/**
 * YAMNet's front end, ported from ml/yamnet_core.py (itself verified against
 * TensorFlow's features.py to 5e-5). Pure functions over 16 kHz mono audio.
 */
import { FFT } from './fft';

export const SAMPLE_RATE = 16000;
export const STFT_WIN = 400; // 25 ms
export const STFT_HOP = 160; // 10 ms
export const FFT_LEN = 512;
export const MEL_BANDS = 64;
export const MEL_MIN_HZ = 125;
export const MEL_MAX_HZ = 7500;
export const LOG_OFFSET = 0.001;
export const PATCH_FRAMES = 96; // 0.96 s
export const PATCH_HOP_FRAMES = 48; // 0.48 s
export const PATCH_HOP_SECONDS = (PATCH_HOP_FRAMES * STFT_HOP) / SAMPLE_RATE; // 0.48
export const PATCH_WINDOW_SECONDS = (PATCH_FRAMES * STFT_HOP) / SAMPLE_RATE; // 0.96

const MIN_SAMPLES = Math.trunc((0.96 + 0.025 - 0.01) * SAMPLE_RATE); // 15600
const HOP_SAMPLES = Math.trunc(0.48 * SAMPLE_RATE); // 7680
const NUM_BINS = FFT_LEN / 2 + 1; // 257

const hzToMel = (f: number): number => 1127 * Math.log1p(f / 700);

let melCache: Float64Array | null = null;
/** Row-major [257, 64] HTK mel weights, identical to tf.signal.linear_to_mel_weight_matrix. */
export function melMatrix(): Float64Array {
  if (melCache) return melCache;
  const w = new Float64Array(NUM_BINS * MEL_BANDS);
  const lo = hzToMel(MEL_MIN_HZ);
  const hi = hzToMel(MEL_MAX_HZ);
  const edges = Array.from({ length: MEL_BANDS + 2 }, (_, i) => lo + ((hi - lo) * i) / (MEL_BANDS + 1));
  const nyquist = SAMPLE_RATE / 2;
  for (let bin = 1; bin < NUM_BINS; bin++) {
    // tf.linspace(0, nyquist, 257)[1:] — the DC row stays zero
    const mel = hzToMel((nyquist * bin) / (NUM_BINS - 1));
    for (let m = 0; m < MEL_BANDS; m++) {
      const lower = (mel - edges[m]) / (edges[m + 1] - edges[m]);
      const upper = (edges[m + 2] - mel) / (edges[m + 2] - edges[m + 1]);
      w[bin * MEL_BANDS + m] = Math.max(0, Math.min(lower, upper));
    }
  }
  melCache = w;
  return w;
}

/** Zero-pad so there is at least one patch and a whole number of patch hops. */
export function padWaveform(wav: Float32Array): Float32Array {
  let n = wav.length;
  let pad = Math.max(0, MIN_SAMPLES - n);
  n = Math.max(n, MIN_SAMPLES);
  const after = n - MIN_SAMPLES;
  const hops = Math.ceil(after / HOP_SAMPLES);
  pad += HOP_SAMPLES * hops - after;
  if (pad === 0) return wav;
  const out = new Float32Array(wav.length + pad);
  out.set(wav);
  return out;
}

const HANN = (() => {
  const w = new Float64Array(STFT_WIN);
  for (let i = 0; i < STFT_WIN; i++) w[i] = 0.5 - 0.5 * Math.cos((2 * Math.PI * i) / STFT_WIN); // periodic
  return w;
})();

/** Log-mel spectrogram, row-major [frames, 64]. Expects already-padded audio. */
export function logMel(wav: Float32Array): { data: Float32Array; frames: number } {
  const frames = wav.length >= STFT_WIN ? 1 + Math.floor((wav.length - STFT_WIN) / STFT_HOP) : 0;
  const out = new Float32Array(frames * MEL_BANDS);
  const fft = new FFT(FFT_LEN);
  const re = new Float64Array(FFT_LEN);
  const im = new Float64Array(FFT_LEN);
  const mag = new Float64Array(NUM_BINS);
  const frame = new Float64Array(STFT_WIN);
  const mel = melMatrix();
  for (let f = 0; f < frames; f++) {
    const start = f * STFT_HOP;
    for (let i = 0; i < STFT_WIN; i++) frame[i] = wav[start + i] * HANN[i];
    fft.magnitude(frame, mag, re, im);
    for (let m = 0; m < MEL_BANDS; m++) {
      let s = 0;
      for (let b = 1; b < NUM_BINS; b++) s += mag[b] * mel[b * MEL_BANDS + m];
      out[f * MEL_BANDS + m] = Math.log(s + LOG_OFFSET);
    }
  }
  return { data: out, frames };
}

export interface Patches {
  /** Row-major [count, 96, 64]. */
  data: Float32Array;
  count: number;
}

/** 16 kHz waveform -> YAMNet input patches (0.96 s windows every 0.48 s). */
export function logMelPatches(wav: Float32Array): Patches {
  const { data: lm, frames } = logMel(padWaveform(wav));
  const count = frames >= PATCH_FRAMES ? 1 + Math.floor((frames - PATCH_FRAMES) / PATCH_HOP_FRAMES) : 0;
  const size = PATCH_FRAMES * MEL_BANDS;
  const data = new Float32Array(count * size);
  for (let p = 0; p < count; p++) {
    data.set(lm.subarray(p * PATCH_HOP_FRAMES * MEL_BANDS, p * PATCH_HOP_FRAMES * MEL_BANDS + size), p * size);
  }
  return { data, count };
}

/** Per-patch RMS level in dBFS, aligned with logMelPatches (0.96 s windows). */
export function patchLevelsDb(wav: Float32Array): Float32Array {
  const w = padWaveform(wav);
  const count = 1 + Math.floor((w.length - MIN_SAMPLES) / HOP_SAMPLES);
  const win = Math.round(PATCH_WINDOW_SECONDS * SAMPLE_RATE); // 15360
  const out = new Float32Array(count);
  for (let p = 0; p < count; p++) {
    let s = 0;
    const start = p * HOP_SAMPLES;
    for (let i = 0; i < win; i++) {
      const v = w[start + i] ?? 0;
      s += v * v;
    }
    out[p] = 10 * Math.log10(s / win + 1e-10);
  }
  return out;
}

/** Start time (s) of patch i; its centre is start + 0.48 s. */
export const patchStart = (i: number): number => i * PATCH_HOP_SECONDS;
