/**
 * Zustand store для генерации по образцу без истории
 */

import { create } from 'zustand';
import type { ChatAttachment } from '../types/editing';
import type { FittingStatusResponse, FittingResult, GenerationStatus } from '../types/fitting';
import { generateExampleImage, pollEditingStatus } from '../api/editing';
import { useAuthStore } from './authStore';
import toast from 'react-hot-toast';

interface ExampleGenerationState {
  isGenerating: boolean;
  taskIds: string[];
  generationStatus: GenerationStatus | null;
  progress: number;
  progressByTask: Record<string, number>;
  statusMessage: string | null;
  results: FittingResult[];
  error: string | null;

  startGeneration: (prompt: string, attachments: ChatAttachment[]) => Promise<FittingResult[]>;
  reset: () => void;
  updateProgress: (taskId: string, status: FittingStatusResponse) => void;
}

export const useExampleGenerationStore = create<ExampleGenerationState>((set, get) => ({
  isGenerating: false,
  taskIds: [],
  generationStatus: null,
  progress: 0,
  progressByTask: {},
  statusMessage: null,
  results: [],
  error: null,

  startGeneration: async (prompt: string, attachments: ChatAttachment[]) => {
    const trimmedPrompt = prompt.trim();
    if (!trimmedPrompt) {
      throw new Error('Промпт не может быть пустым');
    }
    if (!attachments || attachments.length === 0) {
      throw new Error('Необходимо прикрепить хотя бы одно фото');
    }

    set({
      isGenerating: true,
      error: null,
      progress: 0,
      progressByTask: {},
      statusMessage: 'Запускаем генерацию...',
      results: [],
    });

    try {
      const response = await generateExampleImage({
        prompt: trimmedPrompt,
        attachments,
      });

      const taskIds = response.task_ids || [];
      if (taskIds.length === 0) {
        throw new Error('Не удалось запустить генерацию');
      }
      const progressByTask: Record<string, number> = {};
      taskIds.forEach((taskId) => {
        progressByTask[taskId] = 0;
      });

      set({
        taskIds,
        generationStatus: response.status as GenerationStatus,
        statusMessage: response.message,
        progressByTask,
      });

      const results = await Promise.all(
        taskIds.map(async (taskId) => {
          try {
            return await pollEditingStatus(
              taskId,
              (status) => {
                get().updateProgress(taskId, status);
              },
              {
                slowWarningMs: 60000,
                onSlowWarning: () =>
                  toast(
                    'Генерация может занять до 3 минут из-за нагрузки на сервис. Приложение продолжает ждать ответ.',
                    { icon: '⏳' }
                  ),
              }
            );
          } catch (pollError: any) {
            return {
              task_id: taskId,
              status: 'failed',
              error_message: pollError?.message || 'Ошибка генерации',
              has_watermark: false,
              credits_spent: 0,
              created_at: new Date().toISOString(),
            } as FittingResult;
          }
        })
      );

      const hasFailures = results.some((item) => item.status === 'failed');

      set({
        results,
        isGenerating: false,
        generationStatus: hasFailures ? 'failed' : 'completed',
        progress: 100,
        statusMessage: hasFailures ? 'Произошла ошибка' : 'Готово!',
      });

      await useAuthStore.getState().refreshProfile();

      return results;
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Ошибка генерации';
      set({
        isGenerating: false,
        error: errorMessage,
        statusMessage: 'Ошибка',
        progress: 0,
      });
      throw error;
    }
  },

  updateProgress: (taskId: string, status: FittingStatusResponse) => {
    set((state) => {
      const nextProgressByTask = { ...state.progressByTask, [taskId]: status.progress };
      const progressValues = Object.values(nextProgressByTask);
      const avgProgress = progressValues.length
        ? progressValues.reduce((sum, value) => sum + value, 0) / progressValues.length
        : 0;
      return {
        generationStatus: status.status,
        progress: avgProgress,
        statusMessage: status.message,
        progressByTask: nextProgressByTask,
      };
    });
  },

  reset: () => {
    set({
      isGenerating: false,
      taskIds: [],
      generationStatus: null,
      progress: 0,
      progressByTask: {},
      statusMessage: null,
      results: [],
      error: null,
    });
  },
}));
