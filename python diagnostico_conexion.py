"""
Script de diagnóstico: revela el mensaje de error REAL que PostgreSQL
está devolviendo, y que psycopg2 no puede mostrar por el problema de
codificación (UnicodeDecodeError).

CÓMO USARLO:
1. Copia este archivo a la raíz de tu proyecto (2626-DAW-Corte-Rios-Noa-main),
   junto a tu app.py y tu .env.
2. Activa tu entorno virtual:
       env\\Scripts\\activate
3. Ejecútalo:
       python diagnostico_conexion.py
4. Copia y pégame TODO lo que imprima en la terminal.
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

CONFIG_LOCAL = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
    'user': os.environ.get('DB_USER', 'admin'),
    'password': os.environ.get('DB_PASSWORD', 'admin1234'),
    'dbname': os.environ.get('DB_NAME', 'db_gastrobar'),
}

print("=== Intentando conectar con estos datos ===")
for clave, valor in CONFIG_LOCAL.items():
    if clave == 'password':
        print(f"  {clave}: {'*' * len(str(valor))}  (longitud: {len(str(valor))})")
    else:
        print(f"  {clave}: {valor}")
print()

try:
    conn = psycopg2.connect(**CONFIG_LOCAL)
    print("✅ ¡CONEXIÓN EXITOSA! El problema NO está en estos datos de conexión.")
    cur = conn.cursor()
    cur.execute("SELECT current_database(), current_user, inet_server_port();")
    print("Conectado realmente a:", cur.fetchone())
    cur.close()
    conn.close()

except UnicodeDecodeError as e:
    print("❌ Se capturó el UnicodeDecodeError, pero ahora vamos a leer")
    print("   el mensaje real que PostgreSQL intentó enviarte:\n")
    crudo = e.object  # los bytes originales que fallaron al decodificar
    print("Bytes crudos:", crudo)
    print()
    for codec in ("latin-1", "cp1252", "utf-8-sig"):
        try:
            print(f"--- Intentando decodificar como {codec} ---")
            print(crudo.decode(codec))
            print()
        except Exception as err:
            print(f"  (no se pudo con {codec}: {err})")

except psycopg2.OperationalError as e:
    print("❌ Error de conexión normal (esto es lo esperado si algo está mal):")
    print(e)

except Exception as e:
    print(f"❌ Otro tipo de error: {type(e).__name__}")
    print(e)