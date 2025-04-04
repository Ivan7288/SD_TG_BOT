# SD Telegram Bot

Telegram бот с веб-интерфейсом для генерации изображений с помощью Stable Diffusion.

## Описание

Этот проект представляет собой Telegram бота, который позволяет пользователям генерировать изображения с помощью Stable Diffusion. Проект состоит из двух основных компонентов:
- Веб-приложение (app.py)
- Telegram бот (bot.py)

## Требования

- Python 3.8+
- Telegram Bot Token
- HuggingFace Token
- Другие зависимости указаны в requirements.txt

## Установка

1. Клонируйте репозиторий:
```bash
git clone [URL вашего репозитория]
cd SD_TG_BOT
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
.\venv\Scripts\activate.bat     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env на основе .env.example и заполните необходимые переменные окружения:
```bash
cp .env.example .env
```

## Запуск

### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

### Windows
```bash
python app.py
# В другом терминале
python bot.py
```

## Структура проекта

```
SD_TG_BOT/
├── app.py              # Веб-приложение
├── bot.py              # Telegram бот
├── models.py           # Модели данных
├── requirements.txt    # Зависимости
├── start.sh           # Скрипт запуска
├── static/            # Статические файлы
├── templates/         # HTML шаблоны
└── services/          # Сервисные модули
```

## Конфигурация

В файле `.env` необходимо указать следующие переменные:
- `TELEGRAM_BOT_TOKEN` - токен вашего Telegram бота
- `HUGGINGFACE_TOKEN` - API ключ для Stable Diffusion
- `DATABASE_URL` - путь к базе данный(можно и URL)
- `WEB_APP_URL` - Telegram Mini App URL
- Другие необходимые переменные окружения

## Использование

1. Откройте Telegram и найдите вашего бота
2. Запустите бота
3. Используйте веб-интерфейс для генерации изображений

## Авторы

- Ivan7288
- Yelisey-08
 