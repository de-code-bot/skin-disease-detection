'''Routes to expose the classification model'''

from typing import Any, Final

from backend.auxilary.decorators import enforce_mimetype

from quart import Blueprint, Response, request, current_app, jsonify

from werkzeug.datastructures import MultiDict

__all__ = ('MODEL_BLUEPRINT',
           'submit_prediction')

MODEL_BLUEPRINT: Final[Blueprint] = Blueprint("models_blueprint", "models_blueprint")

MODEL_BLUEPRINT.route('/', methods=['POST'])
@enforce_mimetype(current_app.config['ACCEPTED_IMAGE_MIMETYPE'])
async def submit_prediction() -> tuple[Response, int]:
    files: MultiDict = await request.files
    additional_kwargs: dict[str, str] = {}
    if len(files) > 1:
        additional_kwargs['file_quantity'] = "Only a single image accepted"

    image = files[0]
    
    # Some work that the model does idk

    response_data: dict[str, Any] = {'k' : 'v'}
    response_data['additional'] = additional_kwargs

    return (jsonify(response_data), 200)