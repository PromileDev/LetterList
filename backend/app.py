from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
import manageDB as db
from flask_cors import CORS

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
    db.add_product(data['name'], data['section'], data['website'])
    return jsonify({"message": "Product added successfully!"}), 201

@app.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    products = db.get_all_products()
    return jsonify(products), 200

# Obtener todos los productos de una sección específica (POST)
@app.route('/products_section', methods=['POST'])
@jwt_required()
def get_products_section():
    data = request.get_json()
    if not data or "section_id" not in data:
        return jsonify({"error": "El parámetro 'section_id' es obligatorio."}), 400
    
    try:
        products = db.get_all_products_by_section(data["section_id"])
        return jsonify(products), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los productos: {str(e)}"}), 500




## Operaciones con websites

# Añadir website
@app.route('/website', methods=['POST'])
@jwt_required()
def add_website():
    data = request.get_json()
    user_id = get_jwt_identity()    
    db.add_website(data['name'], user_id)
    return jsonify({"message": "Website added successfully!"}), 201

# Obtener websites
@app.route('/websites', methods=['GET'])
@jwt_required()
def get_websites():
    user_id = get_jwt_identity()
    print (user_id)
    websites = db.get_all_websites(user_id)
    return jsonify(websites), 200
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



# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True)
