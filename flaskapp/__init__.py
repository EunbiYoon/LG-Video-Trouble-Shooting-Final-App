
import os

from dotenv import load_dotenv

dotenv_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    '.env'
)

load_dotenv(dotenv_path=dotenv_path, verbose=True)

from flask import Flask, render_template

from flask_migrate import Migrate

migrate = Migrate()

def handle_404(e):
    return render_template('404.html'), 404

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
        SQLALCHEMY_DATABASE_URI=os.environ['SQLALCHEMY_DATABASE_URI'],
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
    app.register_error_handler(404, handle_404)
    
    from flaskapp.models import db 
    db.init_app(app)
    
    migrate.init_app(app, db)
    
    from flaskapp import action
    
    app.register_blueprint(action.bp)
    
    
    import requests
    
    @app.context_processor
    def instance_id():
        instance_id = ''
        try:
            response = requests.get('http://169.254.169.254/latest/meta-data/instance-id/', timeout=3)
            instance_id = response.content.decode('utf-8')
        except:
            pass
        return dict(instance_id=instance_id)
    
    return app

