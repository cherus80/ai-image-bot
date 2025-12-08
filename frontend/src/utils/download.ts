/**
 * Утилиты для скачивания изображений без открытия нового окна.
 */

export const resolveAbsoluteUrl = (url: string): string => {
  if (!url) return '';
  if (url.startsWith('http://') || url.startsWith('https://')) return url;
  const base = window.location.origin.replace(/\/$/, '');
  const normalized = url.startsWith('/') ? url : `/${url}`;
  return `${base}${normalized}`;
};

export const downloadImage = async (url: string, filename: string): Promise<void> => {
  const targetUrl = resolveAbsoluteUrl(url);
  if (!targetUrl) {
    throw new Error('Пустой URL изображения');
  }

  // Прямая попытка через <a download> (лучше для Safari/iOS)
  try {
    const link = document.createElement('a');
    link.href = targetUrl;
    link.download = filename;
    link.rel = 'noopener noreferrer';
    document.body.appendChild(link);
    link.click();
    link.remove();
    return;
  } catch {
    // если не сработало — идём на fetch-блоб ниже
  }

  // Быстрый путь для data URL
  if (targetUrl.startsWith('data:image')) {
    const link = document.createElement('a');
    link.href = targetUrl;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    return;
  }

  const response = await fetch(targetUrl, {
    mode: 'cors',
    cache: 'no-store',
  });

  if (!response.ok) {
    throw new Error(`Ошибка загрузки файла: ${response.status}`);
  }

  const blob = await response.blob();
  const blobUrl = window.URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.href = blobUrl;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();

  window.setTimeout(() => window.URL.revokeObjectURL(blobUrl), 1000);
  return;
};
