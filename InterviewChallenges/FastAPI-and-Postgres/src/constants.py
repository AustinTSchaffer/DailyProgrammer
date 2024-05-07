import os

POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', '5432'))
POSTGRES_DB = os.getenv('POSTGRES_DB', 'defaultdb')
POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME', 'app')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'app-password')

POSTGRES_CONNECTION_STRING = f"""
dbname={POSTGRES_DB}
user={POSTGRES_USERNAME}
password={POSTGRES_PASSWORD}
host={POSTGRES_HOST}
port={POSTGRES_PORT}
"""

APP_RELOAD = os.getenv('APP_RELOAD', 'true').lower() == 'true'
APP_PORT = int(os.getenv('APP_PORT', '8081'))
