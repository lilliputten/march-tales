export function floatToStr(num: number | undefined) {
  if (!num) {
    return '0';
  }
  if (typeof num === 'string') {
    if (isNaN(num)) {
      return '0';
    }
    num = Number(num);
  }
  return num
    .toFixed(3)
    .replace(/(\.\d+)0+$/, '$1')
    .replace(/\.0+$/, '');
}
