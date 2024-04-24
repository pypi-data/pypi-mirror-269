import math
import numpy
import scipy

from typing import Tuple, Any


def mse(x:numpy.ndarray, y: numpy.ndarray)->float:
    """
        Function that computes mse between two images.
        Input:
            x,y - images
        Output:
            computed mse
    """
    return 1/(x.shape[0]*x.shape[1]) * numpy.sum((x-y)**2)


def psnr(x:numpy.ndarray, y: numpy.ndarray)->float:
    """
        Function that computes psnr between two images.
        Input:
            x,y - images
        Output:
            computed psnr
    """
    return 10*numpy.log10(numpy.max(x)**2/mse(x,y))


def GaussianNoise(img:numpy.ndarray, mean:float, sigma:float)->numpy.ndarray:
    """
        Function that add gaussian noise to an image.
        Input:
            image - image 
            mean, sigma - parameters for gaussian distribution
        Output:
            image (with noise)
    """
    x = numpy.copy(img).astype(numpy.float32)
    noise = numpy.random.normal(mean, sigma,(x.shape[0],x.shape[1]))
    match len(x.shape):
        case 2:
            x += noise
        case 3:
            x[:,:,0] += noise
            x[:,:,1] += noise
            x[:,:,2] += noise
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown size of image.".format("0;33"))
    x = numpy.clip(x, 0, 255).astype(numpy.uint8)
    return x


def SaltnPepperNoise(img:numpy.ndarray, prob:float)->numpy.ndarray:
    """
        Function that add gaussian noise to an image.
        Input:
            image - image
            prob - probability of salting
        Output:
            image (with noise)
    """
    x = numpy.copy(img)
    noise = numpy.random.random((x.shape[0],x.shape[1]))
    x[numpy.where(noise < prob)] = 0
    x[numpy.where(noise > 1-prob)] = 255
    return x



def filterLowPass()->numpy.ndarray:
    """
        Function that returns a lowpass filter.
        Input:
            None
        Output:
            filter
    other. 1/9*numpy.array([[1,1,1],[1,1,1],[1,1,1]])
    """
    return 1/8*numpy.array([[0,1,0],[1,4,1],[0,1,0]]) 


def filterHighPass()->numpy.ndarray:
    """
        Function that returns a highpass filter.
        Input:
            None
        Output:
            filter
    """
    return 1/4*numpy.array([[0,-1,0],[-1,8,-1],[0,-1,0]])
    #return numpy.array([[0,-1,0],[-1,4,-1],[0,-1,0]])
    #return 1/16*numpy.array([[-1,-2,-1],[-2,12,-2],[-1,-2,-1]])
    #return 1/9*numpy.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
   

def filterBandreject()->numpy.ndarray:
    """
        Function that returns a band reject filter.
        Input:
            None
        Output:
            filter
    """
    return None

def filterBandpass()->numpy.ndarray:
    """
        Function that returns a bandpass filter.
        Input:
            None
        Output:
            filter
    """
    return None


def filterAverage(n:int)->numpy.ndarray:
    """
        Function that returns an average filter.
        Input:
            n - size of filter
        Output:
            filter
    """ 
    return 1/n**2*numpy.ones((n,n))
  


def filterGaussian()->numpy.ndarray: # sigma:float
    """
        Function that returns a gaussian filter.
        Input:
            sigma - parameter for Gaussian distribution
        Output:
            filter
    
        other.
            filter 1. - 1/1003*numpy.array([[0,0,1,2,1,0,0],[0,3,13,22,13,3,0],[1,13,59,97,59,13,1],[2,22,97,159,97,22,2],[1,13,59,97,59,13,1],[0,3,13,22,13,3,0],[0,0,1,2,1,0,0]])
            filter 2. - 1/273*numpy.array([[1,4,7,4,1],[4,16,26,16,4],[7,26,41,26,7],[4,16,26,16,4],[1,4,7,4,1]])
    """
    return 1/16*numpy.array([[1,2,1],[2,4,2],[1,2,1]])



