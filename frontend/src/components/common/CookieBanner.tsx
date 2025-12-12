import React from 'react';

const STORAGE_KEY = 'cookie-consent';

export const CookieBanner: React.FC = () => {
  const [visible, setVisible] = React.useState(false);

  React.useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) {
      setVisible(true);
    }
  }, []);

  const accept = () => {
    localStorage.setItem(STORAGE_KEY, 'accepted');
    setVisible(false);
  };

  if (!visible) return null;

  return (
    <div className="fixed inset-x-0 bottom-0 z-40 px-4 pb-4">
      <div className="max-w-4xl mx-auto bg-white shadow-xl border border-slate-200 rounded-2xl p-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div className="text-sm text-dark-700 leading-snug">
          Мы используем cookie для авторизации, аналитики и улучшения сервиса. Подробнее —{' '}
          <a href="/privacy" className="text-primary-700 font-semibold hover:text-primary-800 underline">
            политика конфиденциальности
          </a>
          .
        </div>
        <div className="flex items-center gap-2">
          <button
            className="px-4 py-2 text-sm font-semibold text-white rounded-xl bg-gradient-to-r from-primary-500 to-secondary-500 shadow hover:shadow-md transition"
            onClick={accept}
          >
            Понятно
          </button>
        </div>
      </div>
    </div>
  );
};
