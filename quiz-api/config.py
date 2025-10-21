"""Configuration de l'application Flask."""
import os
from datetime import timedelta

class Config:
    """Configuration de base."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(BASE_DIR, 'quiz.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'Groupe 2')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Admin password (MD5 hash of "iloveflask")
    ADMIN_PASSWORD_HASH = b"\xd2x\x07{\xbf\xe7(Z\x14MK[\x11\xad\xb9\xcf"
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Rate limiting
    RATELIMIT_ENABLED = os.environ.get('RATELIMIT_ENABLED', 'False').lower() == 'true'
    RATELIMIT_DEFAULT = "100/hour"
    
    # Pagination
    DEFAULT_PAGE_SIZE = 50
    MAX_PAGE_SIZE = 100


class DevelopmentConfig(Config):
    """Configuration de développement."""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuration de production."""
    DEBUG = False
    TESTING = False
    RATELIMIT_ENABLED = True


class TestingConfig(Config):
    """Configuration de test."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Mapping des environnements
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env_name='default'):
    """Retourne la configuration selon l'environnement."""
    return config_by_name.get(env_name, DevelopmentConfig)

