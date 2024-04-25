import sys
import math
import numpy

from typing import Tuple



def crop(img:numpy.ndarray, x:Tuple[float], width:int, height:int)->numpy.ndarray:
    """
        Function that crops an image.
        Input:
            img - image to crop
            x - point
            width - width of the cropped image
            height - height of the cropped image
        Output:
    """
    y = numpy.copy(img)    
    if not(x[0]>=0 and x[0]<img.shape[0] and x[1]>=0 and x[1]<img.shape[1]):
        raise Exception("\n0\33[{}m[-]Error: Impossible to crop image.".format("0;31"))
        sys.exit()
    if (x[0] + width > img.shape[0] or x[1] + height > img.shape[1]):
        raise Exception("\n0\33[{}m[-]Error: Impossible to crop image.".format("0;31"))
        sys.exit()
    return y[x[0]:x[0]+width, x[1]:x[1]+height]



def compression(img:numpy.ndarray, fact:float)->numpy.ndarray:
    """
        Function that ...
        Input:
        Output:
    """
    return img


def downsampling(img:numpy.ndarray, fact:float)->numpy.ndarray:
    """
        Function that performs downsampling on an image.
        Input:
            img - image to downsample
            fact - factor for downsampling
        Output:
            image (downsampled)
    """
    match len(img.shape):
        case 2:
            return img[::fact, ::fact]
        case 3:
            return img[::fact, ::fact, :]
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown size of image.".format("0;33"))                                                                                                                        


def upsampling(img:numpy.ndarray, fact:float)->numpy.ndarray:
    """
        Function that ...
        Input:
        Output:
    """
    # nearest interpolation
    # bilinear interpolation
    return img


def scaling(img:numpy.ndarray, scale:float)->numpy.ndarray:
    """
        Function that scales an image.
        Input:
            img - image to scale
            scale - factor of scaling
        Output:
            image (scaled)
    """
    size = numpy.copy(img.shape)
    size[0] = int(img.shape[0]*scale)
    size[1] = int(img.shape[1]*scale)
    x = numpy.zeros(size)
    for i in range(size[0]):
        for j in range(size[1]):
            x[i,j] = img[int(i/scale), int(j/scale)]        
    x = numpy.clip(x, 0, 255).astype(numpy.uint8)
    return x



def rotate(img:numpy.ndarray, degree:float)->numpy.ndarray:
    """
        Function that rotates an image.
        Input:
            img - image to rotate
            degree - angle of rotation (degrees)
        Output:
            image (rotate)
    """
    rads = math.radians(degree)
    result = numpy.zeros(img.shape)

    midx,midy = (result.shape[0]//2, result.shape[1]//2)

    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            x = (i-midx)*math.cos(rads)+(j-midy)*math.sin(rads)
            y = -(i-midx)*math.sin(rads)+(j-midy)*math.cos(rads)

            x = round(x)+midx
            y = round(y)+midy 
            
            if (x>=0 and y>=0 and x<img.shape[0] and  y<img.shape[1]):
                result[i,j,:] = img[x,y,:]
    result = numpy.clip(result, 0, 255).astype(numpy.uint8)
    return result


def flipping(img:numpy.ndarray)->numpy.ndarray:
    """
        Function that flips an image.
        Input:
            img - image to flip
        Output:
            image (flip)
    """
    return img[:, ::-1, :]

def reverse(img:numpy.ndarray)->numpy.ndarray:
    """
        Function that reverse an image.
        Input:
            img - image to reverse
        Output:
            image (reverse)
    """
    return img[::-1, :, :]


def translation(img:numpy.ndarray)->numpy.ndarray:
    """
        Function that ...
        Input:
        Output:
    """
    return img

def projection(img:numpy.ndarray)->numpy.ndarray:
    """
        Function that ...
        Input:
        Output:
    """
    return img



