/**
 * Страница редактирования изображений через AI-чат
 * Интерактивный чат с AI-ассистентом для редактирования изображений
 */

import React, { useEffect } from 'react';
import { ChatWindow } from '../components/editing/ChatWindow';
import { ChatInput } from '../components/editing/ChatInput';
import { FileUpload } from '../components/common/FileUpload';
import { useAuthStore } from '../store/authStore';
import { useChatStore } from '../store/chatStore';
import { AuthGuard } from '../components/auth/AuthGuard';
import toast from 'react-hot-toast';

export const EditingPage: React.FC = () => {
  const { user } = useAuthStore();
  const {
    sessionId,
    baseImage,
    messages,
    currentPrompts,
    isSendingMessage,
    isGenerating,
    uploadAndCreateSession,
    sendMessage,
    generateImage,
    resetSession,
    uploadError,
    error,
    clearError,
  } = useChatStore();

  const [isUploadingImage, setIsUploadingImage] = React.useState(false);
  const [showResetConfirm, setShowResetConfirm] = React.useState(false);

  // Сброс состояния при монтировании страницы
  useEffect(() => {
    // Не сбрасываем, если есть активная сессия (пользователь мог вернуться назад)
    // reset();
  }, []);

  // Обработка ошибок
  useEffect(() => {
    if (uploadError) {
      toast.error(uploadError);
      clearError();
    }
    if (error) {
      toast.error(error);
      clearError();
    }
  }, [uploadError, error, clearError]);

  const handleFileSelect = async (file: File) => {
    setIsUploadingImage(true);
    clearError();

    try {
      await uploadAndCreateSession(file);
      toast.success('Изображение загружено! Начните беседу с AI-ассистентом.');
    } catch (err: any) {
      toast.error(err.message || 'Ошибка загрузки изображения');
    } finally {
      setIsUploadingImage(false);
    }
  };

  const handleSendMessage = async (text: string) => {
    try {
      await sendMessage(text);
    } catch (err: any) {
      toast.error(err.message || 'Ошибка отправки сообщения');
    }
  };

  const handleSelectPrompt = async (prompt: string) => {
    try {
      await generateImage(prompt);
      toast.success('Изображение сгенерировано!');
    } catch (err: any) {
      toast.error(err.message || 'Ошибка генерации изображения');
    }
  };

  const handleResetSession = async () => {
    try {
      await resetSession();
      toast.success('Чат сброшен');
      setShowResetConfirm(false);
    } catch (err: any) {
      toast.error(err.message || 'Ошибка сброса чата');
    }
  };

  const hasActiveSession = sessionId && baseImage;

  return (
    <AuthGuard>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
          <div className="max-w-4xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  Редактирование изображений
                </h1>
                <p className="text-sm text-gray-600">
                  AI-ассистент для редактирования фото
                </p>
              </div>
              <div className="flex items-center space-x-4">
                {user && (
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-700">
                      {user.balance_credits} кредитов
                    </p>
                    {user.subscription_type && user.subscription_type !== 'none' && (
                      <span className="text-xs text-blue-600">
                        {user.subscription_type}
                      </span>
                    )}
                  </div>
                )}
                {hasActiveSession && (
                  <button
                    onClick={() => setShowResetConfirm(true)}
                    className="text-sm text-red-600 hover:text-red-700 font-medium"
                    title="Сбросить чат и начать заново"
                  >
                    Сбросить чат
                  </button>
                )}
              </div>
            </div>
          </div>
        </header>

        {/* Main content */}
        {!hasActiveSession ? (
          // Upload screen
          <main className="flex-1 flex items-center justify-center px-4 py-12">
            <div className="max-w-2xl w-full">
              <div className="mb-8 text-center">
                <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full mb-4">
                  <svg
                    className="w-10 h-10 text-white"
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
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                  Загрузите изображение
                </h2>
                <p className="text-gray-600">
                  Выберите фотографию, которую хотите отредактировать с помощью AI
                </p>
              </div>

              <FileUpload
                onFileSelect={handleFileSelect}
                isLoading={isUploadingImage}
                error={uploadError}
                label="Базовое изображение"
                hint="JPEG или PNG, до 5MB"
              />

              {/* Info cards */}
              <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-white p-4 rounded-lg border border-gray-200">
                  <div className="flex items-start">
                    <div className="flex-shrink-0">
                      <svg
                        className="w-6 h-6 text-blue-600"
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
                    <div className="ml-3">
                      <h3 className="text-sm font-semibold text-gray-900 mb-1">
                        AI-ассистент
                      </h3>
                      <p className="text-sm text-gray-600">
                        Опишите изменения естественным языком. AI предложит варианты промптов.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="bg-white p-4 rounded-lg border border-gray-200">
                  <div className="flex items-start">
                    <div className="flex-shrink-0">
                      <svg
                        className="w-6 h-6 text-green-600"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <h3 className="text-sm font-semibold text-gray-900 mb-1">
                        Прозрачная оплата
                      </h3>
                      <p className="text-sm text-gray-600">
                        1 кредит за сообщение AI, 1 кредит за генерацию изображения.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </main>
        ) : (
          // Chat screen
          <>
            <ChatWindow
              messages={messages}
              currentPrompts={currentPrompts}
              onSelectPrompt={handleSelectPrompt}
              isGenerating={isGenerating}
              baseImageUrl={baseImage?.url}
            />

            <ChatInput
              onSend={handleSendMessage}
              disabled={isSendingMessage || isGenerating}
              placeholder="Опишите, как хотите изменить изображение..."
            />
          </>
        )}

        {/* Reset confirmation modal */}
        {showResetConfirm && (
          <div
            className="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center p-4"
            onClick={() => setShowResetConfirm(false)}
          >
            <div
              className="bg-white rounded-2xl p-6 max-w-sm w-full shadow-xl"
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                Сбросить чат?
              </h3>
              <p className="text-sm text-gray-600 mb-6">
                Вся история беседы будет удалена. Это действие нельзя отменить.
              </p>
              <div className="flex space-x-3">
                <button
                  onClick={() => setShowResetConfirm(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Отмена
                </button>
                <button
                  onClick={handleResetSession}
                  className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                  Сбросить
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </AuthGuard>
  );
};
