# Predloshka Bot

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot_API-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Predloshka Bot** — это Telegram-бот, разработанный для сбора идей и предложений от пользователей. Бот принимает сообщения (текст, фото, видео, голосовые сообщения, документы), запрашивает подтверждение отправки и пересылает их в указанную группу для рассмотрения администрацией. Поддерживает локализацию (русский и английский языки), динамическое определение языка и переключение через команду.

---

## ✨ Возможности

- **Прием предложений**: Поддержка текста, фото, видео, голосовых сообщений и документов.
- **Подтверждение**: Пользователь подтверждает отправку через кнопки "Отправить" / "Отменить".
- **Локализация**: Автоматическое определение языка (ru/en) с возможностью ручного переключения.
- **Команды**:
  - `/start` — Приветственное сообщение.
  - `/help` — Подробная инструкция по использованию.
  - `/lang <ru или en>` — Смена языка.
- **Сохранение настроек**: Язык пользователя сохраняется для удобства.

---

## 📋 Требования

- **Python**: 3.9 или выше.
- **Библиотеки**:
  - `python-telegram-bot` (версия 20.x).
- **Telegram**: Токен бота от [@BotFather](https://t.me/BotFather) и ID чата для пересылки сообщений.

---
