# videouroki bot

Бот доступен в Telegram: @vingp_answers_bot

## Запуск

В переменных окружения надо проставить API токен бота, а также список админов

`TELEGRAM_BOT_TOKEN` - API токен бота

`ADMINS` - список админов

Docker:

```shell
docker-compose up --build -d
```

Python (Windows):

```shell
python -m venv venv
````

```shell
.\venv\Scripts\activate
```

```shell
python -m pip install -r requirements.txt
```

```shell
python main.py
````

## Команды бота:

- `/start` — приветственное сообщение
- `/help` — справка
- `/logs` — файл с логами (только для админов)
- `/clean_logs` — очистить логи (только для админов)