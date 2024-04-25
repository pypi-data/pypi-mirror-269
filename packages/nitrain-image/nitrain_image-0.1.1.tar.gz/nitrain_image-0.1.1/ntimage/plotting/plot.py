import math
import matplotlib.pyplot as plt
from matplotlib import gridspec

import numpy as np

from ntimage.core import is_ntimage, load, NTImage
from ntimage.utils.methods import add_method

__all__ = [
    'plot'
]

@add_method(NTImage)
def plot(image, overlay=None, axis=0, nslices=12, ncol=4):
    if not is_ntimage(image):
        raise ValueError('Only ntimages can be plotted.')
    
    # TODO: ensure uneven spacing is handled
    # TODO: ensure image an overlay are in same physical space
    # TODO: resample image to isotropic spacing if needed
    # TODO: reorient 3d images to LPI?
        
    if image.dimension == 2:
        plot_helper_2d(image, overlay)
    elif image.dimension == 3:
        plot_helper_3d(image, overlay, axis=axis, nslices=nslices, ncol=ncol)
    elif image.dimension == 4:
        raise ValueError('Plotting 4-dimensional images is not currently supported.')
    
    plt.show()
    
    
def plot_helper_2d(image, overlay=None, ax=None):
    arr = image.numpy()
    
    if ax is None:
        fig = plt.figure()
        ax = plt.subplot(111)
        
    im = ax.imshow(arr, cmap='Greys_r', interpolation='none')

    if overlay is not None:
        overlay_arr = overlay.numpy()
        mask = overlay_arr == 0
        mask = np.ma.masked_where(mask == 0, mask)
        overlay_arr = np.ma.masked_array(overlay_arr, mask)
        im = ax.imshow(overlay_arr, cmap='jet', alpha=0.8, interpolation='none')
    
    ax.axis("off")


def plot_helper_3d(image, overlay=None, axis=0, nslices=12, ncol=4):
    """
    import ntimage as nti
    img = nti.load(nti.example_data('mni'))
    overlay = img > 7500
    img.plot(overlay)
    """
    # dont include empty parts of the image
    image, indices = image.crop(return_indices=True)
    if overlay is not None:
        overlay = overlay.crop(indices)

    min_slice = math.floor(min(indices[0]) + image.shape[0]*0.1)
    max_slice = math.floor(max(indices[0]) + 1 - image.shape[0]*0.1)

    slices = np.linspace(min_slice, max_slice, nslices).astype("int")

    figsize = 1.5
    if ncol is None:
        ncol = int(round(math.sqrt(nslices)))
        
    nrow = math.ceil(nslices / ncol)
    xdim = image.shape[2]
    ydim = image.shape[1]
    dim_ratio = ydim / xdim
    fig = plt.figure(figsize=((ncol + 1) * figsize, 
                              (nrow + 1) * figsize * dim_ratio))
    gs = gridspec.GridSpec(
        nrow,
        ncol,
        wspace=0.0,
        hspace=0.0,
        top=1.0 - 0.5 / (nrow + 1),
        bottom=0.5 / (nrow + 1),
        left=0.5 / (ncol + 1),
        right=1 - 0.5 / (ncol + 1),
    )
    for idx, slice_idx in enumerate(slices):
        ax = plt.subplot(gs[math.floor(idx/ncol), idx%ncol])
        if overlay is None:
            plot_helper_2d(image[slice_idx, :, :], ax=ax)
        else:
            plot_helper_2d(image[slice_idx, :, :], overlay[slice_idx, :, :], ax=ax)
        
        ax.axis("off")