
import itk

__all__ = [
    'load',
    'save',
    'example_data'
]

from ntimage.core.create import from_itk

def load(file):
    itk_image = itk.imread(file)
    image = from_itk(itk_image)
    return image

def save(image, file):
    itk_image = image._image
    itk.imwrite(itk_image, file)

def example_data(name):
    """
    Get ntimage test data file

    Arguments
    ---------
    name : string
        name of test image tag to retrieve
        Options:
            - 'r16'
            - 'r27'
            - 'r30'
            - 'r62'
            - 'r64'
            - 'r85'
            - 'ch2'
            - 'mni'
            - 'surf'
            - 'pcasl'
    Returns
    -------
    string
        filepath of test image

    Example
    -------
    >>> import ants
    >>> mnipath = ants.get_ants_data('mni')
    """
    import os
    import requests
    import tempfile
    
    def switch_data(argument):
        switcher = {
            "r16": "https://ndownloader.figshare.com/files/28726512",
            "r27": "https://ndownloader.figshare.com/files/28726515",
            "r30": "https://ndownloader.figshare.com/files/28726518",
            "r62": "https://ndownloader.figshare.com/files/28726521",
            "r64": "https://ndownloader.figshare.com/files/28726524",
            "r85": "https://ndownloader.figshare.com/files/28726527",
            "ch2": "https://ndownloader.figshare.com/files/28726494",
            "mni": "https://ndownloader.figshare.com/files/28726500",
            "surf": "https://ndownloader.figshare.com/files/28726530",
            "pcasl": "http://files.figshare.com/1862041/101_pcasl.nii.gz",
        }
        return(switcher.get(argument, "Invalid argument."))

    cache_directory = os.path.expanduser('~/.ntimage/')
    os.makedirs(cache_directory, exist_ok=True)

    if os.path.isdir(cache_directory) == False:
        cache_directory = tempfile.TemporaryDirectory()

    valid_list = ("r16",
                  "r27",
                  "r30",
                  "r62",
                  "r64",
                  "r85",
                  "ch2",
                  "mni",
                  "surf",
                  "pcasl",
                  "show")

    if name == "show" or name is None:
       return(valid_list)

    url = switch_data(name)

    if name == "pcasl":
        target_file_name = cache_directory + "pcasl.nii.gz"
    else:
        extension = ".jpg"
        if name == "ch2" or name == "mni" or name == "surf":
            extension = ".nii.gz"
        if extension == ".jpg":
            target_file_name = cache_directory + name + "slice" + extension
        else:
            target_file_name = cache_directory + name + extension

    target_file_name_path = target_file_name
    if target_file_name == None:
        target_file = tempfile.NamedTemporaryFile(prefix=target_file_name, dir=cache_directory)
        target_file_name_path = target_file.name
        target_file.close()

    if not os.path.exists(target_file_name_path):
        r = requests.get(url)
        with open(target_file_name_path, 'wb') as f:
            f.write(r.content)

    return(target_file_name_path)
    