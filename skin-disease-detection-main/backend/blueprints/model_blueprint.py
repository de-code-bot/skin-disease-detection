'''Routes to expose the classification model'''

import time
from datetime import datetime
from pathlib import Path
from typing import Any, Final
from uuid import uuid4

from backend.classification.predictions import make_prediction
from backend.dependencies.singleton_types import ServerConfigurationType, AppImageClassifierType, DatabaseEntryQueueType

from quart import Blueprint, Response, request, jsonify

from quart.datastructures import FileStorage
from werkzeug.exceptions import BadRequest

__all__ = ('MODEL_BLUEPRINT',
           'submit_prediction')

MODEL_BLUEPRINT: Final[Blueprint] = Blueprint("models_blueprint", "models_blueprint")

@MODEL_BLUEPRINT.route('/', methods=['POST'])
@MODEL_BLUEPRINT.route('', methods=['POST'])
async def submit_prediction(server_config: ServerConfigurationType, image_classifier: AppImageClassifierType, db_queue: DatabaseEntryQueueType) -> tuple[Response, int]:
    try:
        # Log incoming request details
        client_ip = request.remote_addr
        print("\n" + "=" * 70)
        print("🔔 PREDICTION REQUEST RECEIVED FROM PHONE!")
        print("=" * 70)
        print(f"📱 Client IP: {client_ip}")
        print(f"🕐 Time: {datetime.now()}")
        print(f"📝 Method: {request.method}")
        print(f"🔗 Path: {request.path}")
        print(f"📋 Content-Type: {request.content_type}")
        print(f"📋 Content-Length: {request.content_length}")
        print(f"📋 Headers: {dict(request.headers)}")

        files: dict[str, FileStorage] = dict(await request.files)
        print(f"📦 Files in request: {list(files.keys())}")
        print(f"📦 Number of files: {len(files)}")

        if not files:
            print("❌ ERROR: No files in request!")
            raise BadRequest("Missing image for analysis")

        additional_kwargs: dict[str, str] = {}

        input_image: Final[FileStorage|None] = files.pop('image', None)
        if not input_image:
            print("❌ ERROR: No 'image' field in request!")
            raise BadRequest('Missing image for analysis. Required claim "image" missing')

        print(f"✅ Image received: {input_image.filename}")
        # Read image data once to check size
        image_data = input_image.read()
        print(f"✅ Image size: {len(image_data)} bytes")
        input_image.seek(0)  # Reset file pointer

        if files:
            additional_kwargs['file_quantity'] = f"Only a single image accepted, remaining {len(files)} ignored"
            del files

        # Create filename with disease name and datetime
        current_datetime = datetime.now()
        datetime_str = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
        timestamp = str(time.time()).replace('.', '_')

        # Save temporarily with unique name to make prediction first
        temp_filename = f"temp_{timestamp}.jpg"
        temp_path: Final[Path] = server_config.image_bucket / temp_filename

        await input_image.save(destination=temp_path,
                               buffer_size=server_config.image_download_buffer_size)

        print(f"💾 Image saved temporarily to: {temp_path}")

        # Make prediction to get the disease name
        print("🤖 Running model prediction...")
        classification: str = make_prediction(temp_path, image_classifier, server_config.classifier_types) or 'N/A'
        print(f"✅ Prediction result: {classification}")

        # Get original file extension
        original_extension = Path(input_image.filename).suffix if input_image.filename else '.jpg'

        # Clean classification name for filename
        safe_classification = classification.replace('/', '-').replace('\\', '-').replace(':', '-')

        # New filename format: DiseaseName_YYYY-MM-DD_HH-MM-SS.jpg
        new_filename = f"{safe_classification}_{datetime_str}{original_extension}"
        destination_path: Final[Path] = server_config.image_bucket / new_filename

        # Handle duplicate filenames
        if destination_path.exists():
            new_filename = f"{safe_classification}_{datetime_str}_{timestamp}{original_extension}"
            destination_path = server_config.image_bucket / new_filename

        # Rename the temporary file
        try:
            temp_path.rename(destination_path)
        except Exception as e:
            import shutil
            shutil.move(str(temp_path), str(destination_path))

        db_queue.push_entry(destination_path.stem, destination_path.suffix, destination_path, classification, current_datetime)

        response_data: dict[str, Any] = {'result' : classification, 'file' : input_image.filename}
        if additional_kwargs:
            response_data['additional'] = additional_kwargs

        print(f"✅ RESPONSE SENT: {response_data}")
        print("=" * 70 + "\n")
        return jsonify(response_data), 200

    except BadRequest as e:
        print(f"❌ BadRequest error: {str(e)}")
        print("=" * 70 + "\n")
        raise
    except Exception as e:
        print(f"❌ ERROR in prediction endpoint: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        print("=" * 70 + "\n")
        raise BadRequest(f"Error processing image: {str(e)}")
