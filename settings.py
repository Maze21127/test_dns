from dotenv import load_dotenv
from envparse import env

DEV = env.bool("DEV")

load_dotenv('.env') if not DEV else load_dotenv('.env.dev')

DB_USER = env.str('POSTGRES_USER')
DB_PASSWORD = env.str('POSTGRES_PASSWORD')
DB_HOST = env.str('DB_HOST')
DB_PORT = env.int('DB_PORT')
DB_NAME = env.str('POSTGRES_DB')


DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

