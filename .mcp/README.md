# MCP Configuration

Эта директория содержит конфигурацию для Model Context Protocol (MCP) серверов.

## Playwright MCP

### Что это?

MCP Playwright позволяет Claude Code автоматически тестировать фронтенд:
- Открывать приложение в браузере
- Делать скриншоты
- Взаимодействовать с UI
- Читать консоль браузера
- Проверять localStorage/cookies

### Конфигурация

Файл `playwright-config.json` содержит локальную конфигурацию для Playwright MCP сервера.

**Для использования нужно:**
1. Добавить конфигурацию в Claude Desktop config
2. Перезапустить Claude Desktop

**Подробная инструкция:** `../docs/MCP_PLAYWRIGHT_SETUP.md`

### Быстрая настройка

**macOS:**
```bash
# 1. Открыть конфигурацию Claude Desktop
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 2. Добавить:
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp-server"]
    }
  }
}

# 3. Сохранить (Ctrl+O, Enter, Ctrl+X)
# 4. Перезапустить Claude Desktop (Cmd+Q, потом открыть заново)
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Проверка

После настройки спросите Claude Code:
```
Проверь доступен ли MCP Playwright
```

Должны появиться инструменты:
- `mcp__playwright__navigate`
- `mcp__playwright__screenshot`
- `mcp__playwright__click`
- `mcp__playwright__fill`
- `mcp__playwright__console`
- `mcp__playwright__evaluate`

### Использование

```
Claude, открой http://localhost:5173 через Playwright и протестируй HomePage
```

Claude автоматически:
1. Откроет браузер
2. Сделает скриншот
3. Проверит консоль
4. Проверит localStorage
5. Предоставит детальный отчёт

---

**Больше информации:** `../docs/MCP_PLAYWRIGHT_SETUP.md`
