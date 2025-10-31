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
          // Get Telegram initData
          const initData = getTelegramInitData();

          if (!initData) {
            throw new Error('Telegram initData not available. Please open this app in Telegram.');
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
          const errorMessage = error.detail || 'Authentication failed';
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
          throw new Error('Not authenticated');
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
          const errorMessage = error.detail || 'Failed to refresh profile';
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
