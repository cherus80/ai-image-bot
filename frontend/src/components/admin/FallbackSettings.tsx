import React from 'react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { getFallbackSettings, updateFallbackSettings } from '../../api/admin';
import type { FallbackSettings as FallbackSettingsType } from '../../types/admin';
import toast from 'react-hot-toast';

export const FallbackSettings: React.FC = () => {
  const [settings, setSettings] = React.useState<FallbackSettingsType | null>(null);
  const [isLoading, setIsLoading] = React.useState(false);

  const loadSettings = async () => {
    try {
      const data = await getFallbackSettings();
      setSettings(data);
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Не удалось загрузить настройки fallback');
    }
  };

  React.useEffect(() => {
    loadSettings();
  }, []);

  const handleToggle = async (field: 'use_kie_ai' | 'disable_fallback', value: boolean) => {
    if (!settings) return;
    setIsLoading(true);
    try {
      const updated = await updateFallbackSettings({ [field]: value });
      setSettings(updated);
      toast.success('Настройки сохранены');
    } catch (err: any) {
      toast.error(err?.response?.data?.detail || 'Не удалось сохранить настройки');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card variant="glass" padding="lg" className="max-w-3xl">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-2xl font-bold text-dark-900">Fallback генерации</h2>
          <p className="text-sm text-dark-500">
            Управление использованием kie.ai и fallback на OpenRouter без перезапуска сервиса.
          </p>
        </div>
        <Button variant="ghost" size="sm" onClick={loadSettings} isLoading={isLoading}>
          Обновить
        </Button>
      </div>

      {settings ? (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <div className="font-semibold text-dark-800">Использовать kie.ai как основной</div>
              <div className="text-sm text-dark-500">
                При отключении все запросы пойдут напрямую через OpenRouter.
              </div>
            </div>
            <input
              type="checkbox"
              className="h-5 w-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              checked={settings.use_kie_ai}
              onChange={(e) => handleToggle('use_kie_ai', e.target.checked)}
              disabled={isLoading}
            />
          </div>

          <div className="flex items-center justify-between">
            <div>
              <div className="font-semibold text-dark-800">Запретить fallback на OpenRouter</div>
              <div className="text-sm text-dark-500">
                При ошибке kie.ai — не переключаться на OpenRouter (используйте для тестов kie.ai).
              </div>
            </div>
            <input
              type="checkbox"
              className="h-5 w-5 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              checked={settings.disable_fallback}
              onChange={(e) => handleToggle('disable_fallback', e.target.checked)}
              disabled={isLoading}
            />
          </div>
        </div>
      ) : (
        <div className="text-sm text-dark-500">Загрузка настроек...</div>
      )}
    </Card>
  );
};