def filterLaplacian()->numpy.ndarray:
    """
        Function that returns a Laplacian filter.
        Input:
            None
        Output:
            filter
        other. 
            filter . - numpy.array([[1,1,1],[1,-8,1],[1,1,1]])
    """
    return numpy.array([[0,1,0],[1,-4,1],[0,1,0]]) 


def filterSobel()->numpy.ndarray:
    """
        Function that returns a Sobel filter.
        Input:
            None
        Output:
            filter
        other. 
            filter . -numpy.array([[0,-1],[1,0]])
    """
    return numpy.array([[-1,0],[0,1]]) 
  
   

def filterRoberts()->numpy.ndarray:
    """
        Function that returns a Roberts filter.
        Input:
            None
        Output:
            filter
        other. 
            filter . - numpy.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    """
    return numpy.array([[-1,-2,-1],[0,0,0],[1,2,1]])



def padding(img:numpy.ndarray, types:str, n:int)->numpy.ndarray:
    """
        Function to padd an image.
        Input:
            image - image
            types - types of padding {‘reflect’, ‘constant’, ‘wrap’...‘nearest’, ‘mirror’,}
            n - size of padding
        Output:
            image (padded)
    """
    # A TERMINER !!! - add different types of padding

    size = numpy.copy(img.shape)
    size[0] = 3*img.shape[0]
    size[1] = 3*img.shape[1]
    x = numpy.zeros(size)

    match types:
        case "constant":
            """
            size = numpy.copy(img.shape)
            size[0] = img.shape[0]+2*n
            size[1] = img.shape[1]+2*n
            x = numpy.zeros(size)
            x[n:img.shape[0]+n, n:img.shape[1]+n] = img
            """
            x[img.shape[0]:2*img.shape[0], img.shape[1]:2*img.shape[1]] = img
        case "wrap":
            for i in range(3):
                for j in range(3):
                    x[i*img.shape[0]:(i+1)*img.shape[0], j*img.shape[1]:(j+1)*img.shape[1]] = img
        case "reflect":
            x[0:img.shape[0], 0:img.shape[1]] = (img[:, ::-1])[::-1, :]
            x[0:img.shape[0], img.shape[1]:2*img.shape[1]] = (img)[::-1, :]
            x[0:img.shape[0], 2*img.shape[1]:] = (img[:, ::-1])[::-1, :]
            x[img.shape[0]:2*img.shape[0], 0:img.shape[1]] = img[:, ::-1]
            x[img.shape[0]:2*img.shape[0], img.shape[1]:2*img.shape[1]] = img
            x[img.shape[0]:2*img.shape[0], 2*img.shape[1]:] = img[:, ::-1]
            x[2*img.shape[0]:, 0:img.shape[1]] = (img[:, ::-1])[::-1, :]
            x[2*img.shape[0]:, img.shape[1]:2*img.shape[1]] = (img[::-1, ::])
            x[2*img.shape[0]:, 2*img.shape[1]:] = (img[:, ::-1])[::-1, :]
        case "nearest":
            pass
        case "mirror":
            pass
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown type of padding.".format("0;33"))
    x = x[img.shape[0]-n:2*img.shape[0]+n, img.shape[1]-n:2*img.shape[1]+n]
    x = numpy.clip(x, 0, 255).astype(numpy.uint8)
    return x

def convolution(img:numpy.ndarray, filters:numpy.ndarray, mode:str)->numpy.ndarray:
    """
        Function that convolves two images.
        Input:
            img - image
            filters - filter to apply
            mode - type of padding
        Output:
            image (convolution)
    """
    padds = math.ceil((filters.shape[0]-1)/2)
    x = padding(img, mode,padds)
   
    n = img.shape[0]+2*padds-filters.shape[0]+1
    m = img.shape[1]+2*padds-filters.shape[0]+1
    match len(x.shape):
        case 2:
            result = numpy.zeros((n, m))
        case 3:
            result = numpy.zeros((n, m, x.shape[2]))
            if len(filters.shape)==2:
                new = numpy.zeros((filters.shape[0],filters.shape[1], x.shape[2]))
                for i in range(x.shape[2]):
                    new[:,:,i] = filters 
                filters = new               
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown size of image.".format("0;33"))

    for i in range(n):
        for j in range(m):
            z = x[i:i+filters.shape[0], j:j+filters.shape[1]] 
            z = z[:, ::-1]
            z = z[::-1, :]
            convolv = z * filters 

            result[i,j] = numpy.sum(convolv)
        
    result = result[:img.shape[0], :img.shape[1]] # crop image, because of padding
    return result



