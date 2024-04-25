import math
import numpy as np
import itk

from ntimage import core
from ntimage.utils.methods import add_method

__all__ = [
 'smooth',
 'crop',
 'resample',
 'slice',
]

@add_method(core.NTImage)
def smooth(image, sigma, method='gaussian'):
    if method == 'gaussian':
        new_image = itk.smoothing_recursive_gaussian_image_filter(image._image, sigma=sigma)
    else:
        raise ValueError('The supplied method is not supported.')
    return core.from_itk(new_image)

@add_method(core.NTImage)
def crop(image, indices=None, return_indices=False):
    """
    Remove all blank space around an image. 
    
    If the image is cropped, the result image will be smaller than the
    original image. To maintain the same shape, set resample=True
    
    import ntimage as nti
    img = nti.zeros((10,10))
    img[:7,:7] = 1
    img2 = nti.crop(img) # shape: (7,7)
    
    img = nti.load(nti.example_data('r16'))
    img2 = nti.crop(img)
    img3 = nti.resample(img2, (220,240))
    """
    image = image.clone()
    if indices is None:
        arr = image.numpy()
        p = np.where(arr != 0)
        if image.dimension == 2:
            new_image = image[min(p[0]) : max(p[0]) + 1, min(p[1]) : max(p[1]) + 1]
        elif image.dimension == 3:
            new_image = image[min(p[0]) : max(p[0]) + 1, 
                      min(p[1]) : max(p[1]) + 1,
                      min(p[2]) : max(p[2]) + 1]
        
        if return_indices:
            return new_image, [(min(pp), max(pp)+1) for pp in p]
    else:
        i = indices
        if image.dimension == 2:
            new_image = image[i[0][0]:i[0][1], i[1][0]:i[1][1]]
        elif image.dimension == 3:
            new_image = image[i[0][0]:i[0][1], i[1][0]:i[1][1], i[2][0]:i[2][1]]
    
    return new_image

@add_method(core.NTImage)
def resample(image, shape, interpolation='linear', use_spacing=False):
    """
    Resample an image to another shape.
    
    The image will remain the same relatively speaking within the image.
    
    shape : tuple
        new size of the image
        
    interpolation : string
        options: linear, nearestneighbor
        defaults to linear for float and nearestneighbor for int images
        
    Examples
    --------
    import ntimage as nt
    img = nt.load(nt.example_data('r16'))
    img2 = nt.resample(img, (128, 128))
    img3 = nt.resample(img, (1, 1.5), use_spacing=True)
    img4 = nt.resample(img3, (1, 1), use_spacing=True)
    img5 = nt.resample(img3, img.shape)
    """
    itk_image = image._image
    
    resampler = itk.ResampleImageFilter[itk_image, itk_image].New()
    interpolator = itk.LinearInterpolateImageFunction.New(itk_image)
    resampler.SetInterpolator(interpolator)
    resampler.SetOutputParametersFromImage(itk_image)
    resampler.SetDefaultPixelValue(itk_image.GetPixel(1))
    
    if not use_spacing:
        spacing = list(reversed([s1 / s2 for s1, s2 in zip(image.shape, shape)]))
        new_shape = list(reversed(shape))
    else:
        spacing = shape
        new_shape = list(reversed([int(image.shape[i] * image.spacing[i] / spacing[i]) for i in range(image.dimension)]))
    
    resampler.SetOutputSpacing(spacing)

    resampler.SetSize(new_shape)
    resampler.SetInput(itk_image)
    resampler.Update()

    return core.from_itk(resampler.GetOutput())

@add_method(core.NTImage)
def slice(image, axis, index):
    if image.dimension == 2:
        if axis == 0:
            return image[index, :]
        elif axis == 1:
            return image[:, index]
    elif image.dimension == 3:
        if axis == 0:
            return image[index, :, :]
        elif axis == 1:
            return image[:, index, :]
        elif axis == 2:
            return image[:, :, index]
        
    raise ValueError('Image dimension + axis not supported')