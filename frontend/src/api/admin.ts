/**
 * API клиент для админки.
 *
 * Все запросы требуют заголовок X-Admin-Secret.
 */

import apiClient from './client';
import type {
  AdminStats,
  AdminChartsData,
  AdminUsersResponse,
  AdminUsersRequest,
  PaymentExportResponse,
  PaymentExportRequest,
} from '../types/admin';

// ============================================================================
// Конфигурация
// ============================================================================

/**
 * Получить ADMIN_SECRET_KEY из локального хранилища или переменных окружения.
 */
export const getAdminSecret = (): string | null => {
  // Сначала проверяем localStorage (для сохранённого ключа)
  const savedSecret = localStorage.getItem('admin_secret_key');
  if (savedSecret) {
    return savedSecret;
  }

  // Fallback на переменную окружения (для development)
  return import.meta.env.VITE_ADMIN_SECRET_KEY || null;
};

/**
 * Сохранить ADMIN_SECRET_KEY в localStorage.
 */
export const setAdminSecret = (secret: string): void => {
  localStorage.setItem('admin_secret_key', secret);
};

/**
 * Удалить ADMIN_SECRET_KEY из localStorage.
 */
export const clearAdminSecret = (): void => {
  localStorage.removeItem('admin_secret_key');
};

/**
 * Проверить, установлен ли ADMIN_SECRET_KEY.
 */
export const hasAdminSecret = (): boolean => {
  return getAdminSecret() !== null;
};

// ============================================================================
// Вспомогательные функции
// ============================================================================

/**
 * Создать заголовки с X-Admin-Secret.
 */
const createAdminHeaders = (): Record<string, string> => {
  const secret = getAdminSecret();
  if (!secret) {
    throw new Error('Admin secret key is not set. Please set it using setAdminSecret().');
  }

  return {
    'X-Admin-Secret': secret,
  };
};

// ============================================================================
// API запросы
// ============================================================================

/**
 * Получить общую статистику приложения.
 */
export const getAdminStats = async (): Promise<AdminStats> => {
  const response = await apiClient.get<AdminStats>('/api/v1/admin/stats', {
    headers: createAdminHeaders(),
  });
  return response.data;
};

/**
 * Получить данные для графиков (последние 30 дней).
 */
export const getAdminCharts = async (): Promise<AdminChartsData> => {
  const response = await apiClient.get<AdminChartsData>('/api/v1/admin/charts', {
    headers: createAdminHeaders(),
  });
  return response.data;
};

/**
 * Получить список пользователей с фильтрацией и пагинацией.
 */
export const getAdminUsers = async (params?: AdminUsersRequest): Promise<AdminUsersResponse> => {
  const response = await apiClient.get<AdminUsersResponse>('/api/v1/admin/users', {
    headers: createAdminHeaders(),
    params: params || {},
  });
  return response.data;
};

/**
 * Экспортировать платежи в JSON.
 */
export const exportPaymentsJSON = async (params?: PaymentExportRequest): Promise<PaymentExportResponse> => {
  const response = await apiClient.get<PaymentExportResponse>('/api/v1/admin/payments/export', {
    headers: createAdminHeaders(),
    params: {
      ...params,
      format: 'json',
    },
  });
  return response.data;
};

/**
 * Экспортировать платежи в CSV и скачать файл.
 */
export const exportPaymentsCSV = async (params?: PaymentExportRequest): Promise<void> => {
  const response = await apiClient.get('/api/v1/admin/payments/export', {
    headers: createAdminHeaders(),
    params: {
      ...params,
      format: 'csv',
    },
    responseType: 'blob',
  });

  // Создаём ссылку для скачивания
  const blob = new Blob([response.data], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;

  // Получаем имя файла из заголовка Content-Disposition или генерируем
  const contentDisposition = response.headers['content-disposition'];
  let filename = 'payments_export.csv';
  if (contentDisposition) {
    const filenameMatch = contentDisposition.match(/filename="?(.+)"?/);
    if (filenameMatch) {
      filename = filenameMatch[1];
    }
  }

  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};

// ============================================================================
// Вспомогательные функции для форматирования
// ============================================================================

/**
 * Форматировать число с разделителями тысяч.
 */
export const formatNumber = (value: number | string): string => {
  const num = typeof value === 'string' ? parseFloat(value) : value;
  return new Intl.NumberFormat('ru-RU').format(num);
};

/**
 * Форматировать валюту (рубли).
 */
export const formatCurrency = (value: number | string): string => {
  const num = typeof value === 'string' ? parseFloat(value) : value;
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(num);
};

/**
 * Форматировать дату.
 */
export const formatDate = (dateString: string | null): string => {
  if (!dateString) return '—';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
};

/**
 * Форматировать относительное время (например, "2 дня назад").
 */
export const formatRelativeTime = (dateString: string | null): string => {
  if (!dateString) return '—';
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMinutes = Math.floor(diffMs / (1000 * 60));
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffMinutes < 1) return 'только что';
  if (diffMinutes < 60) return `${diffMinutes} мин. назад`;
  if (diffHours < 24) return `${diffHours} ч. назад`;
  if (diffDays < 30) return `${diffDays} дн. назад`;
  return formatDate(dateString);
};

/**
 * Вычислить процент изменения между двумя значениями.
 */
export const calculatePercentChange = (current: number, previous: number): number => {
  if (previous === 0) return current > 0 ? 100 : 0;
  return ((current - previous) / previous) * 100;
};
