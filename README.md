# 💾 Kibronik Telegram Bot: Автогенерация постов

## ✅ Цель проекта

Создать систему, которая:

1. 🔎 Анализирует международные IT, AI, криптоновости за последние 24 часа
2. 📝 Автоматически формирует текст поста
3. 🎨 Генерирует уникальное изображение с помощью AI
4. 📤 Отправляет пост в Telegram-бот как черновик с кнопкой

## 🛠️ Стек технологий
- Python (aiohttp, aiogram)
- Telegram Bot API
- OpenAI API (GPT + DALL·E)
- Render (деплой `web.py`)
- GitHub (репозиторий и хранение изображений)
- Curl (ручной вызов `/create_post`)

## 📂 Структура проекта
```
kibronik_bot/
├── bot.py                # Telegram-бот c кнопкой «Опубликовать»
├── web.py                # Веб-сервер + /create_post
├── images/               # Папка для картинок (требуется `my_image.png`)
├── post.json             # JSON для curl
├── .env                  # BOT_TOKEN, OWNER_ID, CHANNEL_ID
├── requirements.txt      # Зависимости
└── .gitignore            # Git-исключения
```

## ✅ Реализовано
- Черновики в Telegram-бот с текстом и кнопкой «Опубликовать»
- UTF-8 + Markdown отображение текстов
- Поддержка кириллицы
- Подключение картинок через GitHub (Render читает `images/my_image.png`)
- Генерация уникальных изображений через DALL·E (или аналоги)
- Ручная генерация поста через `curl`

## ❌ Что не реализовано
- ChatGPT не может напрямую сделать `POST` на Render (нет доступа в интернет)
- Автопубликация без `curl` ещё не внедрена

## ⏳ Текущий флоу
1. Артём пишет: "Сделай пост"
2. ChatGPT:
   - ищет новость за последние 24 часа
   - генерирует текст поста
   - генерирует уникальное изображение по теме
   - сохраняет в `images/my_image.png`
3. Артём пушит файл в GitHub (если не сгенерирован заранее)
4. ChatGPT даёт `text`, Артём вставляет в `post.json`
5. Выполняется:
   ```bash
   curl -X POST https://kibronik-bot.onrender.com/create_post \
     -H "Content-Type: application/json; charset=utf-8" \
     --data-binary @post.json
   ```

```
