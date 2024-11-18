import sqlite3

# Crear o conectar a la base de datos
conn = sqlite3.connect('backend/letterlist.db')

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

#Crear tabla 'sections'
cursor.execute('''
CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    website_id INTEGER NOT NULL,
    FOREIGN KEY (website_id) REFERENCES websites(id)
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
    price float NOT NULL,
    website INTEGER NOT NULL,
    section_id INTEGER, 

    FOREIGN KEY (website) REFERENCES websites(id),
    FOREIGN KEY (section_id) REFERENCES sections(id)
               
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
    
    def add_section(self, name, website_id):
        self.query(
            "INSERT INTO sections (name, website_id) VALUES (?, ?)",
            (name, website_id),
            commit=True
        )
    
    def add_section_product(self, section_id, product_id):
        self.query(
            "UPDATE products SET section = ? WHERE id = ?", (section_id, product_id),
            commit=True
        )

    def get_all_sections(self, website_id):
        sections = self.query("SELECT * FROM sections where website_id = ?", (website_id,))
        return [dict(row) for row in sections]
    
    def get_all_products_by_section(self, section):
        products = self.query("SELECT * FROM products where section = ?", (section,))
        return [dict(row) for row in products]
    
    def get_all_products_by_website(self, website_id):
        products = self.query("SELECT * FROM products where website = ?", (website_id,))
        return [dict(row) for row in products]
    

    




