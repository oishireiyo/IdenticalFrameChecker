export default function zeroPadding(num, len) {
  if (len < num.toString().length) {
    console.error('指定した桁数よりも大きな数字が入力されました。');
    return num;
  }
  return (Array(len).join('0') + num).slice(-len);
}
