import sqlite3

# Crear o conectar a la base de datos
conn = sqlite3.connect('letterlist.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Crear tabla 'users'
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Crear tabla 'websites'
cursor.execute('''
CREATE TABLE IF NOT EXISTS websites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

# Crear tabla 'products'
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    section TEXT NOT NULL,
    website INTEGER NOT NULL,
    FOREIGN KEY (website) REFERENCES websites(id)
)
''')

# Guardar los cambios
conn.commit()

# Cerrar la conexión
conn.close()

class DatabaseManager:
    def __init__(self, database='letterlist.db'):
        self.database = database

    def query(self, query, args=(), one=False, commit=False):
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, args)
        if commit:
            conn.commit()
            conn.close()
            return
        rv = cursor.fetchall()
        conn.close()
        return (rv[0] if rv else None) if one else rv

    def add_user(self, name, lastname, email, password):
        self.query(
            "INSERT INTO users (name, lastname, email, password) VALUES (?, ?, ?, ?)",
            (name, lastname, email, password),
            commit=True
        )

    def get_user_by_email_and_password(self, email, password):
        return self.query(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password),
            one=True
        )

    def get_user_by_id(self, user_id):
        return self.query(
            "SELECT * FROM users WHERE id = ?",
            (user_id,),
            one=True
        )

    def add_product(self, name, section, website):
        self.query(
            "INSERT INTO products (name, section, website) VALUES (?, ?, ?)",
            (name, section, website),
            commit=True
        )

    def get_all_products(self):
        products = self.query("SELECT * FROM products")
        return [dict(row) for row in products]
    
    def add_website(self, name, user_id):
        self.query(
            "INSERT INTO websites (name, user_id) VALUES (?, ?)",
            (name, user_id),
            commit=True
        )

    def get_all_websites(self, user_id):
        websites = self.query("SELECT * FROM websites where user_id = ?", (user_id,))
        return [dict(row) for row in websites]