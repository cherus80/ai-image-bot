/**
 * Mock Payment Emulator - страница для тестирования платежей
 *
 * ВНИМАНИЕ: Используется только в режиме разработки (PAYMENT_MOCK_MODE=true).
 * НЕ ОТОБРАЖАЕТСЯ В PRODUCTION!
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface MockPayment {
  payment_id: string;
  status: string;
  amount: string;
  currency: string;
  description: string;
  metadata: Record<string, any>;
  confirmation_url: string;
  created_at: string;
  paid: boolean;
  test: boolean;
}

interface MockPaymentListResponse {
  payments: MockPayment[];
  total: number;
}

const MockPaymentEmulator: React.FC = () => {
  const [payments, setPayments] = useState<MockPayment[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const API_BASE_URL = '';  // Use Vite proxy

  // Загрузка списка платежей
  const loadPayments = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get<MockPaymentListResponse>(
        `${API_BASE_URL}/api/v1/mock-payments/list`
      );

      setPayments(response.data.payments);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load payments');
    } finally {
      setLoading(false);
    }
  };

  // Подтверждение платежа
  const approvePayment = async (paymentId: string) => {
    setError(null);
    setSuccessMessage(null);

    try {
      await axios.post(
        `${API_BASE_URL}/api/v1/mock-payments/${paymentId}/approve`
      );

      setSuccessMessage(`Payment ${paymentId} approved successfully!`);
      await loadPayments();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to approve payment');
    }
  };

  // Отмена платежа
  const cancelPayment = async (paymentId: string) => {
    setError(null);
    setSuccessMessage(null);

    try {
      await axios.post(
        `${API_BASE_URL}/api/v1/mock-payments/${paymentId}/cancel`
      );

      setSuccessMessage(`Payment ${paymentId} canceled successfully!`);
      await loadPayments();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to cancel payment');
    }
  };

  // Загрузка при монтировании компонента
  useEffect(() => {
    loadPayments();
    // Автообновление каждые 5 секунд
    const interval = setInterval(loadPayments, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">
                🔧 Mock Payment Emulator
              </h1>
              <p className="text-gray-600">
                Эмулятор платежей для локального тестирования (PAYMENT_MOCK_MODE)
              </p>
            </div>
            <button
              onClick={loadPayments}
              disabled={loading}
              className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg font-medium disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Refresh'}
            </button>
          </div>
        </div>

        {/* Alerts */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-4">
            <strong>Error:</strong> {error}
          </div>
        )}

        {successMessage && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg mb-4">
            <strong>Success:</strong> {successMessage}
          </div>
        )}

        {/* Payments List */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-800">
              Payments ({payments.length})
            </h2>
          </div>

          {payments.length === 0 ? (
            <div className="p-12 text-center text-gray-500">
              <p className="text-lg">No payments found</p>
              <p className="text-sm mt-2">
                Create a payment in the app to see it here
              </p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {payments.map((payment) => (
                <div
                  key={payment.payment_id}
                  className="p-6 hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-start justify-between">
                    {/* Payment Info */}
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <span
                          className={`px-3 py-1 rounded-full text-sm font-medium ${
                            payment.status === 'succeeded'
                              ? 'bg-green-100 text-green-800'
                              : payment.status === 'canceled'
                              ? 'bg-red-100 text-red-800'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}
                        >
                          {payment.status.toUpperCase()}
                        </span>
                        <span className="text-2xl font-bold text-gray-800">
                          {payment.amount} {payment.currency}
                        </span>
                      </div>

                      <p className="text-gray-600 mb-3">{payment.description}</p>

                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-gray-500">Payment ID:</span>
                          <p className="font-mono text-gray-800 break-all">
                            {payment.payment_id}
                          </p>
                        </div>
                        <div>
                          <span className="text-gray-500">Created At:</span>
                          <p className="text-gray-800">
                            {new Date(payment.created_at).toLocaleString()}
                          </p>
                        </div>
                      </div>

                      {/* Metadata */}
                      {Object.keys(payment.metadata).length > 0 && (
                        <div className="mt-3 p-3 bg-gray-50 rounded-lg">
                          <p className="text-xs text-gray-500 mb-2">Metadata:</p>
                          <pre className="text-xs font-mono text-gray-700 overflow-x-auto">
                            {JSON.stringify(payment.metadata, null, 2)}
                          </pre>
                        </div>
                      )}
                    </div>

                    {/* Action Buttons */}
                    {payment.status === 'pending' && (
                      <div className="flex flex-col gap-2 ml-4">
                        <button
                          onClick={() => approvePayment(payment.payment_id)}
                          className="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-lg font-medium transition-colors"
                        >
                          ✓ Approve
                        </button>
                        <button
                          onClick={() => cancelPayment(payment.payment_id)}
                          className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded-lg font-medium transition-colors"
                        >
                          ✗ Cancel
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-sm text-yellow-800">
            <strong>⚠️ Warning:</strong> This is a mock payment emulator for local testing only.
            It does not process real payments. Set PAYMENT_MOCK_MODE=true in backend .env to enable.
          </p>
        </div>
      </div>
    </div>
  );
};

export default MockPaymentEmulator;
