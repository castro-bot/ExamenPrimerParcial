import getpass
import psycopg2
from datetime import datetime
from pymongo.errors import PyMongoError
from app.security import hash_password, verify_password

class UserManagement:
    """Mixin para operaciones de usuario: registrar, iniciar sesión, cerrar sesión, editar, recuperar."""
    def registrar_usuario(self) -> None:
        print("\n--- 📝 User Registration ---")
        username = input("Username: ").strip()
        email = input("Email: ").strip()

        if not username or not email:
            print("❌ Error: Fields cannot be empty.")
            return

        password = getpass.getpass("Password: ")
        confirm_pass = getpass.getpass("Confirm Password: ")

        if password != confirm_pass:
            print("❌ Error: Passwords do not match.")
            return

        hashed_pw = hash_password(password).decode('utf-8')

        try:
            cursor = self.pg_conn.cursor()
            query = """
                INSERT INTO usuarios (username, email, password_hash, is_admin)
                VALUES (%s, %s, %s, %s) RETURNING id;
            """
            is_admin = False
            cursor.execute(query, (username, email, hashed_pw, is_admin))
            user_id = cursor.fetchone()['id']

            mongo_doc = {
                "pg_id": user_id, "username": username, "email": email,
                "password_hash": hashed_pw, "fecha_registro": datetime.now(),
                "activo": True, "is_admin": is_admin
            }
            self.mongo_db.usuarios.insert_one(mongo_doc)

            self.pg_conn.commit()
            self.registrar_log("registro_nuevo_usuario")
            print(f"✅ User '{username}' registered successfully.")

        except psycopg2.errors.UniqueViolation:
            self.pg_conn.rollback()
            print("❌ Error: Username or Email already exists.")
        except PyMongoError as e:
            self.pg_conn.rollback()
            print(f"❌ Error: MongoDB write failed. {e}")
        except Exception as e:
            self.pg_conn.rollback()
            print(f"❌ Unexpected Error: {e}")

    def login(self) -> bool:
        print("\n--- 🔐 Login ---")
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")

        try:
            cursor = self.pg_conn.cursor()
            cursor.execute(
                "SELECT id, username, email, password_hash, is_admin FROM usuarios WHERE username = %s AND activo = TRUE",
                (username,)
            )
            user = cursor.fetchone()

            if user and verify_password(password, user['password_hash']):
                self.current_user = user
                print(f"✅ Welcome back, {user['username']}!")
                self.registrar_log("login_exitoso")
                return True
            else:
                print("❌ Invalid credentials or account inactive.")
                self.registrar_log("login_fallido")
                return False
        except Exception as e:
            print(f"❌ Login Error: {e}")
            return False

    def logout(self) -> None:
        if self.current_user:
            print(f"👋 Goodbye, {self.current_user['username']}.")
            self.registrar_log("logout")
            self.current_user = None

    def recuperar_password(self) -> None:
        email = input("Enter your registered email: ").strip()
        print(f"ℹ️  [Simulation] Recovery link sent to {email}.")

    def editar_perfil(self) -> None:
        if not self.current_user: return

        new_email = input(f"Current email: {self.current_user['email']}\nNew Email: ").strip()
        if not new_email: return

        try:
            cursor = self.pg_conn.cursor()
            cursor.execute(
                "UPDATE usuarios SET email = %s WHERE id = %s",
                (new_email, self.current_user['id'])
            )
            self.mongo_db.usuarios.update_one(
                {"username": self.current_user['username']},
                {"$set": {"email": new_email}}
            )

            self.pg_conn.commit()
            self.current_user['email'] = new_email
            self.registrar_log("perfil_actualizado")
            print("✅ Profile updated successfully.")
        except Exception as e:
            print(f"❌ Update failed: {e}")
            try:
                self.pg_conn.rollback()
                print("ℹ️  Transaction rolled back.")
            except psycopg2.Error as rb_e:
                print(f"⚠️  Could not rollback. Connection error: {rb_e}")