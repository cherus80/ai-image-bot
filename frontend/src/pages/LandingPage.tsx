import React from 'react';
import { Link } from 'react-router-dom';
import { PublicLayout } from '../components/common/PublicLayout';

const actions = [
  {
    title: 'Примерка одежды',
    description: 'Примерьте одежду и аксессуары на своё фото',
    details: 'Загрузите своё фото и фото одежды, и наш AI создаст реалистичную примерку',
    credits: '2 кредита за примерку',
    gradient: 'from-[#7c5cf6] to-[#45a3ff]',
    icon: (
      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M9.5 6h5l2 3v9a2 2 0 01-2 2h-5a2 2 0 01-2-2V9l2-3z"
        />
      </svg>
    ),
    cta: 'Начать',
    link: '/register',
  },
  {
    title: 'Редактирование фото',
    description: 'Редактируйте изображения с помощью AI-ассистента',
    details: 'Общайтесь с AI и описывайте изменения естественным языком',
    credits: '1 кредит за запрос + 2 за генерацию',
    gradient: 'from-[#ff7a7f] to-[#f59e0b]',
    icon: (
      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 20h9" />
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M16.5 3.5a2.121 2.121 0 113 3L7 19l-4 1 1-4 12.5-12.5z"
        />
      </svg>
    ),
    cta: 'Начать',
    link: '/register',
  },
];

const featureTiles = [
  {
    title: 'Виртуальная примерка',
    desc: 'Точные наложения одежды и аксессуаров на ваши фото.',
    icon: '👗',
  },
  {
    title: 'AI-редактирование в чате',
    desc: 'Ассистент формирует промпты и подсказывает варианты правок.',
    icon: '🤖',
  },
  {
    title: 'Прозрачные тарифы',
    desc: 'Подписка или кредиты, оферта и политика открыты для модерации.',
    icon: '💳',
  },
  {
    title: 'Готовность к ЮKassa',
    desc: 'Реальные услуги, реквизиты, автоудаление файлов.',
    icon: '✅',
  },
];

const steps = [
  { title: 'Загрузите фото', desc: 'Портрет или полный рост + одежда/аксессуар.', num: 1 },
  { title: 'Опишите задачу', desc: 'Укажите, что примеряем или какие правки нужны.', num: 2 },
  { title: 'Получите результат', desc: 'AI готовит готовое изображение и сохраняет в историю.', num: 3 },
];

const faq = [
  {
    q: 'Сколько стоят действия?',
    a: '1 действие по подписке или 2 кредита. Примерка — 2 кредита, ассистент — 1 кредит, генерация — 2 кредита.',
  },
  {
    q: 'Что с безопасностью?',
    a: 'Фото примерки хранятся 24 часа, переписки — 30 дней, далее удаляются автоматически.',
  },
  {
    q: 'Нужна ли регистрация?',
    a: 'Да, чтобы сохранить историю и баланс. Регистрация займёт минуту.',
  },
];

