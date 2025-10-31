/**
 * Компонент выбора промпта из 3 вариантов, предложенных AI
 * Отображает карточки с разными уровнями детализации
 */

import React from 'react';

interface PromptSelectorProps {
  prompts: string[];
  onSelect: (prompt: string) => void;
  isGenerating?: boolean;
}

export const PromptSelector: React.FC<PromptSelectorProps> = ({
  prompts,
  onSelect,
  isGenerating = false,
}) => {
  const [selectedPrompt, setSelectedPrompt] = React.useState<string | null>(null);
  const [editingPrompt, setEditingPrompt] = React.useState<string | null>(null);
  const [customPrompt, setCustomPrompt] = React.useState<string>('');

  if (prompts.length === 0) {
    return null;
  }

  const handleSelect = (prompt: string) => {
    setSelectedPrompt(prompt);
    onSelect(prompt);
  };

  const handleEdit = (prompt: string) => {
    setEditingPrompt(prompt);
    setCustomPrompt(prompt);
  };

  const handleSaveEdit = () => {
    if (customPrompt.trim()) {
      handleSelect(customPrompt.trim());
      setEditingPrompt(null);
      setCustomPrompt('');
    }
  };

  const handleCancelEdit = () => {
    setEditingPrompt(null);
    setCustomPrompt('');
  };

  const promptLabels = [
    { label: 'Короткий', icon: '⚡', color: 'blue' },
    { label: 'Средний', icon: '✨', color: 'purple' },
    { label: 'Детальный', icon: '🎨', color: 'pink' },
  ];

  return (
    <div className="my-4 animate-fade-in">
      <div className="flex items-center mb-3">
        <div className="w-6 h-6 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center mr-2">
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
              d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
            />
          </svg>
        </div>
        <p className="text-sm font-semibold text-gray-700">
          Выберите вариант промпта для генерации:
        </p>
      </div>

      <div className="grid grid-cols-1 gap-3">
        {prompts.slice(0, 3).map((prompt, index) => {
          const { label, icon, color } = promptLabels[index] || promptLabels[0];
          const isEditing = editingPrompt === prompt;
          const isSelected = selectedPrompt === prompt;

          return (
            <div
              key={index}
              className={`border-2 rounded-xl p-4 transition-all ${
                isSelected
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300 bg-white'
              }`}
            >
              {/* Header */}
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center">
                  <span className="text-xl mr-2">{icon}</span>
                  <span className={`text-sm font-semibold text-${color}-600`}>
                    {label}
                  </span>
                </div>
                <div className="flex items-center space-x-2">
                  {!isEditing && (
                    <button
                      onClick={() => handleEdit(prompt)}
                      disabled={isGenerating}
                      className="text-xs text-gray-500 hover:text-gray-700 disabled:opacity-50"
                      title="Редактировать промпт"
                    >
                      ✏️ Изменить
                    </button>
                  )}
                </div>
              </div>

              {/* Prompt text or edit field */}
              {isEditing ? (
                <div>
                  <textarea
                    value={customPrompt}
                    onChange={(e) => setCustomPrompt(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                  />
                  <div className="mt-2 flex justify-end space-x-2">
                    <button
                      onClick={handleCancelEdit}
                      className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
                    >
                      Отмена
                    </button>
                    <button
                      onClick={handleSaveEdit}
                      disabled={!customPrompt.trim()}
                      className="px-3 py-1 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
                    >
                      Генерировать
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <p className="text-sm text-gray-700 mb-3 line-clamp-3">
                    {prompt}
                  </p>

                  {/* Generate button */}
                  <button
                    onClick={() => handleSelect(prompt)}
                    disabled={isGenerating}
                    className={`w-full py-2 px-4 rounded-lg font-medium text-sm transition-all ${
                      isGenerating
                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        : 'bg-blue-600 text-white hover:bg-blue-700'
                    }`}
                  >
                    {isGenerating && isSelected ? (
                      <span className="flex items-center justify-center">
                        <svg
                          className="w-4 h-4 mr-2 animate-spin"
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
                        Генерируем...
                      </span>
                    ) : (
                      'Генерировать изображение'
                    )}
                  </button>
                </>
              )}
            </div>
          );
        })}
      </div>

      {/* Info hint */}
      <div className="mt-3 text-xs text-gray-500 flex items-start">
        <svg
          className="w-4 h-4 mr-1 mt-0.5 flex-shrink-0"
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
            clipRule="evenodd"
          />
        </svg>
        <span>
          Генерация изображения списывает 1 кредит. Вы можете изменить промпт перед генерацией.
        </span>
      </div>
    </div>
  );
};
