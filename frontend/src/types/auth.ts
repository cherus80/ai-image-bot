/**
 * Auth types for Telegram WebApp authentication
 */

export interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code?: string;
  is_premium?: boolean;
}

export interface UserProfile {
  id: number;
  telegram_id: number;
  username: string | null;
  first_name: string | null;
  last_name: string | null;
  language_code: string | null;
  balance_credits: number;
  subscription_type: string | null;
  subscription_expires_at: string | null;
  freemium_actions_used: number;
  freemium_reset_at: string;
  can_use_freemium: boolean;
  is_premium: boolean;
  is_blocked: boolean;
  created_at: string;
  last_activity_at: string;
  referral_code: string;
  referred_by_id: number | null;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: UserProfile;
}

export interface TelegramAuthRequest {
  init_data: string;
}

export interface AuthError {
  detail: string;
}
