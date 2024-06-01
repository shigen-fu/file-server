from flask import Flask

from app.utils.utils import configure_logging, load_config


def create_app():
    app = Flask(__name__)
    config = load_config('app/config.yaml')
    app.config['SECRET_KEY'] = config['app']['secret_key']
    app.config['UPLOAD_FOLDER'] = config['app']['upload_folder']
    app.config['MAX_CONTENT_PATH'] = config['app']['max_content_path']
    app.config['DEBUG'] = config['app']['debug']

    configure_logging(config['logging']['level'], config['logging']['format'])

    from app.routes.auth import auth
    from app.routes.files import files
    app.register_blueprint(auth)
    app.register_blueprint(files)

    return app
