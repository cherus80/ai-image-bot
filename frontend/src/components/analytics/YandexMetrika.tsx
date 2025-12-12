import React from 'react';

declare global {
  interface Window {
    ym?: (...args: any[]) => void;
  }
}

export const YandexMetrika: React.FC = () => {
  const counterId = import.meta.env.VITE_YANDEX_METRIKA_ID;

  React.useEffect(() => {
    if (!counterId) return;
    if (document.getElementById('ym-tag')) return;

    const script = document.createElement('script');
    script.id = 'ym-tag';
    script.async = true;
    script.src = 'https://mc.yandex.ru/metrika/tag.js';
    script.onload = () => {
      if (window.ym) {
        window.ym(Number(counterId), 'init', {
          clickmap: true,
          trackLinks: true,
          accurateTrackBounce: true,
          defer: true,
          webvisor: true,
        });
      }
    };
    document.head.appendChild(script);

    return () => {
      script.remove();
    };
  }, [counterId]);

  if (!counterId) return null;

  return (
    <noscript>
      <div>
        <img
          src={`https://mc.yandex.ru/watch/${counterId}`}
          style={{ position: 'absolute', left: '-9999px' }}
          alt=""
        />
      </div>
    </noscript>
  );
};
