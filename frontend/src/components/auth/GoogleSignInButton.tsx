/**
 * Компонент кнопки Google входа
 *
 * Отображает официальную кнопку Google и обрабатывает OAuth flow
 */

import { useEffect, useRef, useState } from 'react';
import { useAuth } from '../../store/authStore';
import type { GoogleSignInResponse, GoogleSignInButtonConfig } from '../../types/auth';

interface GoogleSignInButtonProps {
  onSuccess?: () => void;
  onError?: (error: string) => void;
  text?: 'signin_with' | 'signup_with' | 'continue_with';
  theme?: 'outline' | 'filled_blue' | 'filled_black';
  size?: 'large' | 'medium' | 'small';
  width?: number;
  shape?: GoogleSignInButtonConfig['shape'];
  className?: string;
}

export function GoogleSignInButton({
  onSuccess,
  onError,
  text = 'continue_with',
  theme = 'outline',
  size = 'large',
  shape = 'pill',
  width,
  className,
}: GoogleSignInButtonProps) {
  const buttonRef = useRef<HTMLDivElement>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isReady, setIsReady] = useState<boolean>(Boolean(window.google?.accounts?.id));
  const { loginWithGoogle } = useAuth();

  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

  const ensureScriptLoaded = () => {
    if (window.google?.accounts?.id) return Promise.resolve(true);
    return new Promise<boolean>((resolve) => {
      const existing = document.querySelector<HTMLScriptElement>('script[data-gis-sdk]');
      if (existing && (existing as any)._gisReady) {
        resolve(true);
        return;
      }
      const script = existing || document.createElement('script');
      script.src = 'https://accounts.google.com/gsi/client';
      script.async = true;
      script.defer = true;
      script.dataset.gisSdk = '1';
      (script as any)._gisReady = false;
      script.onload = () => {
        (script as any)._gisReady = true;
        resolve(true);
      };
      script.onerror = () => resolve(false);
      if (!existing) document.head.appendChild(script);
    });
  };

  useEffect(() => {
    // Проверка, настроен ли client ID
    if (!clientId) {
      console.error('Google Client ID не настроен. Установите VITE_GOOGLE_CLIENT_ID в .env');
      onError?.('Google вход не настроен');
      return;
    }

    let cancelled = false;

    const init = async () => {
      const loaded = await ensureScriptLoaded();
      if (!loaded || cancelled || !window.google?.accounts?.id) {
        console.error('Google Identity Services не удалось загрузить');
        onError?.('Google вход недоступен');
        return;
      }

      try {
        window.google.accounts.id.initialize({
          client_id: clientId,
          callback: handleCredentialResponse,
          auto_select: false,
          cancel_on_tap_outside: true,
        });

        if (buttonRef.current) {
          buttonRef.current.innerHTML = '';
          buttonRef.current.style.height = '48px';
          buttonRef.current.style.minHeight = '48px';
          buttonRef.current.style.maxHeight = '48px';
          buttonRef.current.style.width = '100%';

          const config: GoogleSignInButtonConfig = {
            type: 'standard',
            theme,
            size,
            text,
            shape,
            logo_alignment: 'left',
            width,
          };

          window.google.accounts.id.renderButton(buttonRef.current, config);

          const renderedButton = buttonRef.current.querySelector('div[role="button"]') as HTMLDivElement | null;
          if (renderedButton) {
            renderedButton.style.width = '100%';
            renderedButton.style.maxWidth = '100%';
            renderedButton.style.minHeight = '48px';
            renderedButton.style.height = '48px';
            renderedButton.style.borderRadius = '12px';
            renderedButton.style.boxShadow = '0 1px 3px rgba(0,0,0,0.08)';
            renderedButton.style.background = '#ffffff';
            renderedButton.style.color = '#0f172a';
            renderedButton.style.border = '1px solid rgb(226 232 240)';
            renderedButton.style.fontWeight = '700';
            renderedButton.style.letterSpacing = '0.01em';
            renderedButton.style.display = 'flex';
            renderedButton.style.alignItems = 'center';

            const label = renderedButton.querySelector('span');
            if (label) {
              label.style.color = '#0f172a';
              label.style.fontWeight = '700';
            }
          }
        }
        setIsReady(true);
      } catch (error) {
        console.error('Ошибка инициализации Google входа:', error);
        onError?.('Google вход недоступен');
      }
    };

    init();

    return () => {
      cancelled = true;
    };
  }, [clientId, theme, size, text, width, shape]);

  const handleCredentialResponse = async (response: GoogleSignInResponse) => {
    setIsLoading(true);

    try {
      // Отправка ID токена на backend
      await loginWithGoogle(response.credential);

      // Успех
      onSuccess?.();
    } catch (error: any) {
      console.error('Ошибка Google входа:', error);
      const errorMessage =
        error.response?.data?.detail || error.message || 'Google вход не удался';
      onError?.(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // Показать состояние загрузки или заглушку, если Google не загружен или нет client ID
  if (!clientId) {
    return (
      <div className="flex items-center justify-center p-3 border border-gray-300 rounded-md bg-gray-50">
        <span className="text-sm text-gray-500">Google вход не настроен</span>
      </div>
    );
  }

  if (!isReady) {
    return (
      <div className="flex items-center justify-center p-3 h-12 min-h-[48px] max-h-[48px] border border-gray-200 rounded-lg bg-white shadow-sm">
        <span className="text-sm text-gray-500">Загрузка Google входа...</span>
      </div>
    );
  }

  return (
    <div
      className={`relative h-12 min-h-[48px] max-h-[48px] w-full ${className || ''}`}
    >
      {/* Здесь будет отрисована кнопка Google */}
      <div
        ref={buttonRef}
        className={`h-full flex items-stretch justify-center ${isLoading ? 'opacity-50 pointer-events-none' : ''}`}
      />

      {/* Оверлей загрузки */}
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75">
          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600"></div>
        </div>
      )}
    </div>
  );
}
