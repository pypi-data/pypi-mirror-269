import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

__all__ = [
    'plot_hist'
]


def plot_hist(image, xlabel=None, ylabel=None, title=None, color='green', alpha=0.75, show_grid=True):
    arr = image.numpy().flatten()
    
    n, bins, patches = plt.hist(arr,
                                50, 
                                facecolor=color, 
                                alpha=alpha)
    
    if xlabel is not None:
        plt.xlabel(xlabel)
        
    if ylabel is not None:
        plt.ylabel(ylabel)
        
    if title is not None:
        plt.title(title)

    plt.grid(show_grid)
    plt.show()