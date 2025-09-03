'''Routes to expose the classification model'''

import time
from pathlib import Path
from typing import Any, Final
from uuid import uuid4

from backend.singletons import server_config, image_classifier
from backend.auxilary.decorators import enforce_mimetype
from backend.classification.predictions import make_prediction

from quart import Blueprint, Response, request, jsonify

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

# Runtime import checks (this is so scuffed, I deserve to be put down)
assert server_config is not None
assert image_classifier is not None

__all__ = ('MODEL_BLUEPRINT',
           'submit_prediction')

MODEL_BLUEPRINT: Final[Blueprint] = Blueprint("models_blueprint", "models_blueprint")

@MODEL_BLUEPRINT.route('/', methods=['POST'])
@enforce_mimetype(type_=server_config.form_mimetype, subtype=server_config.form_subtype)
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
    
    destination_path: Final[Path] = server_config.image_bucket / '_'.join([str(time.time()), input_image.filename or uuid4().hex])
    await input_image.save(dst=destination_path,
                           buffer_size=server_config.image_download_buffer_size)

    classification: str = make_prediction(destination_path, image_classifier, server_config.classifier_types) or 'N/A'

    response_data: dict[str, Any] = {'result' : classification, 'file' : input_image.filename}
    if additional_kwargs:
        response_data['additional'] = additional_kwargs

    return jsonify(response_data), 200