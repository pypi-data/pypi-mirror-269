import itk
import itk.itkExtractImageFilterPython
import numpy as np

from ntimage import core
from ..utils.datatypes import to_ptype

class NTImage:
    
    def __init__(self, image):
        """
        Create a new NTImage.
        
        An NTImage is a convenient wrapper around an itk image.
        """
        if not 'itkImagePython' in str(type(image)):
            raise ValueError('NTImage can only be initialized with an itk image.')
        self._image = image
    
    @property
    def components(self):
        return self._image.GetNumberOfComponentsPerPixel()
    
    @property
    def dimension(self):
        return self._image.GetImageDimension()
    
    @property
    def orientation(self):
        if self.dimension == 2: return '-'
        direction = self.direction

        orientation = []
        for i in range(3):
            row = direction[:,i]
            idx = np.where(np.abs(row)==np.max(np.abs(row)))[0][0]

            if idx == 0:
                if row[idx] < 0:
                    orientation.append('L')
                else:
                    orientation.append('R')
            elif idx == 1:
                if row[idx] < 0:
                    orientation.append('P')
                else:
                    orientation.append('A')
            elif idx == 2:
                if row[idx] < 0:
                    orientation.append('S')
                else:
                    orientation.append('I')
        return ''.join(orientation)
    
    @property
    def direction(self):
        return np.array(self._image.GetDirection())
    
    def set_direction(self, direction):
        self._image.SetDirection(np.array(direction))
    
    @property
    def origin(self):
        return tuple(self._image.GetOrigin())

    def set_origin(self, origin):
        self._image.SetOrigin(tuple(origin))
    
    @property
    def spacing(self):
        return tuple(self._image.GetSpacing())
    
    def set_spacing(self, spacing):
        self._image.SetSpacing(tuple(spacing))
    
    @property
    def shape(self):
        return self._image.shape
    
    @property
    def dtype(self):
        numpy_dtype = self._image.dtype
        return str(numpy_dtype).split("'")[1].split('.')[1]
    
    @property
    def ptype(self):
        dtype = self.dtype
        return to_ptype(dtype)
    
    def view(self):
        return itk.GetArrayViewFromImage(self._image)
    
    def numpy(self):
        return itk.GetArrayFromImage(self._image)
    
    def clone(self, dtype=None):
        return core.clone(self, dtype)
    
    def __mul__(self, other):
        this_array = self.numpy()

        if isinstance(other, NTImage):
            if not consistent(self, other):
                raise ValueError('Images do not occupy same physical space')
            other = other.numpy()

        new_array = this_array * other
        return core.from_numpy_like(new_array, self)
    
    __rmul__ = __mul__
    
    def __add__(self, other):
        this_array = self.numpy()

        if isinstance(other, NTImage):
            if not consistent(self, other):
                raise ValueError('Images do not occupy same physical space')
            other = other.numpy()

        new_array = this_array + other
        return core.from_numpy_like(new_array, self)
    
    __radd__ = __add__
    
    def __rsub__(self, other):
        this_array = self.numpy()

        if isinstance(other, NTImage):
            if not consistent(self, other):
                raise ValueError('Images do not occupy same physical space')
            other = other.numpy()

        new_array = this_array - other
        return core.from_numpy_like(new_array, self)

    def __pow__(self, other):
        this_array = self.numpy()

        if isinstance(other, NTImage):
            if not consistent(self, other):
                raise ValueError('images do not occupy same physical space')
            other = other.numpy()

        new_array = this_array ** other
        return core.from_numpy_like(new_array, self)

    def __gt__(self, other):
        this_array = self.numpy()

        if isinstance(other, NTImage):
            if not consistent(self, other):
                raise ValueError('images do not occupy same physical space')
            other = other.numpy()

        new_array = this_array > other
        return core.from_numpy_like(new_array.astype('uint8'), self)
    
    def __ge__(self, other):
        this_array = self.numpy()

        if isinstance(other, NTImage):
            if not consistent(self, other):
                raise ValueError('images do not occupy same physical space')
            other = other.numpy()

        new_array = this_array >= other
        return core.from_numpy_like(new_array.astype('uint8'), self)
    
    def __lt__(self, other):
        this_array = self.numpy()

        if isinstance(other, NTImage):
            if not consistent(self, other):
                raise ValueError('images do not occupy same physical space')
            other = other.numpy()

        new_array = this_array < other
        return core.from_numpy_like(new_array.astype('uint8'), self)

    def __le__(self, other):
        this_array = self.numpy()

        if isinstance(other, NTImage):
            if not consistent(self, other):
                raise ValueError('images do not occupy same physical space')
            other = other.numpy()

        new_array = this_array <= other
        return core.from_numpy_like(new_array.astype('uint8'), self)

    def __eq__(self, other):
        this_array = self.numpy()

        if isinstance(other, NTImage):
            if not consistent(self, other):
                raise ValueError('images do not occupy same physical space')
            other = other.numpy()

        new_array = this_array == other
        return core.from_numpy_like(new_array.astype('uint8'), self)

    def __ne__(self, other):
        this_array = self.numpy()

        if isinstance(other, NTImage):
            if not consistent(self, other):
                raise ValueError('images do not occupy same physical space')
            other = other.numpy()

        new_array = this_array != other
        return core.from_numpy_like(new_array.astype('uint8'), self)
    
    def __truediv__(self, other):
        this_array = self.numpy()

        if isinstance(other, NTImage):
            if not consistent(self, other):
                raise ValueError('Images do not occupy same physical space')
            other = other.numpy()

        new_array = this_array / other
        return core.from_numpy_like(new_array, self)
    
    def __contains__(self, item):
        arr = self.numpy()
        return item in arr
    
    def __and__(self, other):
        this_array = self.numpy()

        if isinstance(other, NTImage):
            if not consistent(self, other):
                raise ValueError('images do not occupy same physical space')
            other = other.numpy()

        new_array = this_array & other
        return core.from_numpy_like(new_array.astype('uint8'), self)

    def __or__(self, other):
        this_array = self.numpy()

        if isinstance(other, NTImage):
            if not consistent(self, other):
                raise ValueError('images do not occupy same physical space')
            other = other.numpy()

        new_array = this_array | other
        return core.from_numpy_like(new_array.astype('uint8'), self)
    
    def __getitem__(self, idx):
        """
        If indices, treat like numpy array
        If another image, treat like a mask ?
        """
        image = self._image
        
        if isinstance(idx, NTImage):
            arr = self.numpy()
            other = idx.numpy()
            new_array = arr[other]
            return core.from_numpy_like(new_array, self)
        
        idx = tuple(reversed(idx))
        ndim = len(idx)
        
        old_region = image.GetLargestPossibleRegion()
        size = old_region.GetSize()
        start = old_region.GetIndex()
        shape = list(reversed(self.shape))
        
        for i in range(ndim):
            tmp_idx = idx[i]
            if not isinstance(tmp_idx, slice):
                ndim -= 1
                size[i] = 0
                start[i] = int(tmp_idx)
            else:
                tmp_start = tmp_idx.start
                if tmp_start is None:
                    tmp_start = 0
                tmp_stop = tmp_idx.stop
                if tmp_stop is None:
                    tmp_stop = shape[i]
                    
                if tmp_start > tmp_stop:
                    raise ValueError('Reverse indexing is not currently supported.')
                
                tmp_size = tmp_stop - tmp_start
                if tmp_size == 0:
                    # handle an index of "10:10"
                    ndim -= 1
                    size[i] = 0
                    start[i] = start[i] + int(tmp_start)
                else:
                    size[i] = int(tmp_size)
                    start[i] = start[i] + int(tmp_start)
        
        if ndim < 2:
            return self.numpy().__getitem__(idx)
        
        new_region = itk.ImageRegion[len(idx)]()
        new_region.SetSize(size)
        new_region.SetIndex(start)
        
        NewImageType = itk.Image[itk.ctype(self.ptype), ndim]
        my_filter = itk.ExtractImageFilter[image, NewImageType].New(image)
        my_filter.SetExtractionRegion(new_region)
        my_filter.SetInput(image)
        my_filter.SetDirectionCollapseToIdentity()
        my_filter.Update()
        
        return NTImage(my_filter.GetOutput())
    
    def __setitem__(self, idx, value):
        if isinstance(idx, NTImage):
            if not consistent(self, idx):
                raise ValueError('images do not occupy same physical space')
            idx = idx.numpy().astype('bool')

        arr = self.view()
        arr.__setitem__(idx, value)
    
    def __repr__(self):
        if self.dimension == 3:
            s = 'NTImage - {} ({})\n'.format(self.orientation, self.dtype)
        else:
            s = 'NTImage ({})\n'.format(self.dtype)
        
        if self.components > 1:
            s = s + '     {:<10} : {} [{}]\n'.format('Dimensions', self.shape[:-1], self.components)
        else:
            s = s + '     {:<10} : {}\n'.format('Dimensions', self.shape)
        
        s = s +\
            '     {:<10} : {}\n'.format('Spacing', tuple([round(s,4) for s in self.spacing]))+\
            '     {:<10} : {}\n'.format('Origin', tuple([round(o,4) for o in self.origin]))+\
            '     {:<10} : {}\n'.format('Direction', np.round(self.direction.flatten(),4))
        return s


def is_ntimage(image):
    return 'NTImage' in str(type(image))


def consistent(image, other_image, tolerance=1e-2):
    """
    Check if two images have same physical space
    
    import ntimage as nt
    img = nt.load(nt.load(nt.example_data('r16')))
    img2 = nt.load(nt.load(nt.example_data('r16')))
    nt.consistent(img, img2)
    """
    images = [image, other_image]

    img1 = images[0]
    for img2 in images[1:]:
        if (not is_ntimage(img1)) or (not is_ntimage(img2)):
            raise ValueError('Both images must be of class `AntsImage`')

        # image dimension check
        if img1.dimension != img2.dimension:
            return False

        # image spacing check
        space_diffs = sum([abs(s1-s2)>tolerance for s1, s2 in zip(img1.spacing, img2.spacing)])
        if space_diffs > 0:
            return False

        # image origin check
        origin_diffs = sum([abs(s1-s2)>tolerance for s1, s2 in zip(img1.origin, img2.origin)])
        if origin_diffs > 0:
            return False

        # image direction check
        origin_diff = np.allclose(img1.direction, img2.direction, atol=tolerance)
        if not origin_diff:
            return False

    return True