/**
 * Компонент окна чата с автоматическим скроллингом
 * Контейнер для всех сообщений
 */

import React from 'react';
import { ChatMessage } from './ChatMessage';
import { ImageMessage } from './ImageMessage';
import { PromptSelector } from './PromptSelector';
import type { ChatMessage as ChatMessageType } from '../../types/editing';

interface ChatWindowProps {
  messages: ChatMessageType[];
  currentPrompts: string[] | null;
  onSelectPrompt: (prompt: string) => void;
  isGenerating?: boolean;
  baseImageUrl?: string;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({
  messages,
  currentPrompts,
  onSelectPrompt,
  isGenerating = false,
  baseImageUrl,
}) => {
  const messagesEndRef = React.useRef<HTMLDivElement>(null);
  const containerRef = React.useRef<HTMLDivElement>(null);

  // Автоматический scroll вниз при новых сообщениях
  React.useEffect(() => {
    scrollToBottom();
  }, [messages, currentPrompts]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Показываем базовое изображение в начале чата
  const shouldShowBaseImage = baseImageUrl && messages.length === 0;

  return (
    <div
      ref={containerRef}
      className="flex-1 overflow-y-auto px-4 py-6 bg-gray-50"
      style={{ maxHeight: 'calc(100vh - 200px)' }}
    >
      <div className="max-w-4xl mx-auto">
        {/* Базовое изображение */}
        {shouldShowBaseImage && (
          <div className="mb-6 animate-fade-in">
            <div className="bg-white border border-gray-200 rounded-2xl p-4 shadow-sm">
              <div className="flex items-center mb-3">
                <div className="w-6 h-6 bg-gradient-to-br from-green-500 to-blue-500 rounded-full flex items-center justify-center mr-2">
                  <svg
                    className="w-4 h-4 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                    />
                  </svg>
                </div>
                <span className="text-sm font-semibold text-gray-700">
                  Базовое изображение
                </span>
              </div>
              <img
                src={baseImageUrl}
                alt="Base image"
                className="w-full h-auto rounded-lg"
              />
              <p className="mt-3 text-sm text-gray-600">
                Опишите, как хотите изменить это изображение. AI-ассистент предложит вам несколько вариантов промптов на выбор.
              </p>
            </div>
          </div>
        )}

        {/* Приветственное сообщение */}
        {messages.length === 0 && (
          <div className="text-center py-12 animate-fade-in">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full mb-4">
              <svg
                className="w-8 h-8 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              Начните беседу с AI-ассистентом
            </h3>
            <p className="text-gray-600 max-w-md mx-auto">
              Опишите, как хотите изменить изображение. Например:
              "Измени фон на закат", "Добавь эффект черно-белого фото", "Сделай изображение ярче"
            </p>
          </div>
        )}

        {/* Сообщения */}
        {messages.map((message) => (
          <React.Fragment key={message.id}>
            {message.image_url ? (
              <ImageMessage message={message} />
            ) : (
              <ChatMessage message={message} />
            )}
            {/* Показываем промпты после сообщения ассистента */}
            {message.role === 'assistant' &&
              message.prompts &&
              message.prompts.length > 0 &&
              !message.image_url && (
                <PromptSelector
                  prompts={message.prompts}
                  onSelect={onSelectPrompt}
                  isGenerating={isGenerating}
                />
              )}
          </React.Fragment>
        ))}

        {/* Индикатор генерации */}
        {isGenerating && (
          <div className="flex justify-center my-4 animate-fade-in">
            <div className="flex items-center space-x-2 px-4 py-2 bg-blue-50 border border-blue-200 rounded-full">
              <svg
                className="w-5 h-5 text-blue-600 animate-spin"
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
              <span className="text-sm font-medium text-blue-700">
                Генерируем изображение...
              </span>
            </div>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
};
