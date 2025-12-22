import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { sendVerificationEmail } from '../api/authWeb';
import { AuthGuard } from '../components/auth/AuthGuard';
import { Layout } from '../components/common/Layout';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { useAuthStore } from '../store/authStore';
import toast from 'react-hot-toast';

export function VerifyRequiredPage() {
  const navigate = useNavigate();
  const { user, logout, refreshProfile } = useAuthStore();
  const [isSending, setIsSending] = useState(false);
  const [cooldownSec, setCooldownSec] = useState<number>(0);

  useEffect(() => {
    // если вдруг пользователь уже верифицирован — отправляем домой
    if (user?.email_verified) {
      navigate('/', { replace: true });
    }
  }, [user?.email_verified, navigate]);

  useEffect(() => {
    if (cooldownSec <= 0) return;
    const id = setInterval(() => setCooldownSec((prev) => Math.max(0, prev - 1)), 1000);
    return () => clearInterval(id);
  }, [cooldownSec]);

  const handleResend = async () => {
    if (!user?.email) return;
    setIsSending(true);
    try {
      const response = await sendVerificationEmail();
      toast.success(response.message || 'Письмо отправлено');
      setCooldownSec(60);
      await refreshProfile();
    } catch (error: any) {
      const detail = error.response?.data?.detail || 'Не удалось отправить письмо';
      toast.error(detail);
    } finally {
      setIsSending(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!user) {
    return (
      <AuthGuard>
        <Layout title="Подтверждение email" subtitle="Загрузка..." showBalance={false}>
          <div className="min-h-[60vh] flex items-center justify-center">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-600" />
          </div>
        </Layout>
      </AuthGuard>
    );
  }

  return (
    <AuthGuard>
      <Layout title="Подтвердите email" subtitle={user.email || ''} showBalance={false}>
        <div className="max-w-3xl mx-auto p-4 md:p-6">
          <Card variant="glass" padding="lg" className="space-y-6">
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-12 h-12 rounded-full bg-yellow-100 text-yellow-700 flex items-center justify-center text-xl">
                ✉️
              </div>
              <div className="space-y-2">
                <h2 className="text-2xl font-bold text-gray-900">Требуется подтверждение</h2>
                <p className="text-gray-700">
                  Мы отправили письмо с подтверждением на <strong>{user.email}</strong>. Пожалуйста,
                  перейдите по ссылке из письма, чтобы разблокировать все возможности приложения.
                </p>
                <p className="text-sm text-gray-500">
                  После подтверждения мы автоматически перенаправим вас на главную страницу.
                </p>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3">
              <Button
                onClick={handleResend}
                disabled={isSending || cooldownSec > 0}
                variant="primary"
              >
                {isSending ? 'Отправляем...' : cooldownSec > 0 ? `Повторно через ${cooldownSec} c` : 'Отправить письмо снова'}
              </Button>
              <Button onClick={handleLogout} variant="ghost" className="text-red-600">
                Выйти
              </Button>
            </div>

            <div className="rounded-lg bg-blue-50 border border-blue-200 p-4 text-sm text-blue-800">
              Не нашли письмо? Проверьте папку «Спам» или попробуйте другой адрес. Если проблема
              повторяется, напишите нам в поддержку.
            </div>
          </Card>
        </div>
      </Layout>
    </AuthGuard>
  );
}
