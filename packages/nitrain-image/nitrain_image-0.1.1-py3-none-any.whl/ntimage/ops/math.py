import numpy as np
from ntimage.core.ntimage import NTImage
from ntimage.core.create import from_numpy_like
from ntimage.utils.methods import add_method

__all__ = [
    'abs',
    'ceil',
    'floor',
    'max',
    'min',
    'mean',
    'median',
    'sum',
    'std',
    'unique',
    'log',
    'exp',
    'sqrt',
    'power'
]

@add_method(NTImage)
def abs(image):
    arr = image.numpy()
    return np.abs(arr)
    
@add_method(NTImage)
def ceil(image):
    arr = image.numpy()
    return from_numpy_like(np.ceil(arr), image)
    
@add_method(NTImage)
def floor(image):
    arr = image.numpy()
    return from_numpy_like(np.floor(arr), image)

@add_method(NTImage)
def max(image):
    arr = image.numpy()
    return np.max(arr)
    
@add_method(NTImage)
def min(image):
    arr = image.numpy()
    return np.min(arr)

@add_method(NTImage)
def mean(image):
    arr = image.numpy()
    return np.mean(arr)

@add_method(NTImage)
def median(image):
    arr = image.numpy()
    return np.median(arr)
    
@add_method(NTImage)
def sum(image):
    arr = image.numpy()
    return np.sum(arr)

@add_method(NTImage)
def std(image):
    arr = image.numpy()
    return np.std(arr)
    
@add_method(NTImage)
def unique(image):
    arr = image.numpy()
    return np.unique(arr)
    
@add_method(NTImage)
def log(image):
    arr = image.clone('float32').numpy()
    return from_numpy_like(np.log(arr), image)
    
@add_method(NTImage)
def exp(image):
    arr = image.clone('float32').numpy()
    return from_numpy_like(np.exp(arr), image)
    
@add_method(NTImage)
def sqrt(image):
    arr = image.clone('float32').numpy()
    return from_numpy_like(np.sqrt(arr), image)
    
@add_method(NTImage)
def power(image):
    arr = image.clone('float32').numpy()
    return from_numpy_like(np.power(arr), image)
    
