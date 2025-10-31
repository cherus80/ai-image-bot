/**
 * useAuth hook
 *
 * Provides easy access to authentication state and actions
 */

import { useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import { isTelegramWebApp } from '../utils/telegram';

export const useAuth = () => {
  const {
    user,
    token,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    refreshProfile,
    clearError,
  } = useAuthStore();

  // Auto-login on mount if not authenticated and in Telegram
  useEffect(() => {
    const attemptAutoLogin = async () => {
      // Skip if already authenticated or loading
      if (isAuthenticated || isLoading) {
        return;
      }

      // Skip if not in Telegram
      if (!isTelegramWebApp()) {
        console.warn('Not running in Telegram WebApp');
        return;
      }

      // Attempt login
      try {
        await login();
      } catch (error) {
        console.error('Auto-login failed:', error);
        // Error is already stored in state
      }
    };

    attemptAutoLogin();
  }, []); // Run only on mount

  return {
    // State
    user,
    token,
    isAuthenticated,
    isLoading,
    error,

    // Actions
    login,
    logout,
    refreshProfile,
    clearError,

    // Computed values
    hasCredits: user ? user.balance_credits > 0 : false,
    canUseFreemium: user ? user.can_use_freemium : false,
    hasActiveSubscription: user
      ? user.subscription_type !== null &&
        user.subscription_expires_at !== null &&
        new Date(user.subscription_expires_at) > new Date()
      : false,
  };
};
