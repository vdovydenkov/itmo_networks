import psycopg2
from app.config import Settings

def get_connection():
    # return psycopg2.connect(Settings.DB_DSN, cursor_factory=RealDictCursor)
    return psycopg2.connect(Settings.DB_DSN)