def filtering(img:numpy.ndarray, types:str, mode:str, *args: Tuple[Any])->numpy.ndarray:
    """
        Function that apply filter on an image.
        Input:
            img - image on which th filter is applied
            types - type of filter 
            mode - type of padding {‘reflect’, ‘constant’, ‘nearest’, ‘mirror’, ‘wrap’}
            args - extra arguments (optional)
        Output:
            image (filtered)
    """
    match types:
        case "lowpass":
            filters = filterLowPass()
        case "highpass":
            filters = filterHighPass()
        case "bandreject":
            filters = filterBandreject()
        case "bandpass":
            filters = filterBandpass()
        case "avg":
            filters = filterAverage(int(args[0]))
        case "gauss":
            filters = filterGaussian() #int(args[0]))
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown type of filter.".format("0;33"))

    #x = convolution(img, filters, mode)

    x = numpy.zeros(img.shape)
    match len(img.shape):
        case 2:
            x = scipy.ndimage.convolve(img, filters, mode=mode)
        case 3:
            for i in range(img.shape[2]):
                x[:,:,i] = scipy.ndimage.convolve(img[:,:,i], filters, mode=mode)
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown size of image.".format("0;33"))
  
    x = numpy.clip(x, 0, 255).astype(numpy.uint8)
    return x



def sharpening(img:numpy.ndarray, types:str, mode:str)->numpy.ndarray:
    """
        Function that performs sharpening on an image.
        Input:
            img - image on which th filter is applied
            types - type of filter 
            mode - type of padding {‘reflect’, ‘constant’, ‘wrap’...‘nearest’, ‘mirror’,}
        Output:
            image (filtered)
    """
    match types:
        case "laplacian":
            filters = filterLaplacian()
        case "sobel":
            filters = filterSobel()
        case "roberts":
            filters = filterRoberts()
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown type of filter.".format("0;33"))
    x = convolution(img, filters, mode)
    x = numpy.clip(x, 0, 255).astype(numpy.uint8)
    return x


def crosscorrelation(img:numpy.ndarray, filters:str, sub:numpy.ndarray)->numpy.ndarray:
    """
        Function that find a subimage in an image.
        Input:
            img - image
            sub - subimage to find
        Output:
            subimage (found)
    """
    # A TERMINER !!! - detect elements of same shape but different colors
    
    original = numpy.copy(img)

    img = 0.2989 * img[:,:,0] + 0.5870 * img[:,:,1] + 0.1140 * img[:,:,2]
    sub = 0.2989 * sub[:,:,0] + 0.5870 * sub[:,:,1] + 0.1140 * sub[:,:,2]
    img = sharpening(img, filters, "reflect") 
    sub = sharpening(sub, filters, "reflect") 

    # padding

    size = numpy.copy(img.shape)
    size[0] = img.shape[0]-sub.shape[0]+1
    size[1] = img.shape[1]-sub.shape[0]+1
    result = numpy.zeros(size)

    index = (0,0)
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            corr = img[i:i+sub.shape[0], j:j+sub.shape[1]] * sub
            result[i,j] = numpy.sum(corr)
            
            if numpy.max(result[index]) < numpy.max(result[i,j]):
                index = (i,j)  
    
    N = 5
    COLOR = numpy.array([255,0,127])
    
    find = numpy.copy(original[index[0]:index[0]+sub.shape[0], index[1]:index[1]+sub.shape[1]])    
           
    original[index[0]-N:index[0]+sub.shape[0]+N, index[1]-N:index[1]+sub.shape[1]+N] = COLOR 
    original[index[0]:index[0]+sub.shape[0], index[1]:index[1]+sub.shape[1]] = find        
    return original 
    #return original[index[0]:index[0]+sub.shape[0], index[1]:index[1]+sub.shape[1]] 










