import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { handlePaymentReturn } from '../api/payment';

export const PaymentReturnPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Просто проксируем на /profile, сохранив payment_id из query
    const search = location.search || '';
    // Чтение ID нужно, чтобы ЮKassa успела дописать query параметр (побочный эффект не обязателен)
    handlePaymentReturn();
    navigate(`/profile${search}`, { replace: true });
  }, [location.search, navigate]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 text-center p-6">
      <div className="text-5xl mb-4">🔄</div>
      <h1 className="text-2xl font-bold text-gray-800 mb-2">Возвращаем вас в профиль</h1>
      <p className="text-gray-600">Секунда... проверяем статус платежа.</p>
    </div>
  );
};

