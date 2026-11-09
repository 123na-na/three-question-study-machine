export function generateShareText(courseName: string, kpTitle: string, score: number): string {
  const now = new Date();
  const dateStr = now.getFullYear() + '年' + (now.getMonth() + 1) + '月' + now.getDate() + '日';
  let level = '需复习';
  if (score >= 90) level = '优秀';
  else if (score >= 75) level = '良好';
  else if (score >= 60) level = '合格';

  return '📖 我在「三问高效学习机」完成了「' + courseName + ' - ' + kpTitle + '」的学习！' +
    '\n\n📊 学习评分：' + score + '分（' + level + '）' +
    '\n📅 ' + dateStr +
    '\n\n🔗 使用「三问高效学习机」，高效掌握每一个知识点！';
}

export function copyToClipboard(text: string): void {
  const pasteboard = getPastable();
  if (pasteboard) {
    pasteboard.setData({
      mimeType: 'text/plain',
      data: text,
    });
  }
}

function getPastable(): string {
  try {
    return getContext(this).createDataShareHelper('clipboard');
  } catch (e) {
    console.error('[ShareUtil] Clipboard not available: ' + e.message);
    return null;
  }
}
