import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import Settings

def get_connection():
    return psycopg2.connect(Settings.DB_DSN, cursor_factory=RealDictCursor)
