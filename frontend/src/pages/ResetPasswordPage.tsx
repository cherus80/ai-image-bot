import { useMemo, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { confirmPasswordReset } from '../api/authWeb';
import { validatePassword } from '../utils/passwordValidation';

export function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const token = useMemo(() => searchParams.get('token') || '', [searchParams]);
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);

    if (!token) {
      setError('Ссылка для сброса пароля недействительна.');
      return;
    }

    const validation = validatePassword(password);
    if (!validation.isValid) {
      setError(validation.error || 'Пароль не соответствует требованиям');
      return;
    }

    if (password !== confirmPassword) {
      setError('Пароли не совпадают');
      return;
    }

    setIsLoading(true);
    try {
      const response = await confirmPasswordReset({ token, new_password: password });
      setMessage(response.message);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Не удалось сбросить пароль');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 via-white to-secondary-50 px-4 py-10">
      <div className="max-w-xl w-full bg-white rounded-3xl border border-white/70 shadow-2xl p-8 space-y-6">
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-extrabold text-dark-900">Новый пароль</h2>
          <p className="text-sm text-dark-600">
            Придумайте новый пароль и подтвердите его.
          </p>
        </div>

        {error && (
          <div className="rounded-xl bg-red-50 border border-red-100 p-4">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}
        {message && (
          <div className="rounded-xl bg-emerald-50 border border-emerald-100 p-4">
            <p className="text-sm text-emerald-800">{message}</p>
          </div>
        )}

        <form className="space-y-4" onSubmit={handleSubmit}>
          <div className="space-y-1.5">
            <label htmlFor="password" className="block text-sm font-semibold text-slate-800">
              Новый пароль
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="new-password"
              required
              className="block w-full h-12 px-4 border border-slate-200 rounded-xl bg-slate-50 shadow-inner focus:outline-none focus:ring-2 focus:ring-primary-200 focus:border-primary-500 text-slate-800"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div className="space-y-1.5">
            <label htmlFor="confirmPassword" className="block text-sm font-semibold text-slate-800">
              Повторите пароль
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type="password"
              autoComplete="new-password"
              required
              className="block w-full h-12 px-4 border border-slate-200 rounded-xl bg-slate-50 shadow-inner focus:outline-none focus:ring-2 focus:ring-primary-200 focus:border-primary-500 text-slate-800"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full h-12 inline-flex items-center justify-center rounded-xl text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-indigo-600 shadow-lg shadow-blue-400/30 hover:shadow-blue-400/50 transition disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Сохранение...' : 'Сохранить пароль'}
          </button>
        </form>

        <p className="text-xs text-slate-500 text-center leading-relaxed">
          <Link to="/login" className="text-primary-700 hover:text-primary-800 underline">
            Вернуться ко входу
          </Link>
        </p>
      </div>
    </div>
  );
}
