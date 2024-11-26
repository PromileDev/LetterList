import sqlite3

DATABASE = 'letterlist.db'

def create_tables():
    conn = sqlite3.connect(DATABASE)
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

    # Crear tabla 'sections'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        website_id INTEGER NOT NULL,
        FOREIGN KEY (website_id) REFERENCES websites(id)
    )
    ''')

    # Crear tabla 'templates'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        img TEXT NOT NULL
    )
    ''')
                   

    # Crear tabla 'websites'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS websites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        template_id INTEGER,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (template_id) REFERENCES templates(id)
    )
    ''')

    # Crear tabla 'products'
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price FLOAT NOT NULL,
        website INTEGER NOT NULL,
        section_id INTEGER, 
        FOREIGN KEY (website) REFERENCES websites(id),
        FOREIGN KEY (section_id) REFERENCES sections(id)
    )
    ''')

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

def query(query, args=(), one=False, commit=False):
    conn = sqlite3.connect(DATABASE)
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

def add_user(name, lastname, email, password):
    query(
        "INSERT INTO users (name, lastname, email, password) VALUES (?, ?, ?, ?)",
        (name, lastname, email, password),
        commit=True
    )

def get_user_by_email_and_password(email, password):
    return query(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (email, password),
        one=True
    )

def get_user_by_id(user_id):
    return query(
        "SELECT * FROM users WHERE id = ?",
        (user_id,),
        one=True
    )

def add_product(name, price, section_id, website):
    query(
        "INSERT INTO products (name, price, section_id, website) VALUES (?, ?, ?,?)",
        (name, price, section_id, website),
        commit=True
    )

def get_all_products(id_page):
    products = query("SELECT * FROM products WHERE website = ?", (id_page,))
    return [dict(row) for row in products]  # Convertir cada fila en un diccionario

def add_website(name, user_id):
    query(
        "INSERT INTO websites (name, user_id) VALUES (?, ?)",
        (name, user_id),
        commit=True
    )

def get_all_websites(user_id):
    websites = query("SELECT * FROM websites where user_id = ?", (user_id,))
    return [dict(row) for row in websites]

def get_website(id_page):
    row =  query(
        "SELECT * FROM websites WHERE id = ?",
        (id_page,),
        one=True
    )
    return dict(row)

def add_section(name, website_id):
    query(
        "INSERT INTO sections (name, website_id) VALUES (?, ?)",
        (name, website_id),
        commit=True
    )

def add_section_product(section_id, product_id):
    query(
        "UPDATE products SET section = ? WHERE id = ?", (section_id, product_id),
        commit=True
    )

def get_all_sections(website_id):
    sections = query("SELECT * FROM sections where website_id = ?", (website_id,))
    return [dict(row) for row in sections]

def get_all_products_by_section(section):
    products = query("SELECT * FROM products where section = ?", (section,))
    return [dict(row) for row in products]

def get_all_products_by_website(website_id):
    products = query("SELECT * FROM products where website = ?", (website_id,))
    return [dict(row) for row in products]

def get_validated_register(email):
    return query(
        "SELECT * FROM users WHERE email = ?",
        (email,),
        one=True
    )

def change_user(name, lastname, user_id):
    query(
        "UPDATE users SET name = ?, lastname = ? WHERE id = ?",
        (name, lastname, user_id),
        commit=True
    )

create_tables()