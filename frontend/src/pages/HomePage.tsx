/**
 * Главная страница - выбор между Примеркой и Редактированием
 * Дизайн согласно макету: чистый, современный UI
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { AuthGuard } from '../components/auth/AuthGuard';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        {/* Main Content */}
        <main className="flex-1 max-w-2xl mx-auto w-full px-4 py-8">
          {/* Header with Logo */}
          <div className="text-center mb-8">
            {/* Icon */}
            <div className="w-20 h-20 mx-auto mb-4 bg-gradient-to-br from-blue-500 to-blue-600 rounded-3xl flex items-center justify-center shadow-lg">
              <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
            </div>

            {/* Title */}
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              AI Image Generator
            </h1>
            <p className="text-gray-600">
              Примеряйте одежду и редактируйте фото
            </p>
          </div>

          {/* Balance Card */}
          {user && (
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-4 mb-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {/* Wallet Icon */}
                  <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
                    <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Баланс</p>
                    <p className="text-xl font-bold text-gray-900">{user.balance_credits} кредитов</p>
                  </div>
                </div>
                <button
                  onClick={() => navigate('/profile')}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
                >
                  Пополнить
                </button>
              </div>
            </div>
          )}

          {/* Feature Cards */}
          <div className="space-y-4 mb-6">
            {/* Fitting Card */}
            <button
              onClick={() => navigate('/fitting')}
              className="w-full bg-white rounded-2xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow text-left"
            >
              <div className="flex items-start space-x-4">
                {/* Icon */}
                <div className="w-16 h-16 bg-blue-500 rounded-2xl flex items-center justify-center flex-shrink-0">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                  </svg>
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <h3 className="text-lg font-semibold text-gray-900">
                      Примерка одежды
                    </h3>
                    <svg className="w-5 h-5 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>

                  <p className="text-sm text-gray-600 mb-3">
                    Примерьте одежду или аксессуары на своё фото или фото модели
                  </p>

                  <div className="flex items-center space-x-2">
                    <span className="inline-block px-3 py-1 text-xs font-medium text-gray-700 bg-gray-100 rounded-full">
                      Простой квиз
                    </span>
                    <span className="text-xs text-gray-500">• 2 кредита</span>
                  </div>
                </div>
              </div>
            </button>

            {/* Editing Card */}
            <button
              onClick={() => navigate('/editing')}
              className="w-full bg-white rounded-2xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow text-left"
            >
              <div className="flex items-start space-x-4">
                {/* Icon */}
                <div className="w-16 h-16 bg-purple-500 rounded-2xl flex items-center justify-center flex-shrink-0">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                  </svg>
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <h3 className="text-lg font-semibold text-gray-900">
                      Редактирование AI
                    </h3>
                    <svg className="w-5 h-5 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>

                  <p className="text-sm text-gray-600 mb-3">
                    Изменяйте изображения с помощью AI-ассистента в чате
                  </p>

                  <div className="flex items-center space-x-2">
                    <span className="inline-block px-3 py-1 text-xs font-medium text-gray-700 bg-gray-100 rounded-full">
                      Чат с AI
                    </span>
                    <span className="text-xs text-gray-500">• 1-2 кредита</span>
                  </div>
                </div>
              </div>
            </button>
          </div>

          {/* Profile Button */}
          <button
            onClick={() => navigate('/profile')}
            className="w-full bg-white rounded-2xl shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow flex items-center justify-center space-x-2"
          >
            <svg className="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <span className="text-base font-medium text-gray-900">
              Профиль и история
            </span>
          </button>
        </main>
      </div>
    </AuthGuard>
  );
};
