import React from 'react';
import { PublicLayout } from '../components/common/PublicLayout';
import { Link } from 'react-router-dom';

export const ContactsPage: React.FC = () => {
  return (
    <PublicLayout>
      <div className="max-w-4xl mx-auto px-4 py-12 space-y-6">
        <div className="space-y-2">
          <p className="text-sm font-semibold text-primary-600 uppercase">Контакты и реквизиты</p>
          <h1 className="text-3xl font-bold text-dark-900">Связь и реквизиты исполнителя</h1>
          <p className="text-dark-600">
            Самозанятый: Чернов Руслан Васильевич. ИНН 222312090918. Домен ai-generator.mix4.ru.
          </p>
        </div>

        <div className="bg-white rounded-2xl border border-white/80 shadow-sm p-6 space-y-3">
          <h2 className="text-xl font-semibold text-dark-900">Основные данные</h2>
          <ul className="text-sm text-dark-700 space-y-1">
            <li>ИНН: 222312090918</li>
            <li>Статус: Самозанятый (НПД)</li>
            <li>Телефон: +7 913 220-69-67</li>
            <li>E-mail поддержки: ai-generator@mix4.ru</li>
            <li>Почтовый адрес: Энтузиастов 55-203, 656065, г. Барнаул</li>
            <li>Сайт: https://ai-generator.mix4.ru</li>
            <li>Часы поддержки: 10:00–18:00 (МСК)</li>
          </ul>
        </div>

        <div className="bg-white rounded-2xl border border-white/80 shadow-sm p-6 space-y-3">
          <h2 className="text-xl font-semibold text-dark-900">Предоставление услуги</h2>
          <ul className="text-sm text-dark-700 space-y-1">
            <li>Цифровой сервис: виртуальная примерка и AI-редактирование изображений.</li>
            <li>Начисление после оплаты: мгновенно, баланс виден в профиле.</li>
            <li>Хранение: фото удаляются через 24 часа; переписка — через 30 дней.</li>
            <li>Физическая доставка не требуется.</li>
          </ul>
        </div>

        <div className="flex flex-wrap gap-4 text-sm font-semibold text-primary-700">
          <Link to="/pricing" className="hover:text-primary-800">Тарифы →</Link>
          <Link to="/oferta" className="hover:text-primary-800">Оферта →</Link>
          <Link to="/privacy" className="hover:text-primary-800">Политика →</Link>
        </div>
      </div>
    </PublicLayout>
  );
};
