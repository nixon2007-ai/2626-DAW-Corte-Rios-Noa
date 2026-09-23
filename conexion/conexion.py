import os
import psycopg2
import psycopg2.extras

# ---------------------------------------------------------------------------
# Conexion a PostgreSQL
#
# En Render, la variable de entorno DATABASE_URL se genera automaticamente
# al vincular la base de datos PostgreSQL con el servicio web.
# En local (tu PC), si no existe esa variable, se usan los datos de abajo
# como valor por defecto (ajusta usuario/clave/puerto a tu instalacion).
# ---------------------------------------------------------------------------

DATABASE_URL = os.environ.get('DATABASE_URL')

# Render entrega a veces la URL con el prefijo antiguo "postgres://",
# pero psycopg2 requiere "postgresql://"
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

CONFIG_LOCAL = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'sql1234'),
    'dbname': os.environ.get('DB_NAME', 'gastrobar_db'),
}


def get_conexion():
    """Devuelve una conexion a PostgreSQL.

    Los cursores creados con esta conexion regresan filas como
    diccionarios (RealDictCursor), para poder acceder por nombre de
    columna igual que antes (fila['nombre']).
    """
    if DATABASE_URL:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    else:
        conn = psycopg2.connect(cursor_factory=psycopg2.extras.RealDictCursor, **CONFIG_LOCAL)
    return conn