
import numpy as np
from ntimage import core

__all__ = ['normalize',
           'clamp']


def normalize(image, min, max, dtype='float32'):
    """
    import ntimage as nt
    img = nt.load(nt.example_data('r16'))
    img2 = nt.normalize(img, 0, 1)
    """
    image = image.clone(dtype)
    array = image.numpy()
    minimum, maximum = np.min(array), np.max(array)
    m = (max - min) / (maximum - minimum)
    b = min - m * minimum
    new_array = m * array + b
    new_image = core.from_numpy_like(new_array, image)
    return new_image


def clamp(image, min, max):
    """
    import ntimage as nt
    img = nt.load(nt.example_data('r16'))
    img2 = nt.clamp(img, 5, 250)
    """
    array = image.numpy()
    array[array < min] = min
    array[array > max] = max
    new_image = core.from_numpy_like(array, image)
    return new_image