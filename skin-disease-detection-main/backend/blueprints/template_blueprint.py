'''Routes to expose endpoints for serving HTML files'''

from typing import Final

from quart import Blueprint, render_template

__all__ = ('TEMPLATES_BLUEPRINT',
           'serve_splash',
           'serve_home',
           'serve_index',
           'serve_about',
           'serve_health')

TEMPLATES_BLUEPRINT: Final[Blueprint] = Blueprint('templates_blueprint', 'templates_blueprint')

@TEMPLATES_BLUEPRINT.route('/')
async def serve_splash() -> tuple[str, int]:
    return await render_template('splash.html'), 200

@TEMPLATES_BLUEPRINT.route('/home')
async def serve_home() -> tuple[str, int]:
    return await render_template('home.html'), 200

@TEMPLATES_BLUEPRINT.route('/analyze')
async def serve_index() -> tuple[str, int]:
    return await render_template('index.html'), 200

@TEMPLATES_BLUEPRINT.route('/about')
async def serve_about() -> tuple[str, int]:
    return await render_template('about.html'), 200

@TEMPLATES_BLUEPRINT.route('/health')
async def serve_health() -> tuple[str, int]:
    """Health check endpoint for debugging"""
    return '{"status": "healthy"}', 200
