import os
import pathlib
import flask
from flask import Flask
from flask import current_app 
import click


from init import cors

from flask.cli import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


from config import ProductionConfig
from config import DevelopmentConfig
from config import TestingConfig


profiles = {
    'development': DevelopmentConfig(),
    'production': ProductionConfig(),
    'testing': TestingConfig()
}



def create_app(profile):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(profiles[profile])
    app.config.from_pyfile("config.py", silent=True)

    if profile != "testing":
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)

    try: # make sure the config folder exists
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.cli.command("greet", short_help="Greet Flask users")
    def greet():
        click.echo('Greetings Flask users all over the world!')
        return 0

    @app.shell_context_processor
    def shell():
        return {
            "x": 1,
            "y": 2,
            "z": 3
        }

    return app



flask_env = os.environ.get("FLASK_ENV", default="development")
app = create_app(flask_env)

if __name__ == '__main__':
    app.run()