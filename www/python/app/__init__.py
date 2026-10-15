from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Конфигурация на базата данни
    app.config['DB_CONFIG'] = {
        'host': 'mysql',
        'user': 'dev',
        'password': 'password',
        'database': 'blog'
    }

    # Регистриране на рутовете (Blueprints)
    from app.routes.front import front_bp
    app.register_blueprint(front_bp)
    
    return app