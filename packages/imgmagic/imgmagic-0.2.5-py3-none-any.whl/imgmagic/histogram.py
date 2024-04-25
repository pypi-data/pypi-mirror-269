import numpy
import matplotlib.pyplot as plt


def histogram(img:numpy.ndarray, density:bool,)->None:
    """
        Function that plots histogram of an image.
        Input:
            img - image
        Output:
            None
    """
    # hist, bins = numpy.histogram(img, bins=numpy.arange(256))#, bins='auto', density=True)
    match len(img.shape):
        case 2:
            unique, counts = numpy.unique(img, return_counts=True)
            plt.hist(counts, bins=unique, density=density)
        case 3:
            fig, ax = plt.subplots(3, 1)
            channels = ["Red", "Green", "Blue"]
            for i in range(img.shape[2]):
                unique, counts = numpy.unique(img[:,:,i], return_counts=True)
                ax[i].hist(counts, bins=unique, density=density) 
                ax[i].set_title("Channel {}".format(channels[i]))
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown size of image.".format("0;33"))
    plt.show()
 



def adjustContrast(img:numpy.ndarray)->numpy.ndarray: # A REVOIR !!!
    """
        Function that performs contrast stretching.
        Input:
            img - image
        Output:
            image (with contrat stretching)
    """
    f = lambda x, h, H : 255/(H-h)*(x-h)
    x = numpy.zeros(img.shape)
    match len(img.shape):
        case 2:
            unique, counts = numpy.unique(img, return_counts=True)
            x = f(img, numpy.min(unique), numpy.max(unique))
        case 3:
            for i in range(img.shape[2]):
                unique, counts = numpy.unique(img[:,:,i], return_counts=True)
                x[:,:,i] = f(img[:,:,i], numpy.min(unique), numpy.max(unique))  
            """
            unique, counts = numpy.unique(img, return_counts=True)
            x = f(img, numpy.min(unique), numpy.max(unique)) 
            """        
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown size of image.".format("0;33"))
    x = numpy.clip(x, 0, 255).astype(numpy.uint8)
    return x


def equalization(img:numpy.ndarray)->numpy.ndarray: # A REVOIR !!!
    """
        Function that performs histogram equalization.
        Input:
            img - image
        Output:
            image (with equalization)
    """
    x = numpy.copy(img)
    match len(img.shape):
        case 2:
            unique, counts = numpy.unique(img, return_counts=True)
            const = (numpy.min(unique)-1)/(img.shape[0]*img.shape[1])
            for i in range(unique.shape[0]):
                   x[numpy.where(x==unique[i])] = const*numpy.sum(counts[:i])
        case 3:
            unique, counts = numpy.unique(img, return_counts=True)
            const = (numpy.min(unique)-1)/(img.shape[0]*img.shape[1])
            for i in range(unique.shape[0]):
                x[numpy.where(x==unique[i])] = const*numpy.sum(counts[:i])     
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown size of image.".format("0;33"))
    x = numpy.clip(x, 0, 255).astype(numpy.uint8)
    return x

def correctionGamma(img:numpy.ndarray, c:float, gamma: float)->numpy.ndarray:
    """
        Function that performs gamma correction on an image.
        Input:
            img - image (grey image)
            c, gamma - parameters of formula
        Output:
            image (gamma correction)
        other.
             s = T(r) = c*r**gamma , c = 1
    """
    f = lambda x: c*x**gamma
    x = f(img)
    x = numpy.clip(x, 0, 255).astype(numpy.uint8)
    return x

def negative(img:numpy.ndarray)->numpy.ndarray:
    """
        Function that computes digital negative of an image.
        Input:
            img - image
        Output:
            image (negative)
        other.
            s = T(r) = (L – 1) – r
    """
    f = lambda x, m : (m-1)-x
    x = numpy.zeros(img.shape)
    match len(img.shape):
        case 2:
            unique, counts = numpy.unique(img, return_counts=True)
            x = f(img, numpy.min(unique))
        case 3:
            for i in range(img.shape[2]):
                unique, counts = numpy.unique(img[:,:,i], return_counts=True)
                x[:,:,i] = f(img[:,:,i], numpy.min(unique))          
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown size of image.".format("0;33"))
    x = numpy.clip(x, 0, 255).astype(numpy.uint8)
    return x


