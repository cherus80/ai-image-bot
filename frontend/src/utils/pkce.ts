/**
 * PKCE helper utilities for VK ID OAuth 2.1
 */

const base64UrlEncode = (buffer: ArrayBuffer) => {
  return btoa(String.fromCharCode(...new Uint8Array(buffer)))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
};

export const generateRandomString = (
  length = 64,
  charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~',
) => {
  let result = '';
  const values = crypto.getRandomValues(new Uint8Array(length));
  for (let i = 0; i < length; i += 1) {
    result += charset[values[i] % charset.length];
  }
  return result;
};

// VK может модифицировать state, убирая точки, поэтому для state исключаем "." из набора.
const STATE_CHARSET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

export const generateCodeVerifier = () => generateRandomString(64);

export const generateCodeChallenge = async (verifier: string) => {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return base64UrlEncode(digest);
};

export const getOrCreateDeviceId = () => {
  const key = 'vk_device_id';
  const existing = localStorage.getItem(key);
  if (existing) return existing;
  const deviceId = crypto.randomUUID?.() || generateRandomString(32);
  localStorage.setItem(key, deviceId);
  return deviceId;
};

type StartVKPKCEAuthOptions = {
  appId: string;
  redirectUri: string;
  scope?: string;
  storageKey?: string;
};

const DEFAULT_STORAGE_KEY = 'vk_pkce';

const buildStorageKey = (storageKey: string, state: string) => `${storageKey}:${state}`;

const persistPKCEPayload = (
  storageKey: string,
  state: string,
  payload: Record<string, unknown>,
) => {
  localStorage.setItem(buildStorageKey(storageKey, state), JSON.stringify(payload));
  localStorage.setItem(`${storageKey}:latest`, state);
};

/**
 * Starts VK ID PKCE authorization by redirecting to id.vk.ru/authorize.
 * Stores verifier/state/nonce in localStorage for later exchange.
 */
export const startVKPKCEAuth = async ({
  appId,
  redirectUri,
  scope = 'email phone',
  storageKey = DEFAULT_STORAGE_KEY,
}: StartVKPKCEAuthOptions) => {
  const authBaseUrl = import.meta.env.VITE_VK_AUTH_URL || 'https://id.vk.com/authorize';
  const codeVerifier = generateCodeVerifier();
  const codeChallenge = await generateCodeChallenge(codeVerifier);
  const state = generateRandomString(32, STATE_CHARSET);
  const nonce = generateRandomString(16, STATE_CHARSET);
  const deviceId = getOrCreateDeviceId();

  persistPKCEPayload(storageKey, state, {
    code_verifier: codeVerifier,
    state,
    nonce,
    device_id: deviceId,
    ts: Date.now(),
  });

  const authUrl = new URL(authBaseUrl);
  authUrl.searchParams.set('response_type', 'code');
  authUrl.searchParams.set('client_id', appId);
  authUrl.searchParams.set('redirect_uri', redirectUri);
  authUrl.searchParams.set('scope', scope);
  authUrl.searchParams.set('state', state);
  authUrl.searchParams.set('nonce', nonce);
  authUrl.searchParams.set('code_challenge', codeChallenge);
  authUrl.searchParams.set('code_challenge_method', 'S256');
  authUrl.searchParams.set('device_id', deviceId);

  window.location.href = authUrl.toString();
};
