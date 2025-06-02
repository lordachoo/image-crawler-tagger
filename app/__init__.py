import os
from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.crawler import CrawlerManager

migrate = Migrate()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True,
                template_folder='../templates',
                static_folder='../static')
    
    # Load default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='postgresql://postgres:postgres@localhost/image_tagger',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        IMAGE_STORAGE_PATH=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'storage'),
    )

    # Load config from .env file if it exists
    if os.path.exists(os.path.join(os.path.dirname(app.instance_path), '.env')):
        from dotenv import load_dotenv
        load_dotenv(os.path.join(os.path.dirname(app.instance_path), '.env'))
        
        # Override with environment variables
        if os.environ.get('DATABASE_URL'):
            app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        if os.environ.get('SECRET_KEY'):
            app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        if os.environ.get('IMAGE_STORAGE_PATH'):
            app.config['IMAGE_STORAGE_PATH'] = os.environ.get('IMAGE_STORAGE_PATH')

    # If test config provided, use that instead
    if test_config is not None:
        app.config.update(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Ensure the storage directory exists
    try:
        os.makedirs(app.config['IMAGE_STORAGE_PATH'], exist_ok=True)
    except OSError:
        pass

    # Initialize the database
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize the crawler manager
    crawler_manager = CrawlerManager(app)
    app.crawler_manager = crawler_manager
    
    # Register routes
    from app.routes import main_bp, api_bp, crawl_bp, tag_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(crawl_bp, url_prefix='/crawl')
    app.register_blueprint(tag_bp, url_prefix='/tags')
    
    # Register custom commands
    from commands import register_commands
    register_commands(app)
    
    return app
