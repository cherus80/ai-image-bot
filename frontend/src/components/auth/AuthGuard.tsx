/**
 * AuthGuard component
 *
 * Protects routes that require authentication
 * Shows loading state during authentication
 * Redirects to error page if authentication fails
 */

import React, { ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { LoadingPage } from '../../pages/LoadingPage';
import { isTelegramWebApp } from '../../utils/telegram';

interface AuthGuardProps {
  children: ReactNode;
  fallback?: ReactNode;
}

export const AuthGuard: React.FC<AuthGuardProps> = ({ children, fallback }) => {
  const { isAuthenticated, isLoading, error } = useAuth();

  // Check if running in Telegram
  const inTelegram = isTelegramWebApp();

  // Not in Telegram - show error
  if (!inTelegram) {
    return fallback || (
      <div className="flex flex-col items-center justify-center min-h-screen bg-red-50 dark:bg-gray-900 p-6">
        <div className="max-w-md text-center">
          <div className="text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-red-600 dark:text-red-400 mb-2">
            Invalid Access
          </h1>
          <p className="text-gray-700 dark:text-gray-300 mb-4">
            This app must be opened through Telegram.
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Please use the official Telegram app to access this service.
          </p>
        </div>
      </div>
    );
  }

  // Loading - show loading page
  if (isLoading) {
    return <LoadingPage message="Authenticating..." />;
  }

  // Error - show error page
  if (error && !isAuthenticated) {
    return fallback || (
      <div className="flex flex-col items-center justify-center min-h-screen bg-yellow-50 dark:bg-gray-900 p-6">
        <div className="max-w-md text-center">
          <div className="text-6xl mb-4">🔒</div>
          <h1 className="text-2xl font-bold text-yellow-600 dark:text-yellow-400 mb-2">
            Authentication Failed
          </h1>
          <p className="text-gray-700 dark:text-gray-300 mb-4">
            {error}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // Authenticated - render children
  if (isAuthenticated) {
    return <>{children}</>;
  }

  // Fallback - redirect to login (shouldn't happen with auto-login)
  return <Navigate to="/login" replace />;
};
