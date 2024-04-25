import os
import sys
import numpy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def greyscale(x: numpy.ndarray)->numpy.ndarray:
    """
        Function that converts image into greyscale.
        Input:
            x - image to convert
        Output:
            image (greyscale)
    """
    R, G, B = x[:, :, 0], x[:, :, 1], x[:, :, 2]
    y = 0.2989 * R + 0.5870 * G + 0.1140 * B
    return y


def displayRGB(x: numpy.ndarray)->None:
    """
        Function that displays R,G,B channels of an image.
        Input:
            x - image to display
        Output:
            None
    """
    fig, ax = plt.subplots(1, 3)
    cmaps = [plt.cm.Reds_r, plt.cm.Greens_r, plt.cm.Blues_r]
    channels = ["Red", "Green", "Blue"]
    for i in range(x.shape[2]):
        ax[i].imshow(x[:,:, i], cmap=cmaps[i]) 
        ax[i].set_title("Channel {}".format(channels[i]))
    plt.show()
 

def display(x: numpy.ndarray, y:str)->None:
    """
        Function that displays an image.
        Input:
            x - image to display
        Output:
            None
    """
    plt.title(y)
    plt.xlabel("X pixels scaling")
    plt.ylabel("Y pixels scaling")
    match len(x.shape):
        case 2:
            plt.imshow(x,  cmap='gray')
        case 3:
            plt.imshow(x)
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown size of image.".format("0;33")) 
    plt.show()





    
    

        
