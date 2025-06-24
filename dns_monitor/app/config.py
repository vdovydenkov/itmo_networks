from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "A7112JRosmm")
    DB_DSN = os.getenv("DB_DSN", "postgresql://user:passwd@127.0.0.1:5432/dbname")
