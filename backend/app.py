from quart import Quart
from pathlib import Path
from typing import Final

from backend.auxilary.utils import generic_error_handler
from backend.config.app_config import ServerConfig

from backend.dependencies.singleton_registry import SingletonRegistry
from backend.dependencies import initializers

import keras

def create_app() -> Quart:
    '''Create an instance of the Quart app'''
    SERVER_ROOT_DIRECTORY: Final[Path] = Path(__file__).parent
    
    app: Final[Quart] = Quart(__name__,
                              root_path=str(SERVER_ROOT_DIRECTORY),
                              instance_path=str(SERVER_ROOT_DIRECTORY / 'instance'))
    app.config.from_object(initializers.init_app_config(SERVER_ROOT_DIRECTORY / 'config' / 'app_config.toml'))

    # Initialize global singletons
    server_config: Final[ServerConfig] = initializers.init_server_config(SERVER_ROOT_DIRECTORY / 'config' / 'server_config.toml')
    server_config.prepend_bucket_path(Path(app.instance_path))
    server_config.populate_classifier_types(SERVER_ROOT_DIRECTORY / 'classification' / 'categories.json')
    
    image_classifier: Final[keras.Model] = initializers.init_image_classifier(Path(app.instance_path) / Path(server_config.classifier_h5_filename))

    singleton_registry: Final[SingletonRegistry] = SingletonRegistry(server_config=server_config,
                                                                     image_classifier=image_classifier)
    
    from backend.blueprints.model_blueprint import MODEL_BLUEPRINT
    from backend.blueprints.template_blueprint import TEMPLATES_BLUEPRINT
    app.register_blueprint(MODEL_BLUEPRINT, url_prefix='/'.join([app.config['APPLICATION_ROOT'], 'predictions']))
    app.register_blueprint(TEMPLATES_BLUEPRINT)     # Views will not have url prefix of /api/vx/...

    # Inject default parameters for singletons
    for view, function in app.view_functions.items():
        if '.' in view:
            app.view_functions[view] = singleton_registry.inject_singletons(function)

    app.register_error_handler(Exception, generic_error_handler)

    return app