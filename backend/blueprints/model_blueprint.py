'''Routes to expose the classification model'''

from typing import Any, Final

from backend.auxilary.decorators import enforce_mimetype

from quart import Blueprint, Response, request, current_app, jsonify

from werkzeug.datastructures import MultiDict, FileStorage

__all__ = ('MODEL_BLUEPRINT',
           'submit_prediction')

MODEL_BLUEPRINT: Final[Blueprint] = Blueprint("models_blueprint", "models_blueprint")

MODEL_BLUEPRINT.route('/', methods=['POST'])
async def submit_prediction() -> tuple[Response, int]:
    files: MultiDict[str, FileStorage] = await request.files
    additional_kwargs: dict[str, str] = {}
    
    if len(files) > 1:
        additional_kwargs['file_quantity'] = "Only a single image accepted"

    input_file: Final[FileStorage] = next(iter(files.values()))
    image_bytes: Final[bytes] = await input_file.read()
    
    # Some work that the model does idk

    response_data: dict[str, Any] = {'k' : 'v'}
    if additional_kwargs:
        response_data['additional'] = additional_kwargs

    return (jsonify(response_data), 200)