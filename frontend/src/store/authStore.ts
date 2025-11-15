/**
 * Zustand store for authentication state
 */

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { UserProfile } from '../types/auth';
import { loginWithTelegram, getCurrentUser } from '../api/auth';
import { getTelegramInitData } from '../utils/telegram';

interface AuthState {
  // State
  user: UserProfile | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  login: () => Promise<void>;
  logout: () => void;
  refreshProfile: () => Promise<void>;
  setUser: (user: UserProfile) => void;
  setToken: (token: string) => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // Login action
      login: async () => {
        set({ isLoading: true, error: null });

        try {
          // DEV MODE: Check first before trying to get Telegram data
          const isDev = import.meta.env.DEV;

          // Try to get Telegram initData
          let initData: string | null = null;

          try {
            initData = getTelegramInitData();
          } catch (error) {
            // If not in Telegram and in DEV mode, use mock data
            if (isDev) {
              console.warn('🔧 DEV MODE: Using mock user data (no Telegram data available)');

              // Mock user data for local development
              const mockUser: UserProfile = {
                id: 1,
                telegram_id: 123456789,
                username: 'dev_user',
                first_name: 'Dev',
                last_name: 'User',
                language_code: 'ru',
                balance_credits: 10,
                subscription_type: 'PRO',
                subscription_expires_at: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
                freemium_actions_used: 0,
                freemium_actions_remaining: 10,
                freemium_actions_limit: 10,
                freemium_reset_at: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
                freemium_last_reset: new Date().toISOString(),
                can_use_freemium: true,
                is_premium: true,
                is_blocked: false,
                created_at: new Date().toISOString(),
                last_activity_at: new Date().toISOString(),
                referral_code: 'DEV123',
                referred_by_id: null,
              };

              set({
                token: 'mock_jwt_token_for_development',
                user: mockUser,
                isAuthenticated: true,
                isLoading: false,
                error: null,
              });

              return;
            }

            // Not in DEV mode and no Telegram data - throw error
            throw error;
          }

          // Got Telegram initData

          if (!initData) {
            throw new Error('Данные Telegram недоступны. Пожалуйста, откройте это приложение в Telegram.');
          }

          // Call backend auth API
          const response = await loginWithTelegram(initData);

          // Save token and user
          // Note: Zustand persist middleware automatically saves to localStorage (see line 148-156)
          set({
            token: response.access_token,
            user: response.user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          const errorMessage = error.detail || 'Ошибка авторизации';
          set({
            token: null,
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: errorMessage,
          });

          // Zustand persist will automatically clear localStorage when state is null

          throw error;
        }
      },

      // Logout action
      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        });

        // Zustand persist will automatically clear localStorage when state is null
      },

      // Refresh user profile from server
      refreshProfile: async () => {
        const { token } = get();

        if (!token) {
          throw new Error('Не авторизован');
        }

        set({ isLoading: true, error: null });

        try {
          const user = await getCurrentUser();

          set({
            user,
            isLoading: false,
            error: null,
          });

          // Zustand persist automatically updates localStorage
        } catch (error: any) {
          const errorMessage = error.detail || 'Не удалось обновить профиль';
          set({
            isLoading: false,
            error: errorMessage,
          });

          throw error;
        }
      },

      // Set user (used after successful operations that return updated user)
      setUser: (user: UserProfile) => {
        set({ user });
        // Zustand persist automatically updates localStorage
      },

      // Set token (used for manual token updates)
      setToken: (token: string) => {
        set({ token, isAuthenticated: true });
        // Zustand persist automatically updates localStorage
      },

      // Clear error
      clearError: () => {
        set({ error: null });
      },
    }),
    {
      name: 'auth-storage', // unique name for localStorage key
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        // Only persist token and user, not loading/error states
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
