class UI:
    """Mixin para todos los menús de la interfaz de usuario y el bucle principal de la aplicación."""

    def ver_logs(self) -> None:
        """Ver registros en MongoDB (administrador o del propio usuario)."""
        if not self.current_user: return

        print("\n--- 📜 Activity Logs (MongoDB) ---")
        query = {}
        if not self.current_user.get('is_admin'):
            query = {"usuario_id": self.current_user['id']}

        logs = self.mongo_db.logs.find(query).sort("fecha", -1).limit(10)

        for log in logs:
            print(f"[{log['fecha'].strftime('%Y-%m-%d %H:%M:%S')}] {log['accion']} | IP: {log['ip']}")

    def menu_sesion(self):
        while self.current_user:
            role = "Admin" if self.current_user.get('is_admin') else "User"
            print(f"\n--- 👤 User Dashboard ({role}) ---")
            print("1. View Profile")
            print("2. Edit Profile")
            print("3. View Activity Logs")
            print("4. Logout")

            opcion = input("Select option: ")

            if opcion == "1":
                print(f"\nUser: {self.current_user['username']}\nEmail: {self.current_user['email']}")
            elif opcion == "2":
                self.editar_perfil()
            elif opcion == "3":
                self.ver_logs()
            elif opcion == "4":
                self.logout()
            else:
                print("Invalid option.")

    def run_app(self):
        try:
            while True:
                print("\n=== 🛡️  SECURE AUTH SYSTEM (PG + MONGO) ===")
                print("1. Login")
                print("2. Register")
                print("3. Password Recovery")
                print("4. Exit")

                opcion = input("Select option: ")

                if opcion == "1":
                    if self.login():
                        self.menu_sesion()
                elif opcion == "2":
                    self.registrar_usuario()
                elif opcion == "3":
                    self.recuperar_password()
                elif opcion == "4":
                    break
                else:
                    print("Invalid option.")
        except KeyboardInterrupt:
            print("\nShutdown signal received.")
        finally:
            if self.pg_conn is not None:
                self.pg_conn.close()
                print("PostgreSQL connection closed.")
            print("Goodbye.")