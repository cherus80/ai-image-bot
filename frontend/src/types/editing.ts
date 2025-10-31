/**
 * TypeScript типы для редактирования изображений
 * Соответствуют backend схемам из app/schemas/editing.py
 */

// Роли сообщений в чате
export type MessageRole = 'user' | 'assistant';

// Запрос на создание сессии чата
export interface ChatSessionCreate {
  base_image_url: string;
}

// Ответ с созданной сессией
export interface ChatSessionResponse {
  session_id: string; // UUID
  base_image_url: string;
  created_at: string;
}

// Запрос на отправку сообщения
export interface ChatMessageRequest {
  session_id: string;
  message: string;
}

// Ответ от AI-ассистента
export interface ChatMessageResponse {
  role: MessageRole;
  content: string;
  prompts?: string[]; // 3 варианта промптов от AI
  timestamp: string;
}

// Запрос на генерацию изображения
export interface GenerateImageRequest {
  session_id: string;
  prompt: string;
}

// Ответ при запуске генерации
export interface GenerateImageResponse {
  task_id: string;
  status: string;
  message: string;
}

// Сообщение из истории чата
export interface ChatHistoryMessage {
  role: MessageRole;
  content: string;
  image_url?: string; // URL сгенерированного изображения (если есть)
  timestamp: string;
}

// Ответ с историей чата
export interface ChatHistoryResponse {
  session_id: string;
  base_image_url?: string;
  messages: ChatHistoryMessage[];
  message_count: number;
  is_active: boolean;
}

// Ответ на сброс сессии
export interface ResetSessionResponse {
  session_id: string;
  message: string;
}

// Ошибка API
export interface EditingError {
  detail: string;
  error_code?: string;
}

// Локальное состояние сообщения (для UI)
export interface ChatMessage {
  id: string; // Локальный ID для React keys
  role: MessageRole;
  content: string;
  image_url?: string;
  prompts?: string[]; // Промпты от AI (только для assistant)
  timestamp: Date;
  isLoading?: boolean; // Индикатор загрузки
}

// Состояние загрузки базового изображения
export interface BaseImageUpload {
  file_id: string;
  url: string;
  preview: string; // data URL для превью
  file: File;
}
