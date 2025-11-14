# Sistema de Autenticación Híbrido (Postgres + MongoDB)

## 1. Visión General
Este proyecto es un sistema de autenticación desarrollado como el Examen de Primer Parcial de Adolfo Castro.

El objetivo es implementar un sistema de registro e inicio de sesión seguro que realiza una **doble escritura** de los datos del usuario. El sistema utiliza una arquitectura híbrida:
* **PostgreSQL (en Clever Cloud):** Sirve como la fuente principal de verdad para la autenticación y los datos relacionales del usuario.
* **MongoDB (en Atlas):** Sirve como un almacén de documentos NoSQL para el registro de auditoría (logs) y como un almacén de datos de usuario.

El sistema está construido en Python con una arquitectura modular basada en Mixins para una clara separación de conceptos (SoC).

## 2. Pruebas
Se ejecutaron pruebas manuales para verificar toda la funcionalidad del sistema. Las pruebas cubrieron el registro de nuevos usuarios, la autenticación, la gestión de perfiles y el registro de auditoría.

### Prueba 1: Registro de nuevo usuario (Adolfo Castro)
* **Descripción:** Verifica que un nuevo usuario (`Adolfo Castro`) puede ser creado. El sistema debe escribir en Postgres y Mongo, y registrar la acción.
* **Resultado:** **ÉXITO**. El usuario fue creado en ambas bases de datos y el log anónimo de "registro_nuevo_usuario" fue creado.
    ![Prueba 1 Screenshot](screenshots/image15.png)

    ![Prueba 1 Screenshot](screenshots/image13.png)

### Prueba 2: Login con credenciales correctas (Adolfo Castro)
* **Descripción:** Verifica que el usuario recién creado (`Adolfo Castro`) puede iniciar sesión.
* **Resultado:** **ÉXITO**. El usuario fue autenticado, se mostró el dashboard y se creó un log de `login_exitoso` en MongoDB.
    ![Prueba 2 Screenshot](screenshots/image16.png)

### Prueba 3: Edición de perfil de usuario (Jose Naranjo)
* **Descripción:** Verifica que un usuario logueado (`Jose Naranjo`) puede editar su perfil. La actualización debe reflejarse en ambas bases de datos y ser registrada.
* **Resultado:** **ÉXITO**. El email fue actualizado en el terminal, en la tabla de Postgres y se generó un log de `perfil_actualizado` en Mongo.
    ![Prueba 3 Screenshot](screenshots/image3.png)

    ![Prueba 3 Screenshot](screenshots/image12.png)

    ![Prueba 3 Screenshot](screenshots/image8.png)

### Prueba 4: Cierre de sesión (Jose Naranjo)
* **Descripción:** Verifica que un usuario logueado puede cerrar su sesión. La acción debe ser registrada.
* **Resultado:** **ÉXITO**. El sistema mostró el mensaje "Goodbye" y se creó un log de `logout` en MongoDB.
    ![Prueba 4 Screenshot](screenshots/image4.png)

    ![Prueba 4 Screenshot](screenshots/image9.png)

### Prueba 5: Login con credenciales incorrectas
* **Descripción:** Verifica que el sistema rechaza credenciales inválidas.
* **Resultado:** **ÉXITO**. La terminal mostró un error y la base de datos de MongoDB registró correctamente el evento `login_fallido`.
    ![Prueba 5 Screenshot](screenshots/image10.png)
    ![Prueba 5 Screenshot](screenshots/image11.png)

### Prueba 6: Edición de perfil de usuario (Adolfo Castro)
* **Descripción:** Verifica que un usuario logueado (`Adolfo Castro`) puede editar su correo electrónico. La actualización debe reflejarse en la sesión de la app y registrarse en los logs.
* **Resultado:** **ÉXITO**. El usuario cambió su email de `aacastrom@pucesm.edu.ec` a `aacastrom@gmail.com`. La app mostró el nuevo email al seleccionar "View Profile", y el log `perfil_actualizado` fue creado en MongoDB.
    ![Prueba 6 Screenshot](screenshots/image17.png)

    ![Prueba 6 Screenshot B](screenshots/image18.png)


### Prueba 7: Estado de la base de datos (MongoDB Usuarios)
* **Descripción:** Verificación de la colección `usuarios` en MongoDB que muestra los datos de los usuarios de prueba.
* **Resultado:** **ÉXITO**. La colección muestra los documentos para `Jose Naranjo` y `Adolfo Castro` (con su emails ya actualizados).
    ![Prueba 7 Screenshot](screenshots/image14.png)

---

## 3. Instrucciones de instalación y configuración

Siga estos pasos para ejecutar el proyecto en un entorno de desarrollo

1.  **Clonar el Repositorio**
    ```bash
    git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
    cd ExamPrimerParcial
    ```

