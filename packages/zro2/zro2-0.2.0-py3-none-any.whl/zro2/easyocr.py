import io
from typing import overload
import easyocr
import numpy

@overload
def get_text_coordinates(image: str, lang = ["en"]):
    ...

@overload
def get_text_coordinates(image: bytes, lang = ["en"]):
    ...

@overload
def get_text_coordinates(image: numpy.ndarray, lang = ["en"]):
    ...

@overload
def get_text_coordinates(image: io.BytesIO, lang = ["en"]):
    ...

def get_text_coordinates(image : str | bytes | numpy.ndarray | io.BytesIO, lang = ["en"]):

    reader = easyocr.Reader(lang)  # Initialize the EasyOCR reader for English
    if isinstance(image, bytes):
        image = io.BytesIO(image)

    result = reader.readtext(image)
    
    coordinates = []
    for detection in result:
        top_left = tuple(detection[0][0])
        bottom_right = tuple(detection[0][2])
        text = detection[1]
        confidence = detection[2]
        coordinates.append({
            'text': text,
            'confidence': confidence,
            'top_left': top_left,
            'bottom_right': bottom_right
        })
    
    return coordinates
