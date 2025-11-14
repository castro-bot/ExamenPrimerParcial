from app.core import AuthSystemCore
from app.logging import Logging
from app.user_mgt import UserManagement
from app.ui import UI

class SistemaAutenticacion(
    AuthSystemCore,
    Logging,
    UserManagement,
    UI            
):
    """
    El sistema completo de autenticación, ensamblado a partir de:
    - Core (estado y conexiones)
    - LoggingMixin (registro de auditoría)
    - UserManagementMixin (acciones de usuario)
    - UIMixin (menús y flujos)
    """
    def __init__(self):
        super().__init__()