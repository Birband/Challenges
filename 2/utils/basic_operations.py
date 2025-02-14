import pathlib
from PIL import Image
import numpy as np

INPUT_FOLDER = pathlib.Path("INPUT")
OUTPUT_FOLDER = pathlib.Path("OUTPUT")

def initialize_directories() -> None:
    INPUT_FOLDER.mkdir(exist_ok=True)
    OUTPUT_FOLDER.mkdir(exist_ok=True)


def load_image(image_name : str) -> Image:
    image_path = INPUT_FOLDER / image_name
    if not image_path.exists():
        raise FileNotFoundError(f"Image {image_name} not found")
    
    image = Image.open(image_path)
    return image
    
def prepare_image(image : Image) -> np.array:
    image = image.convert("RGB")
    image_array = np.array(image)
    return image_array

def save_image(image_array : np.array, filename: str) -> None:
    image = Image.fromarray(image_array)
    image.save(OUTPUT_FOLDER / filename)