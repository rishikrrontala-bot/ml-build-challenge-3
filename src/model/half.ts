/** IEEE-754 binary16 -> float32, for the model weights (stored little-endian float16). */
export function halfToFloat(h: number): number {
  const s = (h & 0x8000) >> 15;
  const e = (h & 0x7c00) >> 10;
  const f = h & 0x03ff;
  let v: number;
  if (e === 0) v = (f / 1024) * 2 ** -14; // subnormal
  else if (e === 0x1f) v = f ? NaN : Infinity;
  else v = (1 + f / 1024) * 2 ** (e - 15);
  return s ? -v : v;
}

export function decodeFloat16(buffer: ArrayBuffer, byteOffset: number, length: number): Float32Array {
  const view = new DataView(buffer, byteOffset, length * 2);
  const out = new Float32Array(length);
  for (let i = 0; i < length; i++) out[i] = halfToFloat(view.getUint16(i * 2, true));
  return out;
}
