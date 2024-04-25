
__all__ = [
    'expand_dims',
    'squeeze',
    'reshape',
    'stack',
    'merge',
    'split',
    'repeat',
    'reorient',
    'swapaxes',
    'moveaxis'
]


def stack():
    """Creates an nd+1 dimensional image from list of nd images"""
    pass


def merge():
    """Creates an nd dimensional image with channels from a list of nd images"""
    pass


def reorient(image, orientation='LPI'):
    """
    Reorients a 3D image.
    
    Options are based on the following:
        - left (L) or right (R)
        - posterior (P) or anterior (P)
        - inferior (I) or superior (S)
    
    Where the value you specify indicates that the given axis should start
    at that position. For instance, LPI indicates that axis 0 should start on
    the left side and go to the right, axis 1 should start in the posterior
    and go to the anterior, etc.
    
    The default is LPI as this is a commonly accepted default orientation.
    """
    pass