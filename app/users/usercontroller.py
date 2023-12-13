from app import  db
from flask import Blueprint, request, jsonify

from werkzeug.security import generate_password_hash
from flask_login import LoginManager, current_user, login_required, logout_user
from .pdf_processing import extract_info_from_pdf, save_file, check_comunas
from .auth import login

from .usermodel import User


userBp = Blueprint('user', __name__)   
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@userBp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return jsonify({'error': 'Email already in use'}), 400
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256') 
        new_user = User(
            email=data['email'],
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'New user created!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@userBp.route('/login', methods=['POST'])
def login_route():
    return login()

@userBp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'status': 'success'})

@userBp.route('/status')
@login_required
def status():
    user_id = current_user.id
    user = User.query.get(user_id)
    if user:
        return jsonify({'status': 'success', 'user': {'name': user.nombre, 'email': user.email}})
    else:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404



@userBp.route('/')
def index():
    return 'Hello, World!'

@userBp.route('/info', methods=['POST'])
def extract_info():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'})

    file = request.files['file']

    comunas =["ANDACOLLO","COQUIMBO","LA HIGUERA","LA SERENA","PAIHUANO","VICUÑA","COMBARBALA","MONTE PATRIA","OVALLE","PUNITAQUI", "RIO HURTADO","CANELA","ILLAPEL","LOS VILOS","SALAMANCA"]

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        pdf_path = "D:\\Users\\nicko\\Documents\\Cosas Cidere\\PDFS" + file.filename
        save_file(file, pdf_path)

        extracted_info, extracted_rut = extract_info_from_pdf(pdf_path)

        if check_comunas(extracted_info, comunas):
            return jsonify({'result': 'Approved', 'rut': extracted_rut})

        return jsonify({'result': 'Empresa fuera de region', 'rut': extracted_rut})