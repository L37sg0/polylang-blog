from flask import Flask, render_template

def create_app():
    app = Flask(__name__, template_folder='views')
    app.secret_key = 'super-secret-key-change-me-later'
    # Конфигурация на базата данни
    app.config['DB_CONFIG'] = {
        'host': 'mysql',
        'user': 'dev',
        'password': 'password',
        'database': 'blog'
    }

    # Регистриране на рутовете (Blueprints)
    from app.routes.front import front_bp
    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp
            
    app.register_blueprint(front_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    
    
    # Глобален хендлър за 404 грешки
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    return app