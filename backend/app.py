from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
from manageDB import DatabaseManager
from flask_cors import CORS

# Configuración de la app Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["JWT_SECRET_KEY"] = "tu_clave_secreta_segura"  # Cambia esto por algo más seguro
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)
jwt = JWTManager(app)

# Instancia del gestor de base de datos
db = DatabaseManager()

# Rutas de autenticación
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    db.add_user(data['name'], data['lastname'], data['email'], data['password'])
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = db.get_user_by_email_and_password(data['email'], data['password'])
    if not user:
        return jsonify({"message": "Invalid credentials!"}), 401
    
    access_token = create_access_token(identity=user['id'])
    return jsonify({"access_token": access_token}), 200

# Ruta protegida
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

@app.route('/website', methods=['POST'])
@jwt_required()
def add_website():
    data = request.get_json()
    db.add_website(data['name'], data['user_id'])
    return jsonify({"message": "Website added successfully!"}), 201

@app.route('/websites', methods=['GET'])
@jwt_required()
def get_websites():
    user_id = get_jwt_identity()
    print (user_id)
    websites = db.get_all_websites(user_id)
    return jsonify(websites), 200

@app.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    user_id = get_jwt_identity()
    dashboard = db.get_dashboard(user_id)
    return jsonify(dashboard), 200

# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True)
