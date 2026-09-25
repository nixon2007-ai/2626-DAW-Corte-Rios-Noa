import os

import psycopg2
import psycopg2.extras

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace(
        'postgres://',
        'postgresql://',
        1
    )

CONFIG_LOCAL = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5433'),
    'user': os.environ.get('DB_USER', 'admin'),
    'password': os.environ.get('DB_PASSWORD', 'sql1234'),
    'dbname': os.environ.get('DB_NAME', 'db_gastrobar'),
    'options': '-c client_encoding=UTF8 -c lc_messages=C',
}


def get_conexion():

    if DATABASE_URL:
        return psycopg2.connect(
            DATABASE_URL,
            cursor_factory=psycopg2.extras.RealDictCursor
        )

    return psycopg2.connect(
        cursor_factory=psycopg2.extras.RealDictCursor,
        **CONFIG_LOCAL
    )