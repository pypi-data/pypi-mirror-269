import itk
import numpy as np

from ntimage import core
from ..utils.datatypes import to_ptype

__all__ = [
    'from_itk',
    'from_numpy',
    'from_numpy_like',
    'ones',
    'ones_like',
    'zeros',
    'zeros_like',
    'rand',
    'rand_like',
    'randint',
    'randint_like',
    'clone'
]

def from_itk(image):
    return core.NTImage(image)

def from_numpy(arr, origin=None, spacing=None, direction=None, is_vector=False):
    """
    Examples
    --------
    >>> import ntimage as nt
    >>> import numpy as np
    >>> img = nt.from_numpy(np.random.randn(128,128))
    """
    # bool is not supported by itk
    if arr.dtype == 'bool':
        arr = arr.astype('uint8')
        
    itk_image = itk.GetImageFromArray(np.ascontiguousarray(arr), is_vector=is_vector)
    image = from_itk(itk_image)
    
    if origin is not None:
        image.set_origin(origin)
    if spacing is not None:
        image.set_spacing(spacing)
    if direction is not None:
        image.set_direction(direction)
        
    return image


def from_numpy_like(arr, image):
    """
    import ntimage as nt
    img = nt.load(nt.example_data('r16'))
    img.set_spacing((2,2))
    arr = img.numpy() * 10
    img2 = nt.from_numpy_like(arr, img)
    nt.consistent(img, img2)
    """
    return from_numpy(arr,
                      origin=image.origin,
                      spacing=image.spacing,
                      direction=image.direction,
                      is_vector=image.components > 1)


def ones(shape, dtype=None):
    arr = np.ones(shape, dtype)
    return from_numpy(arr)

def ones_like(image):
    arr = np.ones(image.shape, dtype=image.dtype)
    return from_numpy_like(arr, image)

def zeros(shape, dtype=None):
    arr = np.zeros(shape, dtype)
    return from_numpy(arr)

def zeros_like(image):
    arr = np.zeros(image.shape, image.dtype)
    return from_numpy_like(arr, image)

def rand(shape):
    """
    Returns float values between 0 and 1
    """
    arr = np.random.random(shape, dtype='float32')
    return from_numpy(arr)

def rand_like(image):
    arr = np.random.random(image.shape, dtype='float32')
    return from_numpy(arr)

def randint(low, high, shape):
    arr = np.random.randint(low, high, shape)
    return from_numpy(arr)

def randint_like(low, high, image):
    arr = np.random.randint(low, high, image.shape)
    return from_numpy_like(arr, image)

def clone(image, dtype=None):
    
    if dtype is None:
        dtype = image.dtype
        
    itk_image = image._image
    
    OutputPixelType = itk.ctype(to_ptype(dtype))
    Dimension = image.dimension
    OutputImageType = itk.Image[OutputPixelType, Dimension]
    
    castImageFilter = itk.CastImageFilter[itk_image, OutputImageType].New()
    castImageFilter.SetInput(itk_image)
    castImageFilter.Update()
    new_itk_image = castImageFilter.GetOutput()
    
    new_image = from_itk(new_itk_image)
    return new_image