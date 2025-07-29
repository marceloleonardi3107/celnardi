import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS

# Importar todos os modelos primeiro
from src.models.user import db, User
from src.models.module import Module, Lesson, MediaFile
from src.models.quiz import Quiz, Question, QuizAttempt, QuizAnswer
from src.models.progress import UserProgress, UserCertificate, UserActivity

# Importar todas as rotas
from src.routes.user import user_bp
from src.routes.modules import modules_bp
from src.routes.quiz import quiz_bp
from src.routes.upload import upload_bp

# Criar aplicação Flask como API pura
app = Flask(__name__)
app.config['SECRET_KEY'] = 'amar_assist_api_secret_key_2024'

# Configurar CORS para permitir requisições de qualquer origem
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Registrar blueprints com prefixo /api
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(modules_bp, url_prefix='/api')
app.register_blueprint(quiz_bp, url_prefix='/api')
app.register_blueprint(upload_bp, url_prefix='/api')

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração para upload de arquivos
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

# Criar pasta de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializar banco de dados
db.init_app(app)
with app.app_context():
    db.create_all()
    
    # Criar dados iniciais se não existirem (comentado temporariamente)
    # try:
    #     from src.utils.seed_data import create_initial_data
    #     create_initial_data()
    # except ImportError:
    #     print("Seed data module not found, skipping initial data creation")

# Rota de health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Amar Assist Training API is running',
        'version': '1.0'
    })

# Rota raiz da API
@app.route('/api', methods=['GET'])
def api_info():
    return jsonify({
        'name': 'Amar Assist Training API',
        'version': '1.0',
        'description': 'API para Sistema de Treinamento de Vendas da Amar Assist',
        'endpoints': {
            'health': '/api/health',
            'users': '/api/users',
            'modules': '/api/modules',
            'quiz': '/api/quiz',
            'upload': '/api/upload'
        }
    })

# Handler para CORS preflight
@app.before_request
def handle_preflight():
    from flask import request
    if request.method == "OPTIONS":
        response = jsonify({'status': 'ok'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

# Handler de erro global
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'The requested API endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

