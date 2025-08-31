'''Routes to expose the classification model'''

from typing import Any, Final

from quart import Blueprint, Response, request, jsonify

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

__all__ = ('MODEL_BLUEPRINT',
           'submit_prediction')

MODEL_BLUEPRINT: Final[Blueprint] = Blueprint("models_blueprint", "models_blueprint")

@MODEL_BLUEPRINT.route('/', methods=['POST'])
async def submit_prediction() -> tuple[Response, int]:
    files: dict[str, FileStorage] = dict(await request.files)
    if not files:
        raise BadRequest("Missing image for analysis")
    
    additional_kwargs: dict[str, str] = {}

    input_image: Final[FileStorage|None] = files.pop('image', None)
    if not input_image:
        raise BadRequest('Missing image for analysis. Required claim "image" missing')
    
    if files:
        additional_kwargs['file_quantity'] = f"Only a single image accepted, remaining {len(files)} ignored"
        del files
    
    # Some work that the model does idk

    response_data: dict[str, Any] = {'result' : '...', 'file' : input_image.filename}
    if additional_kwargs:
        response_data['additional'] = additional_kwargs

    return (jsonify(response_data), 200)