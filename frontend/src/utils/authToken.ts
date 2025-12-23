const AUTH_STORAGE_KEY = 'auth-storage';
const AUTH_TOKEN_SESSION_KEY = 'auth-token';

let memoryToken: string | null = null;

export const getAuthToken = (): string | null => {
  if (memoryToken) {
    return memoryToken;
  }

  if (typeof window === 'undefined') {
    return null;
  }

  try {
    const sessionToken = sessionStorage.getItem(AUTH_TOKEN_SESSION_KEY);
    if (sessionToken) {
      memoryToken = sessionToken;
      return sessionToken;
    }
  } catch (error) {
    console.error('Failed to read auth token from sessionStorage:', error);
  }

  try {
    const authStorage = localStorage.getItem(AUTH_STORAGE_KEY);
    if (!authStorage) {
      return null;
    }
    const parsed = JSON.parse(authStorage);
    const token = parsed?.state?.token || null;
    if (token) {
      memoryToken = token;
      try {
        sessionStorage.setItem(AUTH_TOKEN_SESSION_KEY, token);
      } catch (error) {
        console.error('Failed to cache auth token in sessionStorage:', error);
      }
    }
    return token;
  } catch (error) {
    console.error('Failed to parse auth storage:', error);
    return null;
  }
};

export const setAuthToken = (token: string | null) => {
  memoryToken = token;

  if (typeof window === 'undefined') {
    return;
  }

  try {
    if (token) {
      sessionStorage.setItem(AUTH_TOKEN_SESSION_KEY, token);
    } else {
      sessionStorage.removeItem(AUTH_TOKEN_SESSION_KEY);
    }
  } catch (error) {
    console.error('Failed to update auth token cache:', error);
  }
};

export const clearAuthToken = () => {
  setAuthToken(null);
};
