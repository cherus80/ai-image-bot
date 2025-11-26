/**
 * Компонент кнопки VK входа
 *
 * Отображает официальную кнопку VK ID и обрабатывает OAuth flow
 */

import { useEffect, useRef, useState } from 'react';
import { useAuth } from '../../store/authStore';
import type { VKIDAuthResponse } from '../../types/auth';

interface VKSignInButtonProps {
  onSuccess?: () => void;
  onError?: (error: string) => void;
}

export function VKSignInButton({ onSuccess, onError }: VKSignInButtonProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const buttonInstanceRef = useRef<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [sdkError, setSdkError] = useState<string | null>(null);
  const { loginWithVK } = useAuth();

  const appId = import.meta.env.VITE_VK_APP_ID;

  useEffect(() => {
    // Проверка, настроен ли VK App ID
    if (!appId) {
      console.error('VK App ID не настроен. Установите VITE_VK_APP_ID в .env');
      setSdkError('VK вход не настроен');
      onError?.('VK вход не настроен');
      return;
    }

    // Ожидание загрузки VK ID SDK
    const initializeVK = () => {
      if (!window.VKID) {
        console.warn('VK ID SDK ещё не загружен, повторная попытка...');
        return false;
      }

      try {
        // Инициализация VK ID SDK
        window.VKID.Config.init({
          app: appId,
          redirectUrl: window.location.origin,
        });

        // Создание кнопки VK ID
        if (containerRef.current && !buttonInstanceRef.current) {
          const button = new window.VKID.FloatingOneTapButton(containerRef.current);

          // Обработка успешного входа
          button.on('success', handleVKAuthResponse);

          // Отрисовка кнопки
          button.render();

          // Сохранение ссылки на кнопку для очистки
          buttonInstanceRef.current = button;
        }

        return true;
      } catch (error) {
        console.error('Ошибка инициализации VK ID SDK:', error);
        setSdkError('Ошибка загрузки VK входа');
        return false;
      }
    };

    // Попытка инициализации сразу
    if (initializeVK()) {
      return;
    }

    // Если не загружен, повторять с интервалом
    let retryCount = 0;
    const maxRetries = 10;
    const retryInterval = 500; // 500ms

    const intervalId = setInterval(() => {
      retryCount++;

      if (initializeVK()) {
        clearInterval(intervalId);
      } else if (retryCount >= maxRetries) {
        clearInterval(intervalId);
        console.error('VK ID SDK не удалось загрузить после нескольких попыток');
        setSdkError('VK вход недоступен');
        onError?.('VK вход недоступен');
      }
    }, retryInterval);

    // Cleanup
    return () => {
      clearInterval(intervalId);
      if (buttonInstanceRef.current) {
        try {
          buttonInstanceRef.current.destroy();
          buttonInstanceRef.current = null;
        } catch (error) {
          console.error('Ошибка при очистке VK ID кнопки:', error);
        }
      }
    };
  }, [appId]);

  const handleVKAuthResponse = async (response: VKIDAuthResponse) => {
    setIsLoading(true);

    try {
      // Отправка silent token и UUID на backend
      await loginWithVK(response.token, response.uuid);

      // Успех
      onSuccess?.();
    } catch (error: any) {
      console.error('Ошибка VK входа:', error);
      const errorMessage =
        error.response?.data?.detail || error.message || 'VK вход не удался';
      onError?.(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // Показать ошибку, если VK App ID не настроен или SDK не загружен
  if (!appId || sdkError) {
    return (
      <div className="flex items-center justify-center p-3 border border-gray-300 rounded-md bg-gray-50">
        <span className="text-sm text-gray-500">
          {sdkError || 'VK вход не настроен'}
        </span>
      </div>
    );
  }

  if (!window.VKID && !sdkError) {
    return (
      <div className="flex items-center justify-center p-3 border border-gray-300 rounded-md bg-gray-50">
        <span className="text-sm text-gray-500">Загрузка VK входа...</span>
      </div>
    );
  }

  return (
    <div className="relative">
      {/* Контейнер для кнопки VK ID */}
      <div
        ref={containerRef}
        className={isLoading ? 'opacity-50 pointer-events-none' : ''}
        style={{ minHeight: '44px' }}
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
