from datetime import datetime
from pymongo.errors import PyMongoError

class Logging:
    """Mixin para todos los métodos de registro de auditoría."""
    def registrar_log(self, accion: str, ip: str = "127.0.0.1") -> None:
        if self.mongo_db is None:
            return

        log_entry = {
            "usuario_id": self.current_user['id'] if self.current_user else None,
            "username_snapshot": self.current_user['username'] if self.current_user else "Anonymous",
            "accion": accion,
            "fecha": datetime.now(),
            "ip": ip
        }
        try:
            self.mongo_db.logs.insert_one(log_entry)
        except PyMongoError as e:
            print(f"⚠️ [Warning] Failed to write log to Mongo: {e}")