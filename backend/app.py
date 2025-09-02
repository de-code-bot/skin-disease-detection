from quart import Quart
from pathlib import Path
from typing import Final

from backend.auxilary.utils import generic_error_handler
from backend.config.app_config import ServerConfig

from backend import bootup

def create_app() -> Quart:
    '''Create an instance of the Quart app'''
    SERVER_ROOT_DIRECTORY: Final[Path] = Path(__file__).parent
    
    app: Final[Quart] = Quart(__name__,
                              root_path=str(SERVER_ROOT_DIRECTORY),
                              instance_path=str(SERVER_ROOT_DIRECTORY / 'instance'))
    app.config.from_object(bootup.init_app_config(SERVER_ROOT_DIRECTORY / 'config' / 'app_config.toml'))

    # Initialize global singletons
    server_config: Final[ServerConfig] = bootup.init_server_config(SERVER_ROOT_DIRECTORY / 'config' / 'server_config.toml')
    
    bootup.init_image_classifier(Path(app.instance_path) / Path(server_config.classifier_h5_filename))
    
    from backend.blueprints.model_blueprint import MODEL_BLUEPRINT
    from backend.blueprints.template_blueprint import TEMPLATES_BLUEPRINT
    app.register_blueprint(MODEL_BLUEPRINT, url_prefix='/'.join([app.config['APPLICATION_ROOT'], 'predictions']))
    app.register_blueprint(TEMPLATES_BLUEPRINT)     # Views will not have url prefix of /api/vx/...

    app.register_error_handler(Exception, generic_error_handler)

    return app