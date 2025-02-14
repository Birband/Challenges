import numpy as np
from typing import Callable

METHODS = {
    "average": np.mean,
    "median": np.median,
    "max": np.max,
    "min": np.min
}

def block_processing(image_array : np.array, chunk_size: int = 8, method: Callable[[np.array], float] = np.mean) -> np.array:
    """
    Apply a method to each chunk of the image array

    :param image_array: The image array
    :param chunk_size: The size of the chunk
    :param method: The method to apply to each chunk

    :return: The processed image array
    """
    for i in range(0, image_array.shape[0], chunk_size):
        for j in range(0, image_array.shape[1], chunk_size):
            chunk = image_array[i:i+chunk_size, j:j+chunk_size]
            color = method(chunk, axis=(0, 1))
            image_array[i:i+chunk_size, j:j+chunk_size] = color
                
    return image_array