export const LandingPage: React.FC = () => {
  return (
    <PublicLayout>
      <div className="bg-slate-50 text-slate-900">
        {/* Hero */}
        <section className="relative overflow-hidden pt-24 pb-16">
          <div className="absolute -left-24 top-0 w-80 h-80 bg-purple-200 blur-3xl opacity-60" />
          <div className="absolute -right-10 bottom-0 w-80 h-80 bg-blue-200 blur-3xl opacity-60" />

          <div className="max-w-6xl mx-auto px-4 grid lg:grid-cols-2 gap-12 items-center relative z-10">
            <div className="space-y-6">
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-orange-50 border border-orange-100 text-orange-600 text-sm font-semibold shadow-sm">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8V4m0 4a4 4 0 00-4 4h4m0-4a4 4 0 014 4h-4m0 0v4m0 0h4m-4 0H8" />
                </svg>
                <span>Бонус при регистрации: 10 кредитов</span>
              </div>

              <h1 className="text-4xl lg:text-5xl font-extrabold leading-tight text-slate-900">
                Виртуальная примерка и <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-pink-500">AI-редактирование</span>
              </h1>
              <p className="text-lg text-slate-600 leading-relaxed">
                Загружайте фото, примеряйте одежду, улучшайте изображения и получайте идеальный визуал с помощью умного ассистента.
              </p>

              <div className="bg-white p-4 rounded-xl border border-slate-100 shadow-soft flex items-start gap-4">
                <div className="w-10 h-10 rounded-full bg-green-100 text-green-600 flex items-center justify-center shrink-0">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <p className="font-bold text-slate-800">Специальный оффер</p>
                  <p className="text-slate-500">10 бесплатных кредитов всем новым пользователям.</p>
                </div>
              </div>

              <div className="flex flex-wrap gap-3">
                <Link
                  to="/register"
                  className="px-6 py-3 rounded-full text-white font-semibold bg-gradient-to-r from-blue-500 to-purple-600 shadow-lg shadow-blue-400/30 hover:shadow-blue-400/50 transition"
                >
                  Попробовать бесплатно
                </Link>
                <a
                  href="/#how-it-works"
                  className="px-6 py-3 rounded-full font-semibold text-slate-700 bg-white border border-slate-200 hover:bg-slate-50 transition"
                >
                  Смотреть как работает
                </a>
              </div>
            </div>

            {/* Two main cards */}
            <div className="relative">
              <div className="bg-white rounded-3xl shadow-2xl border border-slate-100 overflow-hidden">
                <div className="p-6 sm:p-8 border-b border-slate-100 bg-slate-50">
                  <h3 className="text-2xl font-bold text-slate-800 mb-2">Выберите функцию</h3>
                  <p className="text-sm text-slate-500 leading-relaxed">
                    Начните с загрузки фото, затем выберите действие.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 p-6 sm:p-8">
                  {actions.map((action) => (
                    <div key={action.title} className="rounded-3xl border border-slate-100 shadow-soft overflow-hidden bg-white flex flex-col">
                      <div className={`text-white px-6 sm:px-8 pt-6 pb-8 text-center bg-gradient-to-br ${action.gradient}`}>
                        <div className="mx-auto w-14 h-14 bg-white/20 rounded-2xl flex items-center justify-center mb-4 shadow-[0_0_25px_rgba(255,255,255,0.25)]">
                          {action.icon}
                        </div>
                        <h4 className="text-2xl font-bold mb-2">{action.title}</h4>
                        <p className="text-white/90 font-medium">{action.description}</p>
                      </div>
                      <div className="p-6 sm:p-8 flex flex-col gap-3">
                        <p className="text-slate-600">{action.details}</p>
                        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-100 text-slate-700 text-sm font-semibold self-start">
                          <svg className="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-2.21 0-4 1.79-4 4 0 1.657 1.343 3 3 3h4.5" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 2v2m0 16v2M4 12H2m20 0h-2M5.64 5.64L4.22 4.22m15.56 15.56l-1.42-1.42M18.36 5.64l1.42-1.42M5.64 18.36l-1.42 1.42" />
                          </svg>
                          <span>{action.credits}</span>
                        </div>
                        <Link
                          to={action.link}
                          className={`w-full py-3 rounded-xl text-white text-sm font-bold shadow-lg hover:shadow-xl transition flex items-center justify-center gap-2 bg-gradient-to-r ${action.gradient}`}
                        >
                          <span>{action.cta}</span>
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="px-6 sm:px-8 pb-6">
                  <div className="bg-slate-50 p-3 rounded-xl text-center border border-slate-100 text-xs text-slate-500 font-medium">
                    <span className="text-orange-500 mr-1">•</span> Все действия списывают 1 действие по подписке или 2 кредита.
                  </div>
                </div>
              </div>
              <div className="absolute -z-10 top-10 -right-10 w-full h-full bg-gradient-to-br from-blue-100 to-purple-100 rounded-3xl opacity-50 blur-3xl" />
            </div>
          </div>
        </section>

        {/* Features */}
        <section id="features" className="py-16">
          <div className="max-w-6xl mx-auto px-4 space-y-6">
            <h2 className="text-3xl font-bold text-center">Что вы получаете</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {featureTiles.map((f) => (
                <div key={f.title} className="bg-white rounded-2xl shadow-soft border border-slate-100 p-5 space-y-3">
                  <div className="text-3xl">{f.icon}</div>
                  <h3 className="text-lg font-semibold text-slate-900">{f.title}</h3>
                  <p className="text-sm text-slate-600">{f.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* How it works */}
        <section id="how-it-works" className="py-16 bg-white">
          <div className="max-w-6xl mx-auto px-4 space-y-8">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <h2 className="text-3xl font-bold">Как это работает</h2>
              <Link to="/app" className="text-sm font-semibold text-blue-600 hover:text-blue-700">Перейти в приложение →</Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {steps.map((s) => (
                <div key={s.num} className="bg-slate-50 rounded-2xl border border-slate-100 shadow-sm p-5">
                  <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 text-white flex items-center justify-center font-bold mb-3">
                    {s.num}
                  </div>
                  <h3 className="text-lg font-semibold text-slate-900">{s.title}</h3>
                  <p className="text-sm text-slate-600">{s.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* AI Assistant */}
        <section className="py-20 bg-gradient-to-br from-purple-50 via-white to-blue-50">
          <div className="max-w-6xl mx-auto px-4 grid md:grid-cols-2 gap-12 items-center">
            <div className="space-y-4">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-100 text-purple-700 text-sm font-semibold">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6M9 8h6m-7 9l-3 3V6a2 2 0 012-2h10a2 2 0 012 2v11l-3-3H8z" />
                </svg>
                <span>AI-ассистент</span>
              </div>
              <h2 className="text-3xl font-extrabold leading-tight">Умный ассистент для быстрых правок</h2>
              <p className="text-lg text-slate-600">
                Ассистент формирует точные промпты, предлагает варианты и учитывает стоимость: −1 кредит за улучшение промпта и −2 кредита за генерацию.
              </p>
            </div>

            <div className="bg-white rounded-3xl border border-slate-200 shadow-2xl overflow-hidden">
              <div className="flex items-center justify-between px-6 py-4 bg-slate-50 border-b border-slate-100">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-pink-500 rounded-2xl flex items-center justify-center text-white shadow-[0_10px_35px_-12px_rgba(249,115,22,0.5)]">
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.5 4.5l6 6m-2.25-3.75L10.5 13.5 9 18l4.5-1.5 6.75-6.75" />
                    </svg>
                  </div>
                  <div>
                    <p className="font-bold text-slate-900 text-lg leading-tight">AI Редактор</p>
                    <p className="text-xs text-slate-400">Ассистент для фото</p>
                  </div>
                </div>
                <div className="px-4 py-2 bg-white rounded-xl shadow-soft border border-slate-100 text-right">
                  <div className="text-lg font-extrabold text-slate-900 leading-none">106</div>
                  <div className="text-[11px] uppercase text-slate-400 tracking-wide leading-none">кредитов</div>
                </div>
              </div>

              <div className="bg-slate-50 px-4 sm:px-6 py-6 flex flex-col gap-4">
                <div className="flex justify-end">
                  <div className="max-w-[75%] bg-gradient-to-r from-[#7c3aed] to-[#0ea5e9] text-white px-4 py-3 rounded-2xl rounded-br-sm shadow-[0_12px_30px_-10px_rgba(59,130,246,0.45)] text-sm">
                    Замени цвет платья на красный
                    <div className="text-[11px] text-white/70 mt-1 text-right">20:37</div>
                  </div>
                </div>

                <div className="bg-white border border-slate-100 rounded-2xl shadow-soft p-4 sm:p-5 space-y-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-white shadow-[0_10px_30px_-12px_rgba(124,58,237,0.5)]">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5h2m-1-2v4m0 2v10m0 0H8m4 0h4" />
                      </svg>
                    </div>
                    <div>
                      <p className="text-xs font-bold text-purple-600 uppercase">AI Assistant</p>
                      <p className="text-[11px] text-slate-400">13:37</p>
                    </div>
                  </div>
                  <p className="text-slate-700 text-sm leading-relaxed">
                    Вот улучшенный промпт: <span className="font-semibold">“Преобразуй цвет платья, заменив текущий оттенок на яркий красный с сохранением текстуры ткани.”</span>
                  </p>
                  <div className="flex flex-wrap gap-2">
                    <span className="px-3 py-1 rounded-full bg-slate-100 text-slate-700 text-xs font-semibold">Короткий</span>
                    <span className="px-3 py-1 rounded-full bg-purple-50 text-purple-700 text-xs font-semibold">Средний</span>
                    <span className="px-3 py-1 rounded-full bg-amber-50 text-amber-700 text-xs font-semibold">Детальный</span>
                  </div>
                  <button className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-bold py-3 rounded-xl shadow-[0_14px_35px_-15px_rgba(59,130,246,0.8)] hover:shadow-[0_16px_38px_-14px_rgba(59,130,246,0.9)] transition">
                    Генерировать изображение
                  </button>
                  <div className="flex items-center gap-2 text-xs text-slate-500">
                    <svg className="w-4 h-4 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M12 2a10 10 0 1010 10A10 10 0 0012 2z" />
                    </svg>
                    <span>AI-ассистент −1 кр, генерация −2 кр.</span>
                  </div>
                </div>

                <div className="bg-white border border-slate-200 rounded-2xl shadow-inner p-3 sm:p-4 flex items-center gap-3">
                  <input
                    className="flex-1 bg-transparent outline-none text-sm text-slate-600 placeholder-slate-400"
                    placeholder="Опишите, как хотите изменить изображение..."
                  />
                  <button className="px-4 py-2 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold text-sm shadow-[0_12px_30px_-12px_rgba(124,58,237,0.5)] flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span>Отправить</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Pricing CTA */}
        <section id="pricing" className="py-16 bg-white">
          <div className="max-w-6xl mx-auto px-4">
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-3xl shadow-2xl overflow-hidden grid md:grid-cols-2 items-center">
              <div className="p-8 text-white space-y-3">
                <p className="text-sm uppercase font-bold text-white/80">Тарифы</p>
                <h3 className="text-3xl font-extrabold leading-tight">Кредиты или подписка — выбирайте, как удобнее</h3>
                <p className="text-white/80">Прозрачные цены и моментальный доступ после оплаты.</p>
                <div className="flex flex-wrap gap-3">
                  <Link to="/pricing" className="px-6 py-3 bg-white text-blue-600 font-semibold rounded-xl shadow-lg hover:shadow-xl transition">Смотреть тарифы</Link>
                  <Link to="/register" className="px-6 py-3 border border-white/60 text-white font-semibold rounded-xl hover:bg-white/10 transition">Начать бесплатно</Link>
                </div>
              </div>
              <div className="bg-white/10 backdrop-blur p-8 text-white space-y-3 border-l border-white/20">
                <p className="text-lg font-semibold">Оплата через ЮKassa</p>
                <p className="text-white/80">ИНН 222312090918 · ai-generator@mix4.ru · +7 913 220-69-67</p>
                <p className="text-white/80">Фото примерки — 24 ч хранения, переписки — 30 дн.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Safety */}
        <section className="py-16 bg-slate-50">
          <div className="max-w-6xl mx-auto px-4 space-y-6">
            <h2 className="text-3xl font-bold text-center">Безопасность и надёжность</h2>
            <div className="grid md:grid-cols-4 gap-4">
              {[ 'Временное хранение файлов', 'Автоматическое удаление', 'Платежи через ЮKassa', 'Защита персональных данных' ].map((item) => (
                <div key={item} className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 text-center text-sm text-slate-700">
                  {item}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section id="faq" className="py-16 bg-white">
          <div className="max-w-6xl mx-auto px-4 space-y-6">
            <h2 className="text-3xl font-bold text-center">Частые вопросы</h2>
            <div className="grid md:grid-cols-3 gap-4">
              {faq.map((item) => (
                <div key={item.q} className="bg-slate-50 rounded-2xl border border-slate-100 p-6 shadow-sm space-y-2">
                  <p className="font-semibold text-slate-900">{item.q}</p>
                  <p className="text-sm text-slate-600 leading-relaxed">{item.a}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="py-16 bg-gradient-to-r from-blue-500 to-purple-600">
          <div className="max-w-6xl mx-auto px-4 text-center text-white space-y-4">
            <h2 className="text-3xl font-extrabold">Готовы примерить и отредактировать?</h2>
            <p className="text-white/80 text-lg">Зарегистрируйтесь, получите 10 кредитов и начните прямо сейчас.</p>
            <div className="flex justify-center gap-3 flex-wrap">
              <Link to="/register" className="px-6 py-3 bg-white text-blue-600 font-semibold rounded-xl shadow-lg hover:shadow-xl transition">Попробовать бесплатно</Link>
              <Link to="/login" className="px-6 py-3 border border-white/70 text-white font-semibold rounded-xl hover:bg-white/10 transition">У меня уже есть аккаунт</Link>
            </div>
          </div>
        </section>
      </div>
    </PublicLayout>
  );
};
