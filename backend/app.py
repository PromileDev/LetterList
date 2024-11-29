from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
import manageDB as db
from flask_cors import CORS
import clients, createPage
import os

# Configuración de la app Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["JWT_SECRET_KEY"] = "tu_clave_secreta_segura"  # Cambia esto por algo más seguro
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(days=1)
jwt = JWTManager(app)



# Rutas de autenticación
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if db.get_validated_register(data["email"]) == None:
        db.add_user(data['name'], data['lastname'], data['email'], data['password'])
        return jsonify({"message": "User registered successfully!"}), 201
    else:
        return jsonify({"message": "Email already registered!"}), 400
    
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = db.get_user_by_email_and_password(data['email'], data['password'])
    if not user:
        return jsonify({"message": "Invalid credentials!"}), 401
    
    access_token = create_access_token(identity=user['id'])
    return jsonify({"access_token": access_token}), 200

# Extraer token user
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = db.get_user_by_id(user_id)
    clients.new_client(user_id)
    return jsonify({
        "name": user['name'],
        "lastname": user['lastname'],
        "email": user['email']
        
        }), 200

# Operaciones con productos
@app.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    if not all(key in data for key in ["name", "price", "section_id", "website"]):
        return jsonify({"error": "Faltan campos necesarios para agregar el producto."}), 400
    try:
        db.add_product(data['name'], data['price'], data['section_id'], data['website'])
        return jsonify({"message": "Producto añadido correctamente."}), 201
    except Exception as e:
        return jsonify({"error": f"Error al añadir producto: {str(e)}"}), 500


@app.route('/products/list', methods=['POST'])
@jwt_required()
def get_products():
    # Obtener productos por id_page
    data = request.get_json()
    print("Datos recibidos para obtener productos:", data)  # Ver qué datos se están recibiendo

    id_page = data.get('id_page')
    if not id_page:
        return jsonify({"error": "El parámetro 'id_page' es obligatorio."}), 400

    try:
        products = db.get_all_products(id_page)  # Asegúrate que esta función esté funcionando correctamente
        
        if not products:
            return jsonify({"message": "No se encontraron productos."}), 404  # En caso de que no haya productos
        
        return jsonify(products), 200
    except Exception as e:
        print(f"Error al obtener productos: {str(e)}")  # Ver si ocurre algún error en la base de datos
        return jsonify({"error": "Error interno al obtener los productos."}), 500
    
# Borrar producto
@app.route('/product/delete', methods=['POST'])
@jwt_required()
def delete_product():
    data = request.get_json()
    if not data or "id" not in data:
        return jsonify({"error": "El parámetro 'id' es obligatorio."}), 400
    
    try:
        db.delete_product(data["id"])
        return jsonify({"message": "Producto eliminado exitosamente."}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el producto: {str(e)}"}), 500
    
# Editar producto
@app.route('/product/edit', methods=['POST'])
@jwt_required()
def edit_product():
    data = request.get_json()
    if not all(key in data for key in ["name", "price", "id"]):
        return jsonify({"error": "Faltan campos necesarios para editar el producto."}), 400
    
    try:
        db.edit_product(data["name"], data["price"], data["id"])
        return jsonify({"message": "Producto editado exitosamente."}), 200
    except Exception as e:
        return jsonify({"error": f"Error al editar el producto: {str(e)}"}), 500

## Operaciones con websites
# Añadir website
@app.route('/website', methods=['POST'])
@jwt_required()
def add_website():
    data = request.get_json()
    user_id = get_jwt_identity()    
    web_id = db.add_website(data['name'], user_id)
    clients.new_page(data['name'], user_id)
    astro_content = createPage.template1(data['name'])
    astro_file = os.path.join(os.path.dirname(__file__), "..", "frontend", "src", "pages", "clients", str(user_id), str(data["name"]), "index.astro")
    with open(astro_file, "w") as f:
        f.write(astro_content)
    return jsonify({"message": "Website added successfully!"}), 201

# Obtener websites
@app.route('/websites', methods=['GET'])
@jwt_required()
def get_websites():
    user_id = get_jwt_identity()
    websites = db.get_all_websites(user_id)
    return jsonify(websites), 200
# Borrar website
@app.route('/website/delete', methods=['POST'])
@jwt_required()
def delete_website():
    data = request.get_json()
    if not data or "id" not in data:
        return jsonify({"error": "No se pudo borrar la pagina"}), 400
    try:
        db.delete_website(data["id"])
        return jsonify({"message": "Delete successfully."}), 200
    except Exception as e:
        return jsonify({"error": f"An error has ocurred: {str(e)}"}), 500
#obtener una sola website
@app.route('/website/single', methods=['POST'])
@jwt_required()
def get_single_website():
    data = request.get_json()
    website = db.get_website(data['id_page'])
    return jsonify(website), 200

# Pagina de edicion de website
@app.route('/website_edit', methods=['POST'])
@jwt_required()
def get_website():
    data = request.get_json()
    website = db.get_website(data['id_page'])
    return jsonify(website), 200

# Obtener todas las secciones de una página (POST)
@app.route('/sections', methods=['POST'])
@jwt_required()
def get_sections():
    data = request.get_json()
    if not data or "id_page" not in data:
        return jsonify({"error": "El parámetro 'id_page' es obligatorio."}), 400
    
    try:
        sections = db.get_all_sections(data["id_page"])
        return jsonify(sections), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener las secciones: {str(e)}"}), 500
    
# Añadir sección a una página (POST)
@app.route('/section/add', methods=['POST'])
@jwt_required()
def add_section():
    data = request.get_json()
    if not all(key in data for key in ["name", "id_page"]):
        return jsonify({"error": "Faltan campos necesarios para agregar la sección."}), 400
    
    try:
        db.add_section(data["name"], data["id_page"])
        return jsonify({"message": "Sección agregada exitosamente."}), 201
    except Exception as e:
        return jsonify({"error": f"Error al agregar la sección: {str(e)}"}), 500


# Settings
@app.route("/settings", methods=['POST'])
@jwt_required()
def change_user():
    data = request.get_json()
    user_id = get_jwt_identity()
    user = db.get_user_by_email_and_password(data['email'], data['password'])
    if not user:
        return jsonify({"message": "Invalid credentials!"}), 401
    db.change_user(data['name'], data['lastname'], user_id)
    return jsonify({"message": "User changed successfully!"}), 201

#get id
@app.route("/user/website", methods=['POST'])
@jwt_required()
def get_id():
    user_id = get_jwt_identity()
    data = request.get_json()
    name = db.get_website(data['id_page'])
    name = name['name']
    return jsonify({"id": user_id, "name": name}), 200

# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True)
