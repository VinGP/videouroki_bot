from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()
TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")
ADMINS = env.list("ADMINS", subcast=int)
