/**
 * Компонент ввода сообщения в чат
 * Textarea с автоматическим ростом и кнопкой отправки
 */

import React from 'react';
import { useAuthStore } from '../../store/authStore';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSend,
  disabled = false,
  placeholder = 'Опишите, как хотите изменить изображение...',
}) => {
  const [message, setMessage] = React.useState('');
  const textareaRef = React.useRef<HTMLTextAreaElement>(null);
  const { user } = useAuthStore();

  // Автоматическая подстройка высоты textarea
  React.useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  const handleSubmit = () => {
    const trimmedMessage = message.trim();
    if (!trimmedMessage || disabled) {
      return;
    }

    onSend(trimmedMessage);
    setMessage('');

    // Сброс высоты textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Enter без Shift - отправка сообщения
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="border-t border-gray-200 bg-white px-4 py-4">
      <div className="max-w-4xl mx-auto flex items-end space-x-3">
        {/* Textarea */}
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={disabled}
            rows={1}
            className="w-full px-4 py-3 border border-gray-300 rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed transition-all"
            style={{ maxHeight: '200px' }}
          />
          {/* Hint text */}
          <div className="absolute right-3 bottom-2 text-xs text-gray-400">
            Enter для отправки
          </div>
        </div>

        {/* Send button */}
        <button
          onClick={handleSubmit}
          disabled={!message.trim() || disabled}
          className="flex-shrink-0 p-3 bg-blue-600 text-white rounded-full hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          title="Отправить сообщение"
        >
          {disabled ? (
            // Loading spinner
            <svg
              className="w-6 h-6 animate-spin"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
          ) : (
            // Send icon
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
              />
            </svg>
          )}
        </button>
      </div>

      {/* Balance and Freemium info */}
      {user && (
        <div className="max-w-4xl mx-auto mt-2 flex items-center justify-between text-xs">
          <div className="flex items-center space-x-4 text-gray-600">
            <span>
              Баланс: <span className="font-semibold">{user.balance_credits}</span> кредитов
            </span>
            {user.subscription_type && user.subscription_type !== 'none' && (
              <span className="text-blue-600">
                + подписка ({user.subscription_type})
              </span>
            )}
            {user.freemium_actions_remaining && user.freemium_actions_remaining > 0 && (
              <span className="text-green-600">
                + {user.freemium_actions_remaining} бесплатных
              </span>
            )}
          </div>
          {message.length > 1500 && (
            <div className="text-gray-500">
              {message.length} / 2000 символов
            </div>
          )}
        </div>
      )}
    </div>
  );
};
