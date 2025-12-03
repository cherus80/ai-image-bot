import React from 'react';
import { Link } from 'react-router-dom';
import { PublicLayout } from '../components/common/PublicLayout';

export const LandingPage: React.FC = () => {
  const stats = [
    { label: 'До 500 действий/мес', desc: 'подписка Pro' },
    { label: '24/7', desc: 'обработка запросов' },
    { label: '24 ч', desc: 'хранение фото примерки' },
    { label: '30 дн', desc: 'хранение переписок' },
  ];

  const features = [
    {
      title: 'Виртуальная примерка',
      desc: 'Загрузите своё фото и одежду/аксессуар — получите примерку за секунды.',
      icon: '🧥',
    },
    {
      title: 'AI-редактирование',
      desc: 'Опишите задачу текстом — ассистент подготовит промпт и результат.',
      icon: '✨',
    },
    {
      title: 'История и безопасность',
      desc: 'Все генерации доступны в истории, файлы удаляются автоматически.',
      icon: '🛡️',
    },
  ];

  const steps = [
    { title: 'Загрузите фото', desc: 'Портрет или полный рост + фото вещи/аксессуара.', num: 1 },
    { title: 'Опишите задачу', desc: 'Выберите зону примерки или введите правки в чат.', num: 2 },
    { title: 'Получите результат', desc: 'AI соберёт финальное изображение, доступное в истории.', num: 3 },
  ];

  return (
    <PublicLayout>
      <div className="bg-gradient-to-br from-primary-50 via-white to-secondary-50">
        <section className="max-w-6xl mx-auto px-4 py-16 grid grid-cols-1 lg:grid-cols-2 gap-10 items-center">
          <div className="space-y-6">
            <p className="text-sm font-semibold text-primary-600 uppercase">AI Media Generator</p>
            <h1 className="text-4xl md:text-5xl font-bold text-dark-900 leading-tight">
              Виртуальная примерка и AI-редактирование изображений
            </h1>
            <p className="text-lg text-dark-600">
              Быстрые примерки одежды и аксессуаров на вашем фото, чат с AI-ассистентом для правок,
              автоматическое удаление файлов и прозрачные тарифы.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link
                to="/register"
                className="px-6 py-3 rounded-xl text-white font-semibold bg-gradient-to-r from-primary-500 to-secondary-500 shadow-lg hover:shadow-xl transition hover:-translate-y-0.5"
              >
                Попробовать бесплатно
              </Link>
              <Link
                to="/pricing"
                className="px-6 py-3 rounded-xl font-semibold text-primary-700 border border-primary-200 hover:bg-primary-50 transition"
              >
                Посмотреть тарифы
              </Link>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {stats.map((item) => (
                <div key={item.label} className="rounded-2xl bg-white shadow-sm border border-white/60 p-4">
                  <p className="text-lg font-semibold text-primary-700">{item.label}</p>
                  <p className="text-xs text-dark-500">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
          <div className="relative">
            <div className="absolute -inset-6 bg-gradient-to-br from-primary-200/40 to-secondary-200/40 blur-3xl rounded-full" />
            <div className="relative bg-white rounded-3xl shadow-2xl border border-white/80 p-6 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-dark-500">Примерка</p>
                  <p className="text-xl font-semibold text-dark-900">AI Fit Session</p>
                </div>
                <span className="px-3 py-1 text-xs rounded-full bg-primary-100 text-primary-700">онлайн</span>
              </div>
              <div className="h-48 rounded-2xl bg-gradient-to-br from-primary-100 via-white to-secondary-100 border border-white/70 flex items-center justify-center text-4xl">
                👗
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm">
                <div className="p-3 rounded-xl bg-primary-50 text-primary-800 border border-primary-100">
                  <p className="font-semibold">24 часа</p>
                  <p className="text-xs text-primary-700">удаление фото</p>
                </div>
                <div className="p-3 rounded-xl bg-secondary-50 text-secondary-800 border border-secondary-100">
                  <p className="font-semibold">30 дней</p>
                  <p className="text-xs text-secondary-700">история чатов</p>
                </div>
              </div>
              <div className="flex items-center justify-between text-sm text-dark-600">
                <span>ИНН 222312090918</span>
                <span>Поддержка 10:00–18:00</span>
              </div>
            </div>
          </div>
        </section>

        <section id="features" className="max-w-6xl mx-auto px-4 py-12 space-y-6">
          <h2 className="text-3xl font-bold text-dark-900 text-center">Что вы получаете</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {features.map((f) => (
              <div key={f.title} className="bg-white rounded-2xl shadow-sm border border-white/80 p-6 space-y-3">
                <div className="text-3xl">{f.icon}</div>
                <h3 className="text-xl font-semibold text-dark-900">{f.title}</h3>
                <p className="text-sm text-dark-600">{f.desc}</p>
              </div>
            ))}
          </div>
        </section>

        <section id="how-it-works" className="max-w-6xl mx-auto px-4 py-12 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-3xl font-bold text-dark-900">Как это работает</h2>
            <Link to="/app" className="text-sm font-semibold text-primary-700 hover:text-primary-800">
              Перейти в приложение →
            </Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {steps.map((s) => (
              <div key={s.num} className="bg-white rounded-2xl border border-white/80 shadow-sm p-5">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 text-white flex items-center justify-center font-bold mb-3">
                  {s.num}
                </div>
                <h3 className="text-lg font-semibold text-dark-900">{s.title}</h3>
                <p className="text-sm text-dark-600">{s.desc}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="max-w-6xl mx-auto px-4 py-12 grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
          <div className="space-y-3">
            <h2 className="text-3xl font-bold text-dark-900">Готовы к модерации ЮKassa</h2>
            <ul className="space-y-2 text-sm text-dark-700">
              <li>• Реальные услуги и цены: подписки/кредиты опубликованы на /pricing.</li>
              <li>• Доставка/предоставление: цифровой сервис, результаты в истории, автоудаление.</li>
              <li>• Оферта и политика: публичные страницы /oferta и /privacy.</li>
              <li>• Реквизиты самозанятого: ИНН 222312090918, контакты на /contacts.</li>
            </ul>
          </div>
          <div className="bg-white rounded-2xl border border-white/80 shadow-sm p-6 space-y-3">
            <h3 className="text-xl font-semibold text-dark-900">Контакты</h3>
            <p className="text-sm text-dark-700">ai-generator@mix4.ru · +7 913 220-69-67</p>
            <p className="text-sm text-dark-700">Энтузиастов 55-203, 656065 · ИНН 222312090918</p>
            <div className="flex flex-wrap gap-3 pt-2">
              <Link to="/oferta" className="text-sm font-semibold text-primary-700 hover:text-primary-800">
                Оферта →
              </Link>
              <Link to="/privacy" className="text-sm font-semibold text-primary-700 hover:text-primary-800">
                Политика →
              </Link>
              <Link to="/contacts" className="text-sm font-semibold text-primary-700 hover:text-primary-800">
                Контакты →
              </Link>
            </div>
          </div>
        </section>
      </div>
    </PublicLayout>
  );
};
