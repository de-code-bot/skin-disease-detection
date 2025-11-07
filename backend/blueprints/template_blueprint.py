'''Routes to expose endpoints for serving HTML files'''

from typing import Final

from quart import Blueprint, render_template

__all__ = ('TEMPLATES_BLUEPRINT',
           'serve_index')

TEMPLATES_BLUEPRINT: Final[Blueprint] = Blueprint('templates_blueprint', 'templates_blueprint')

@TEMPLATES_BLUEPRINT.route('/')
async def serve_index() -> tuple[str, int]:
    return await render_template('index.html'), 200