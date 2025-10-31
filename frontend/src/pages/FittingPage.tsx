/**
 * Страница примерки одежды
 * Главная страница для виртуальной примерки
 */

import React, { useEffect } from 'react';
import { FittingWizard } from '../components/fitting/FittingWizard';
import { useAuthStore } from '../store/authStore';
import { useFittingStore } from '../store/fittingStore';
import { AuthGuard } from '../components/auth/AuthGuard';

export const FittingPage: React.FC = () => {
  const { user } = useAuthStore();
  const { reset } = useFittingStore();

  // Сброс состояния при монтировании страницы
  useEffect(() => {
    reset();
  }, [reset]);

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
          <div className="max-w-2xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  Виртуальная примерка
                </h1>
                <p className="text-sm text-gray-600">
                  Примерьте одежду на своё фото
                </p>
              </div>
              {user && (
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-700">
                    {user.balance_credits} кредитов
                  </p>
                  {user.subscription_type && user.subscription_type !== 'none' && (
                    <span className="text-xs text-blue-600">
                      {user.subscription_type}
                    </span>
                  )}
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Main content */}
        <main>
          <FittingWizard />
        </main>
      </div>
    </AuthGuard>
  );
};
