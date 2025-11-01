import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MockPaymentEmulator from './pages/MockPaymentEmulator';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
            <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl w-full">
              <h1 className="text-3xl font-bold text-gray-800 mb-4">
                🚀 AI Image Generator Bot
              </h1>
              <p className="text-gray-600 mb-6">
                Backend запущен успешно! Mock Payment Emulator доступен для тестирования платежей.
              </p>

              <div className="space-y-4">
                <div className="border border-gray-200 rounded-lg p-4">
                  <h2 className="text-lg font-semibold text-gray-700 mb-2">
                    📡 Сервисы
                  </h2>
                  <ul className="space-y-2 text-sm">
                    <li className="flex items-center">
                      <span className="w-3 h-3 bg-green-500 rounded-full mr-3"></span>
                      <span className="text-gray-600">Backend API:</span>
                      <a href="http://localhost:8000" target="_blank" rel="noopener noreferrer" className="ml-2 text-blue-600 hover:underline">
                        http://localhost:8000
                      </a>
                    </li>
                    <li className="flex items-center">
                      <span className="w-3 h-3 bg-green-500 rounded-full mr-3"></span>
                      <span className="text-gray-600">API Docs:</span>
                      <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" className="ml-2 text-blue-600 hover:underline">
                        http://localhost:8000/docs
                      </a>
                    </li>
                    <li className="flex items-center">
                      <span className="w-3 h-3 bg-green-500 rounded-full mr-3"></span>
                      <span className="text-gray-600">Mock Emulator:</span>
                      <a href="/mock-payment-emulator" className="ml-2 text-blue-600 hover:underline">
                        /mock-payment-emulator
                      </a>
                    </li>
                  </ul>
                </div>

                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <h3 className="text-sm font-semibold text-yellow-800 mb-2">
                    🔧 Режим разработки
                  </h3>
                  <p className="text-xs text-yellow-700">
                    PAYMENT_MOCK_MODE включён. Платежи эмулируются локально без реального ЮKassa.
                  </p>
                </div>

                <a href="/mock-payment-emulator" className="block w-full bg-blue-600 hover:bg-blue-700 text-white text-center font-medium py-3 px-4 rounded-lg transition-colors">
                  Открыть эмулятор платежей →
                </a>
              </div>
            </div>
          </div>
        } />

        <Route path="/mock-payment-emulator" element={<MockPaymentEmulator />} />

        <Route path="*" element={
          <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
            <div className="bg-white rounded-lg shadow-lg p-8 text-center">
              <h1 className="text-2xl font-bold text-gray-800 mb-4">404</h1>
              <p className="text-gray-600 mb-6">Страница не найдена</p>
              <a href="/" className="text-blue-600 hover:underline">
                Вернуться на главную
              </a>
            </div>
          </div>
        } />
      </Routes>
    </Router>
  );
}

export default App;
