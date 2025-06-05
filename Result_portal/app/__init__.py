from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap()
migrate = Migrate()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    
    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.student import bp as student_bp
    app.register_blueprint(student_bp, url_prefix='/student')
    
    # Create default levels if they don't exist
    with app.app_context():
        from app.models import Level, Program
        
        # Create default levels if they don't exist
        default_levels = ['100', '200', '300', '400', '500', '600', '700', '800']
        for level_name in default_levels:
            level = Level.query.filter_by(name=level_name).first()
            if not level:
                level = Level(name=level_name, description=f'Level {level_name}')
                db.session.add(level)
        
        # Create a default program if none exists
        if Program.query.count() == 0:
            program = Program(name='Computer Science', description='Default program')
            db.session.add(program)
        
        db.session.commit()
    
    @app.route("/")
    def index():
        return render_template('index.html')
    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {'now': datetime.now()}

    return app

from app import models
