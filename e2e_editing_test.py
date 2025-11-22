"""
E2E тест для функции «Редактирование фото».

Сценарий:
- Регистрирует нового пользователя через API (если существует — логинится).
- Кладёт токен и профиль в localStorage, чтобы сразу открыть защищённые страницы.
- Выполняет полный цикл редактирования: загрузка базового изображения, ввод промпта,
  улучшение промпта AI-ассистентом, генерация результата и проверка, что изображение получено.

Перед запуском убедитесь, что фронт доступен по BASE_URL и API по API_URL.
"""

import argparse
import asyncio
import json
import os
import uuid
from pathlib import Path
from typing import Any, Dict

import requests
from playwright.async_api import async_playwright, expect, Page

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5173")
API_URL = os.environ.get("API_URL", "http://localhost:8000")
FIXTURE_IMAGE = Path("imeg/1.JPG")
ARTIFACTS_DIR = Path(".playwright-mcp")


def _api_register_or_login(email: str, password: str) -> Dict[str, Any]:
    """Возвращает пару (token, user) после регистрации или логина."""
    payload = {"email": email, "password": password, "first_name": "E2E", "last_name": "Tester"}
    register_resp = requests.post(f"{API_URL}/api/v1/auth-web/register", json=payload, timeout=10)
    if register_resp.status_code not in (200, 201):
        # Возможно пользователь уже есть — пробуем логин
        login_resp = requests.post(
            f"{API_URL}/api/v1/auth-web/login", json={"email": email, "password": password}, timeout=10
        )
        login_resp.raise_for_status()
        data = login_resp.json()
    else:
        data = register_resp.json()

    token = data["access_token"]
    me_resp = requests.get(
        f"{API_URL}/api/v1/auth-web/me",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    me_resp.raise_for_status()
    user = me_resp.json()["user"]
    return {"token": token, "user": user}


async def _hydrate_auth(page: Page, token: str, user: Dict[str, Any]) -> None:
    """Ставит auth-storage в localStorage и обновляет страницу."""
    auth_state = {"state": {"token": token, "user": user, "isAuthenticated": True}, "version": 0}
    await page.goto(BASE_URL)
    await page.evaluate(
        """(state) => {
            localStorage.setItem('auth-storage', JSON.stringify(state));
        }""",
        auth_state,
    )
    await page.reload(wait_until="domcontentloaded")


async def run_test(prompt_text: str) -> None:
    if not FIXTURE_IMAGE.exists():
        raise FileNotFoundError(f"Фикстура не найдена: {FIXTURE_IMAGE}")

    email = f"e2e-edit-{uuid.uuid4().hex[:8]}@example.com"
    password = "Test1234!"
    auth = _api_register_or_login(email, password)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await _hydrate_auth(page, auth["token"], auth["user"])

        # Переходим на страницу редактирования
        await page.goto(f"{BASE_URL}/editing", wait_until="domcontentloaded")

        # Загружаем базовое изображение
        file_input = page.locator('input[type="file"]')
        await file_input.set_input_files(str(FIXTURE_IMAGE))

        # Вводим промпт
        prompt_box = page.get_by_placeholder("Опишите, как хотите изменить изображение...")
        await prompt_box.fill(prompt_text)

        # Отправляем на улучшение AI
        await page.get_by_role("button", name="Улучшить с AI").click()

        # Ждём появления карточки с вариантами
        confirm_block = page.get_by_text("Подтвердите или отредактируйте улучшенный промпт")
        await expect(confirm_block).to_be_visible(timeout=45_000)

        # Генерируем изображение по первому варианту
        await page.get_by_role("button", name="Генерировать изображение").first.click()

        # Ждём результата
        result_text = page.get_by_text("Изображение готово", exact=False)
        await expect(result_text).to_be_visible(timeout=120_000)
        result_image = page.get_by_role("img", name="Generated result")
        await expect(result_image).to_be_visible(timeout=5_000)

        # Сохраняем скриншот артефакта
        ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(ARTIFACTS_DIR / "e2e-editing.png"), full_page=True)

        await browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="E2E тест редактирования фото")
    parser.add_argument(
        "--prompt",
        default="Замени фон на поверхность луны",
        help="Промпт для тестовой генерации",
    )
    args = parser.parse_args()
    asyncio.run(run_test(args.prompt))
