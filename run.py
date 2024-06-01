from app import create_app
from app.utils.utils import load_config

config = load_config('app/config.yaml')
app = create_app()

if __name__ == '__main__':
    app.run(host=config['server']['host'], port=config['server']
            ['port'], debug=config['app']['debug'])
