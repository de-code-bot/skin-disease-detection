from pathlib import Path
from typing import Mapping, Final, Optional

import numpy as np
import keras
from keras.preprocessing.image import img_to_array, load_img
from keras.applications.vgg19 import preprocess_input

__all__ = ('make_prediction',)

def make_prediction(path: Path, model: keras.models.Model, classification_mapping: Mapping[int, str]) -> Optional[str]:
    img = load_img(path, target_size= (224,224))
    i = img_to_array(img)
    im = preprocess_input(i)
    assert isinstance(im, np.ndarray)
    img = np.expand_dims(im, axis = 0)
    prediction_index: Final[int] = int(np.argmax(model.predict(img)))

    if prediction_index not in classification_mapping:
        return None
    
    return classification_mapping[prediction_index]