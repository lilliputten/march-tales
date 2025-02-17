export function floatToStr(num: number | undefined) {
  if (!num) {
    return '0';
  }
  return num.toFixed(2).replace(/\.0+$/, '');
}
