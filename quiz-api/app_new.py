"""Application Flask restructurée - Point d'entrée principal."""
from flask import Flask
from flask_cors import CORS
from config import get_config
from models import db
import os


def create_app(config_name='default'):
    """Factory pour créer l'application Flask."""
    app = Flask(__name__)
    
    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.quiz_routes import quiz_bp
    from routes.question_routes import question_bp
    from routes.attempt_routes import attempt_bp
    from routes.leaderboard_routes import leaderboard_bp
    from routes.admin_routes import admin_bp
    from routes.legacy_routes import legacy_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(quiz_bp, url_prefix='/api/quizzes')
    app.register_blueprint(question_bp, url_prefix='/api/questions')
    app.register_blueprint(attempt_bp, url_prefix='/api/attempts')
    app.register_blueprint(leaderboard_bp, url_prefix='/api/leaderboard')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(legacy_bp, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Root route
    @app.route('/')
    def index():
        return {
            'message': 'Quiz API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth/login',
                'quizzes': '/api/quizzes',
                'questions': '/api/questions',
                'attempts': '/api/attempts',
                'leaderboard': '/api/leaderboard/<quiz_id>'
            }
        }
    
    # Health check
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    # Debug: list routes
    @app.route('/routes')
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': sorted(list(rule.methods - set(['HEAD', 'OPTIONS']))),
                'rule': str(rule)
            })
        routes.sort(key=lambda r: r['rule'])
        return {'routes': routes}, 200
    
    return app


if __name__ == '__main__':
    env = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env)
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)

