import sys
import psycopg2
from typing import Optional, Dict, Any
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from psycopg2.extras import RealDictCursor
from config import PG_URI, MONGO_URI

class AuthSystemCore:
    """
    Clase base que mantiene el estado de la aplicación (conexiones a bases de datos, sesión de usuario).
    """
    def __init__(self):
        self.current_user: Optional[Dict[str, Any]] = None
        self.pg_conn = None
        self.mongo_db = None

        try:
            self.pg_conn = psycopg2.connect(PG_URI, cursor_factory=RealDictCursor)
            print("✅ [System] Connected to Clever Cloud PostgreSQL.")
        except psycopg2.Error as e:
            print(f"❌ [Critical] PostgreSQL Connection Failed: {e}")
            sys.exit(1)

        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            client.server_info()
            self.mongo_db = client["auth_system"]
            print("✅ [System] Connected to MongoDB Atlas.")
        except PyMongoError as e:
            print(f"❌ [Critical] MongoDB Atlas Connection Failed: {e}")
            sys.exit(1)