use auth_system

db.createCollection("usuarios")

db.usuarios.createIndex({ "username": 1 }, { unique: true })
db.usuarios.createIndex({ "email": 1 }, { unique: true })

db.createCollection("logs")

db.logs.createIndex({ "usuario_id": 1 })
db.logs.createIndex({ "fecha": -1 })