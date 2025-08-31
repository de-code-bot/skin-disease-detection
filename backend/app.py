from quart import Quart
from typing import Final

from backend.config.app_config import make_config
from backend.auxilary.utils import generic_error_handler

def create_app() -> Quart:
    '''Create an instance of the Quart app'''
    
    app: Final[Quart] = Quart(__name__)
    app.config.from_object(make_config())

    from backend.blueprints.model_blueprint import MODEL_BLUEPRINT
    from backend.blueprints.template_blueprint import TEMPLATES_BLUEPRINT
    app.register_blueprint(MODEL_BLUEPRINT, url_prefix='/'.join([app.config['APPLICATION_ROOT'], 'predictions']))
    app.register_blueprint(TEMPLATES_BLUEPRINT)     # Views will not have url prefix of /api/vx/...

    app.register_error_handler(Exception, generic_error_handler)

    return app