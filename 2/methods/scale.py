import numpy as np
from typing import Tuple, Optional

def scale_NN(image: np.array, size: Optional[Tuple[int, int]] = None, scale: float = None) -> np.array:
    """
    Resize an image using manual nearest-neighbor interpolation.

    :param image: The input image as a NumPy array.
    :param size: A tuple (new_width, new_height). Ignored if scale is provided.
    :param scale: A scaling factor for both width and height.
    
    :return: The resized image.
    """
    height, width = image.shape[:2]  # Correct order (height, width)

    if scale is not None:
        new_width = int(width * scale)
        new_height = int(height * scale)
        scale_x = width / new_width
        scale_y = height / new_height    
    elif size is not None:
        new_width, new_height = size
        scale_x = width / new_width
        scale_y = height / new_height
    else:
        raise ValueError("Either 'size' or 'scale' must be provided.")

    new_image = np.zeros((new_height, new_width, 3), dtype=np.uint8)

    for i in range(new_height):
        for j in range(new_width):
            src_x = min(int(j * scale_x), width - 1)
            src_y = min(int(i * scale_y), height - 1)
            new_image[i, j] = image[src_y, src_x]

    return new_image
