#!/usr/bin/env python3
"""
Archivo de Configuración para Figma Analytics Web App
=====================================================

Configuraciones por defecto y variables de entorno para la aplicación web.
"""

import os
from datetime import datetime, timedelta

class Config:
    """Configuración base de la aplicación"""
    
    # Configuración básica
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'figma_analytics_2025_secret_key'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Configuración del servidor
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # Configuración de la API de Figma
    FIGMA_API_BASE_URL = "https://www.figma.com/api/v1/analytics/libraries"
    FIGMA_API_TIMEOUT = int(os.environ.get('FIGMA_API_TIMEOUT', 30))
    
    # Configuración de archivos temporales
    TEMP_DIR = os.environ.get('TEMP_DIR') or os.path.join(os.getcwd(), 'temp')
    MAX_FILE_SIZE = int(os.environ.get('MAX_FILE_SIZE', 100)) * 1024 * 1024  # 100MB
    
    # Configuración de fechas por defecto
    DEFAULT_START_DATE = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    DEFAULT_END_DATE = datetime.now().strftime('%Y-%m-%d')
    
    # Configuración de validación
    MIN_DATE = '2020-01-01'
    MAX_DATE_RANGE_DAYS = int(os.environ.get('MAX_DATE_RANGE_DAYS', 1095))  # 3 años
    
    # Configuración de paginación
    DEFAULT_PAGE_SIZE = int(os.environ.get('DEFAULT_PAGE_SIZE', 100))
    MAX_PAGE_SIZE = int(os.environ.get('MAX_PAGE_SIZE', 1000))
    
    # Configuración de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'figma_analytics.log')
    
    # Configuración de seguridad
    MAX_REQUESTS_PER_MINUTE = int(os.environ.get('MAX_REQUESTS_PER_MINUTE', 60))
    SESSION_TIMEOUT = int(os.environ.get('SESSION_TIMEOUT', 3600))  # 1 hora
    
    @staticmethod
    def init_app(app):
        """Inicializa la configuración en la aplicación Flask"""
        # Crear directorio temporal si no existe
        if not os.path.exists(Config.TEMP_DIR):
            os.makedirs(Config.TEMP_DIR)
        
        # Configurar logging
        import logging
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    # En producción, usar variables de entorno para secretos
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY debe estar configurado en producción")

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DEBUG = True
    TEMP_DIR = os.path.join(os.getcwd(), 'test_temp')

# Mapeo de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Obtiene la configuración basada en el entorno"""
    config_name = os.environ.get('FLASK_ENV', 'default')
    return config.get(config_name, config['default'])
