import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { HomePage } from './pages/HomePage';
import { FittingPage } from './pages/FittingPage';
import { EditingPage } from './pages/EditingPage';
import { ProfilePage } from './pages/ProfilePage';
import { AdminPage } from './pages/AdminPage';
import { ErrorPage } from './pages/ErrorPage';
import MockPaymentEmulator from './pages/MockPaymentEmulator';

function App() {
  return (
    <Router>
      <Routes>
        {/* Главная страница - выбор функции */}
        <Route path="/" element={<HomePage />} />

        {/* Функция 1: Примерка одежды */}
        <Route path="/fitting" element={<FittingPage />} />

        {/* Функция 2: Редактирование изображений */}
        <Route path="/editing" element={<EditingPage />} />

        {/* Профиль пользователя */}
        <Route path="/profile" element={<ProfilePage />} />

        {/* Админ панель */}
        <Route path="/admin" element={<AdminPage />} />

        {/* Эмулятор платежей для тестирования */}
        <Route path="/mock-payment-emulator" element={<MockPaymentEmulator />} />

        {/* 404 страница */}
        <Route path="*" element={<ErrorPage />} />
      </Routes>
    </Router>
  );
}

export default App;
