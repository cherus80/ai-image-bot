const PD_CONSENT_STORAGE_KEY = 'pd-consent-version';

export const getStoredPdConsentVersion = (): string | null => {
  if (typeof window === 'undefined') {
    return null;
  }
  try {
    return localStorage.getItem(PD_CONSENT_STORAGE_KEY);
  } catch (error) {
    console.error('Failed to read PD consent version:', error);
    return null;
  }
};

export const setStoredPdConsentVersion = (version: string | null) => {
  if (typeof window === 'undefined') {
    return;
  }
  try {
    if (version) {
      localStorage.setItem(PD_CONSENT_STORAGE_KEY, version);
    } else {
      localStorage.removeItem(PD_CONSENT_STORAGE_KEY);
    }
  } catch (error) {
    console.error('Failed to store PD consent version:', error);
  }
};
