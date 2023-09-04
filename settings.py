from dotenv import load_dotenv
from envparse import env


load_dotenv('.env')
DEV = env.bool("DEV")
DB_USER_TEST = env.str('POSTGRES_USER_TEST')
DB_PASSWORD_TEST = env.str('POSTGRES_PASSWORD_TEST')
DB_HOST_TEST = env.str('DB_HOST_TEST')
DB_PORT_TEST = env.int('DB_PORT_TEST')
DB_NAME_TEST = env.str('POSTGRES_DB_TEST')

print(DEV)

if not DEV:
    DB_USER = env.str('POSTGRES_USER')
    DB_PASSWORD = env.str('POSTGRES_PASSWORD')
    DB_HOST = env.str('DB_HOST')
    DB_PORT = env.int('DB_PORT')
    DB_NAME = env.str('POSTGRES_DB')
else:
    DB_USER = env.str('POSTGRES_USER_DEV')
    DB_PASSWORD = env.str('POSTGRES_PASSWORD_DEV')
    DB_HOST = env.str('DB_HOST_DEV')
    DB_PORT = env.int('DB_PORT_DEV')
    DB_NAME = env.str('POSTGRES_DB_DEV')


ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(ASYNC_DATABASE_URL)
DATABASE_TEST_URL = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASSWORD_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"