2.  **Crear y Activar el Entorno Virtual**
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate
    ```

3.  **Instalar Dependencias**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno**
    * Cree un archivo `.env` en la raíz del proyecto.
    * Copie el contenido de la [Sección 9 (Ejemplo .env)] en este archivo.
    * Rellene `POSTGRESQL_ADDON_URI` y `MONGO_URI` con sus credenciales de Clever Cloud y MongoDB Atlas.

5.  **Preparar las Bases de Datos**
    * **PostgreSQL:** Conéctese a su base de datos de Clever Cloud y ejecute el script de la [Sección 7 (PostgreSQL Schema)].
    * **MongoDB:** Conéctese a su clúster de Atlas (usando `mongosh`) y ejecute los comandos de la [Sección 8 (MongoDB Commands)].

6.  **Ejecutar la Aplicación**
    ```bash
    python main.py
    ```

---

## 4. Explicación de la estructura de la base de datos

El sistema utiliza una arquitectura de datos híbrida con dos bases de datos en la nube.

### PostgreSQL (Clever Cloud)
Esta es la fuente de verdad para la autenticación y los datos del usuario.
* **Tabla: `usuarios`**
    * `id`: `SERIAL` (autoincremental) y Clave Primaria.
    * `username`: `VARCHAR(50)`, `UNIQUE`.
    * `email`: `VARCHAR(100)`, `UNIQUE`.
    * `password_hash`: `VARCHAR(255)`, almacena el hash de bcrypt.
    * `is_admin`: `BOOLEAN`, diferencia entre usuarios normales y administradores.

### MongoDB (Atlas)
Esta base de datos cumple dos funciones: auditoría y redundancia de datos.
* **Colección: `usuarios`**
    * Almacena una copia de los datos del usuario (`username`, `email`, `pg_id`, etc.)
    * Se crean índices únicos en `username` y `email` para mantener la integridad de los datos, reflejando el esquema de SQL.
* **Colección: `logs`**
    * Esta es la colección de auditoría. Cada vez que ocurre un evento importante (login, logout, registro), se inserta un documento con:
        * `usuario_id` (o `null` si es anónimo)
        * `accion` (ej. "login_exitoso")
        * `fecha` (Timestamp)
        * `ip`

---

## 5. Decisiones de diseño tomadas

* **Pivote a PostgreSQL:** Aunque el examen mencionaba MySQL, se tomó la decisión estratégica de usar PostgreSQL. Postgres es generalmente preferido en entornos de gran escala (FAANG) por su robustez, extensibilidad y características avanzadas de tipos de datos. La migración de `AUTO_INCREMENT` a `SERIAL` fue trivial.

* **Arquitectura Modular (Mixins):** El código se refactorizó de un script monolítico (`auth_system.py`) a un paquete `app/` modular.
    * `app/core.py`: Contiene la clase base (`AuthSystemCore`) que maneja el estado (conexiones de BD, sesión de usuario).
    * `app/mixin_*.py` (ahora `logging.py`, `ui.py`, etc.): Clases "Mixin" que inyectan funcionalidad específica (logs, UI, gestión de usuarios) en la clase base.
    * `app/system.py`: Ensambla la aplicación final (`SistemaAutenticacion`) a partir del Core y los Mixins. Esto proporciona una excelente Separación de Conceptos (SoC).

* **Estrategia de Doble Escritura (Dual-Write):** Para el registro de usuarios, el sistema escribe en Postgres *primero*. Si tiene éxito, escribe en MongoDB. Si Mongo falla, la transacción de Postgres se revierte (`rollback()`), evitando datos "fantasma" en la base de datos relacional.

* **Manejo de Conexiones en la Nube:** Las bases de datos en la nube (Clever Cloud, Atlas) tienen firewalls que cierran conexiones inactivas. Esto se manifestó como un `psycopg2.OperationalError` (stale connection). Se implementó un manejo de errores robusto (un `try-except` anidado) para que el `rollback()` no bloqueara la aplicación si la conexión ya estaba cerrada.

---

## 6. Dificultades encontradas y soluciones

* **Desafío:** Error de Handshake SSL de MongoDB (`[SSL: TLSV1_ALERT_INTERNAL_ERROR]`).
    * **Solución:** Este fue un problema de entorno. Se identificaron dos causas: (1) La IP del desarrollador no estaba en la lista blanca de Red de Atlas. (2) La versión de `pymongo` (3.12) estaba desactualizada y no soportaba los cifrados TLS modernos de Atlas. La solución fue **actualizar `pymongo`** y **añadir la IP `0.0.0.0/0`** (solo para desarrollo).

* **Desafío:** `Database objects do not implement truth value testing`.
    * **Solución:** El código `if not self.mongo_db:` es inválido para objetos de conexión. Se corrigió por la sintaxis explícita `if self.mongo_db is None:` en todos los archivos (ej. `logging.py`, `ui.py`).

* **Desafío:** `psycopg2.OperationalError: server closed the connection unexpectedly`.
    * **Solución:** Ocurría cuando la conexión a Clever Cloud se volvía inactiva (stale). La solución fue envolver la lógica de `rollback()` en `editar_perfil` dentro de su propio bloque `try-except` para evitar que la aplicación crasheara al intentar hacer `rollback` en una conexión ya cerrada.

---

## 7. Script del Esquema de PostgreSQL
```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE
);
```

---

## 8. Comandos MongoDB para Colecciones e Índices

Comandos para ejecutar en **mongosh**:

```js
// 1. Cambiar a la base de datos
use auth_system

// 2. Crear la colección 'usuarios' y sus índices únicos
db.createCollection("usuarios")
db.usuarios.createIndex({ "username": 1 }, { unique: true })
db.usuarios.createIndex({ "email": 1 }, { unique: true })

// 3. Crear la colección 'logs' y sus índices
db.createCollection("logs")
db.logs.createIndex({ "usuario_id": 1 })
db.logs.createIndex({ "fecha": -1 })
```

---

## 9. Archivo de configuración de ejemplo (.env)

Este es un archivo .env de ejemplo. Reemplace YOUR_VALUE_HERE con sus credenciales reales.

```env
POSTGRESQL_ADDON_URI="postgresql://YOUR_USER:YOUR_PASSWORD@YOUR_HOST:YOUR_PORT/YOUR_DB_NAME"

MONGO_URI="mongodb+srv://YOUR_USER:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/?retryWrites=true&w=majority"
```