export default function sec2Min(sec) {
  const min = Math.floor(sec / 60);
  const secrem = Math.floor(sec % 60);
  return {
    min: min,
    sec: secrem,
  };
}
