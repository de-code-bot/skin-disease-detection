from pathlib import Path
from typing import Final

from backend.auxilary.utils import generic_error_handler
from backend.background.runtime import model_swapper, database_batch_writer
from backend.config.app_config import ServerConfig
from backend.dependencies import initializers
from backend.dependencies.singleton_registry import SingletonRegistry

import keras

from quart import Quart

__all__ = ('create_app',)

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
    server_config.prepend_database_path(Path(app.instance_path))

    server_config.populate_classifier_types(SERVER_ROOT_DIRECTORY / 'classification' / 'categories.json')
    
    model_filepath: Final[Path] = Path(app.instance_path) / Path(server_config.classifier_h5_filename)
    image_classifier: Final[keras.Model] = initializers.init_image_classifier(model_filepath)

    singleton_registry: Final[SingletonRegistry] = SingletonRegistry(server_config=server_config,
                                                                     image_classifier=image_classifier)
    
    from backend.blueprints.model_blueprint import MODEL_BLUEPRINT
    from backend.blueprints.template_blueprint import TEMPLATES_BLUEPRINT
    # Register the prediction endpoint at /api/v1/predictions/
    app.register_blueprint(MODEL_BLUEPRINT, url_prefix='/api/v1/predictions')
    app.register_blueprint(TEMPLATES_BLUEPRINT)     # Views will not have url prefix of /api/vx/...

    # Inject default parameters for singletons
    for view, function in app.view_functions.items():
        if '.' in view:
            app.view_functions[view] = singleton_registry.inject_singletons(function)

    app.register_error_handler(Exception, generic_error_handler)

    # ASGI Lifecycle middleware
    @app.before_serving
    async def startup() -> None:
        app.add_background_task(model_swapper, model_filepath, image_classifier, server_config.model_swap_poll_interval)
        app.add_background_task(database_batch_writer,
                                server_config.database_filepath,
                                singleton_registry._db_entry_queue,
                                singleton_registry._db_entry_write_lock,
                                server_config.database_write_interval,
                                server_config.database_write_batch_size,
                                server_config.lock_contention_timeout)
    
    @app.after_serving
    async def shutdown() -> None:
        for task in app.background_tasks:
            task.cancel()

    return app