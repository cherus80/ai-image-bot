/**
 * Error Page
 *
 * Generic error page for various error scenarios
 */

import React from 'react';

interface ErrorPageProps {
  title?: string;
  message?: string;
  icon?: string;
  onRetry?: () => void;
}

export const ErrorPage: React.FC<ErrorPageProps> = ({
  title = 'Что-то пошло не так',
  message = 'Произошла непредвиденная ошибка. Пожалуйста, попробуйте еще раз.',
  icon = '⚠️',
  onRetry,
}) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      <div className="max-w-md text-center">
        <div className="text-6xl mb-4">{icon}</div>

        <h1 className="text-2xl font-bold text-gray-800 dark:text-white mb-2">
          {title}
        </h1>

        <p className="text-gray-600 dark:text-gray-300 mb-6">
          {message}
        </p>

        {onRetry && (
          <button
            onClick={onRetry}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Попробовать снова
          </button>
        )}
      </div>
    </div>
  );
};
