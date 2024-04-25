import numpy
import scipy
import matplotlib.pyplot as plt

from typing import Tuple, Any


def Fourier(img:numpy.ndarray)->None:
    """
        Function that computes Fourier transform of an image.
        Input:
            img - image
        Output:
            None
    """
    x = scipy.fft.fftn(img)
    x = scipy.fft.fftshift(x)

    # plot phase and magnitude
    magnitude = numpy.abs(x) #numpy.sqrt(xreal**2 + ximag**2) 
    phase = numpy.arctan2(numpy.imag(x),numpy.real(x))  # numpy.angle(x)

    # reconstruct image
    y = magnitude * numpy.exp(1j*phase)
    y = scipy.fft.ifftshift(y)
    y = scipy.fft.ifftn(y) 
    y = numpy.real(y)
    y = numpy.clip(y, 0, 255).astype(numpy.uint8)
    plt.imshow(y)
    plt.show()



def hardthresholding(img:numpy.ndarray, threshold:float)->numpy.ndarray:
    """
        Function that performs hard thresholding.
        Input:
            img - image
            threshold - 
        Output:     
            image (threshold)
    """
    x = scipy.fft.fftn(img)
    #x = scipy.fft.fftshift(x)

    magnitude = numpy.abs(x)
    phase = numpy.arctan2(numpy.imag(x),numpy.real(x)) # numpy.angle(x)

    threshold *= numpy.mean(magnitude)
    x[numpy.where(magnitude < threshold)] = 0 #numpy.where(magnitude > threshold)

    magnitude = numpy.abs(x)
    phase = numpy.arctan2(numpy.imag(x),numpy.real(x))

    y = magnitude * numpy.exp(1j*phase)
    #y = scipy.fft.ifftshift(y)
    y = scipy.fft.ifftn(x) 
    y = numpy.real(y)
    y = numpy.clip(y, 0, 255).astype(numpy.uint8)
    return y



def IdealHighPassFilter(img:numpy.ndarray, D0:float)->numpy.ndarray:
    """
        Function that returns an Ideal Lowpass filter.
        Input:
            img - image
            D0 - cutoff frequency
        Output:
            filter
    """
    P = img.shape[0]
    Q = img.shape[1]
    D = lambda u,v: numpy.sqrt((u-P/2)**2 + (v-Q/2)**2)  

    H = numpy.zeros((P,Q))
    for u in range(P):
        for v in range(Q):
            if D(u,v) <= D0:
                H[u,v] = 1
            else:
                H[u,v] = 0
    return H

def ButterworthHighPassFilter(img:numpy.ndarray, D0:float, n:int)->numpy.ndarray:
    """
        Function that returns a Butterworth Lowpass filter.
        Input:
        Input:
            img - image
            D0 - cutoff frequency
            n - order
        Output:
            filter
    """
    P = img.shape[0]
    Q = img.shape[1]
    D = lambda u,v: numpy.sqrt((u-P/2)**2 + (v-Q/2)**2)  
    Butterworth = lambda u,v: 1/(1 + (D(u,v)/D0)**(2*n))

    H = numpy.zeros((P,Q))
    for u in range(P):
        for v in range(Q):
           H[u,v] = Butterworth(u,v)
    return H

def GaussianHighPassFilter(img:numpy.ndarray, sigma:float)->numpy.ndarray:
    """
        Function that returns an Gaussian Lowpass filter.
        Input:
            img - image
            sigma - cutoff frequency
        Output:
            filter
    """
    P = img.shape[0]
    Q = img.shape[1]
    D = lambda u,v: numpy.sqrt((u-P/2)**2 + (v-Q/2)**2)  
    gaussian = lambda u,v: numpy.exp(-D(u,v)**2/(2*sigma**2))

    H = numpy.zeros((P,Q))
    for u in range(P):
        for v in range(Q):
           H[u,v] = gaussian(u,v)
    return H

def IdealLowPassFilter(img:numpy.ndarray, D0:float)->numpy.ndarray:
    """
        Function that returns an Ideal Highpass filter.
        Input:
            img - image
            D0 - cutoff frequency
        Output:
            filter
    """
    P = img.shape[0]
    Q = img.shape[1]
    D = lambda u,v: numpy.sqrt((u-P/2)**2 + (v-Q/2)**2) 

    H = numpy.zeros((P,Q))
    for u in range(P):
        for v in range(Q):
            if D(u,v) <= D0:
                H[u,v] = 0
            else:
                H[u,v] = 1
    return H

def ButterworthLowPassFilter(img:numpy.ndarray, D0:float, n:int)->numpy.ndarray:
    """
        Function that returns a Butterworth Highpass filter.
        Input:
        Input:
            img - image
            D0 - cutoff frequency
            n - order
        Output:
            filter
    """
    P = img.shape[0]
    Q = img.shape[1]
    D = lambda u,v: numpy.sqrt((u-P/2)**2 + (v-Q/2)**2)  
    Butterworth = lambda u,v: 1/(1 + (D0/D(u,v))**(2*n))

    H = numpy.zeros((P,Q))
    for u in range(P):
        for v in range(Q):
           H[u,v] = Butterworth(u,v)
    return H


def GaussianLowPassFilter(img:numpy.ndarray, sigma:float)->numpy.ndarray:
    """
        Function that returns an Gaussian Highpass filter.
        Input:
            img - image
            sigma - cutoff frequency
        Output:
            filter
    """
    P = img.shape[0]
    Q = img.shape[1]
    D = lambda u,v: numpy.sqrt((u-P/2)**2 + (v-Q/2)**2) 
    gaussian = lambda u,v: numpy.exp(-D(u,v)**2/(2*sigma**2))

    H = numpy.zeros((P,Q))
    for u in range(P):
        for v in range(Q):
           H[u,v] = 1-gaussian(u,v)
    return H


def HomomorphicFilter(img:numpy.ndarray, D0:int, Hgamma:float, Lgamma:float, c:float)->numpy.ndarray:
    """
        Function that returns a homorphic filter.
        Input:
            img - image
            D0 - cutoff frequency
            c - constant
            gammah, gammal - dynamic range (gammaH, gammaL)
        Output:
            filter
        Other.
            H(u,v) = (gammaH - gammaL) (1 - exp(-(c*D(u,v)**2) / D0**2)) + gammaL
    """
    P = img.shape[0]
    Q = img.shape[1]
    D = lambda u,v: numpy.sqrt((u-P/2)**2 + (v-Q/2)**2)
    fgauss = lambda u, v: numpy.exp(-c*D(u,v)**2 / D0**2)

    H = numpy.zeros((P,Q))
    for u in range(P):
        for v in range(Q):
           H[u,v] = (Hgamma-Lgamma) * (1-fgauss(u,v)) + Lgamma
    return H


def BandrejectFilter(img:numpy.ndarray, D0:float, W:float, filters:str, args:Tuple[Any])->numpy.ndarray:
    """
        Function that returns bandreject filter.
        Input:
            img - image
            D0 - cutoff frequency
            W - width of the band
            filters - type of filter
            *args - parameters (optional)
        Output:
            filter
    """
    P = img.shape[0]
    Q = img.shape[1]
    D = lambda u,v: numpy.sqrt((u-P/2)**2 + (v-Q/2)**2)  

    H = numpy.zeros((P,Q))

    match filters:
        case "ideal":
            for u in range(P):
                for v in range(Q):
                    if D0-W/2<=D(u, v) and D(u,v)<=D0+W/2:
                        H[u,v] = 0
                    else:
                        H[u,v] = 1
        case "butterworth":
            n = int(args[0])
            for u in range(P):
                for v in range(Q):
                    H[u,v] = 1 / (1 + (D(u,v)*W /(D(u,v)**2-D0**2))**(2*n) )
        case "gauss":
            for u in range(P):
                for v in range(Q):
                    H[u,v] = 1 - numpy.exp(- ((D(u,v)**2-D0**2) / (D(u,v)*W))**2)
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown type of filter.".format("0;33"))
    return H


def BandpassFilter(img:numpy.ndarray, D0:float, W:float, filters:str, args:Tuple[Any])->numpy.ndarray:
    """
        Function that returns bandpass filter.
        Input:
            img - image
            D0 - cutoff frequency
            W - width of the band
            filters - type of filter
            *args - parameters (optional)
        Output:
            filter
    """
    return 1-BandrejectFilter(img, D0, W, filters, args) # numpy.abs()



def LaplacianFilter(img:numpy.ndarray, c:int)->numpy.ndarray:
    """
        Function that returns an Gaussian Laplacian filter.
        Input:
            img - image
            c - constant
        Output:
            filter
    """
    P = img.shape[0]
    Q = img.shape[1]
    D = lambda u,v: numpy.sqrt((u-P/2)**2 + (v-Q/2)**2)  

    H = numpy.zeros((P,Q))
    for u in range(P):
        for v in range(Q):
           H[u,v] = -D(u,v)**2
    
    match len(img.shape):
        case 2:
            pass
        case 3:
            h = numpy.zeros((H.shape[0], H.shape[1], img.shape[2]))
            for i in range(img.shape[2]):
                h[:,:, i] = H  
            H = h             
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown size of image.".format("0;33"))
    F = scipy.fft.fftn(img)
    df = numpy.abs(H)*numpy.abs(F)* numpy.exp(1j*numpy.angle(F))
    df = scipy.fft.ifftn(df) 
    df = numpy.real(df)
    g = img + c*df
    #g = numpy.clip(g, 0, 255).astype(numpy.uint8)
    return g


def UnsharpMasking(img:numpy.ndarray, D0:int, k:int)->numpy.ndarray: 
    """
        Function that performs Unsharp Masking and Highboost filtering.
        Input:
            img - image
            k - parameter
                    k=1 - unsharp masking
                    k>1 - highboost filtering
        Output:
            image
    """
    F = scipy.fft.fftn(img)
    H = IdealLowPassFilter(img, D0) # IdealHighPassFilter(img, D0)
    match len(img.shape):
        case 2:
            pass
        case 3:
            h = numpy.zeros((H.shape[0], H.shape[1], img.shape[2]))
            for i in range(img.shape[2]):
                h[:,:, i] = H  
            H = h             
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown size of image.".format("0;33"))
    G = numpy.abs(H)*numpy.abs(F)* numpy.exp(1j*numpy.angle(F))
    gmask = scipy.fft.ifftn(G) 
    gmask = numpy.real(gmask)
    #gmask = numpy.clip(gmask, 0, 255).astype(numpy.uint8)
    g = img + k * gmask
    g = numpy.clip(g, 0, 255).astype(numpy.uint8)
    return g


def HighFreqEmph(img:numpy.ndarray, D0:int, k1:int, k2:int)->numpy.ndarray: 
    """
        Function that performs High-frequency emphasis.
        Input:
            img - image
            k1, k2 - parameter
                    k1 = 1
                    k2=1 - unsharp masking
                    k2>1 - highboost filtering
        Output:
            image
    """
    F = scipy.fft.fftn(img)
    H = IdealLowPassFilter(img, D0) # IdealHighPassFilter(img, D0)
    match len(img.shape):
        case 2:
            pass
        case 3:
            h = numpy.zeros((H.shape[0], H.shape[1], img.shape[2]))
            for i in range(img.shape[2]):
                h[:,:, i] = H  
            H = h             
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown size of image.".format("0;33"))
    H = k1 +k2*H
    G = numpy.abs(H)*numpy.abs(F)* numpy.exp(1j*numpy.angle(F))
    y = scipy.fft.ifftn(G) 
    y = numpy.real(y)
    y = numpy.clip(y, 0, 255).astype(numpy.uint8)
    return y


def NotchFilter()->numpy.ndarray:
    """
        Function that ...
        Input:
        Output:
    """
    return None


def ftfiltering(img:numpy.ndarray, filters:str, *args: Tuple[Any])->numpy.ndarray: # mode:str
    """
        Function that performs filtering.
        Input:
            img - image
            filters - type of filter {lowpass, blowpass, glowpass, highpass, bhighpass, ghighoass, bandreject, bandpass,homomorphic}
            *args - (opt.)
        Output:
            image (filtered)
    """
    # TERMINER !!! - case of padding (image)
    match filters:
        case "lowpass":
            H = IdealLowPassFilter(img, float(args[0]))
        case "blowpass":
            H = ButterworthLowPassFilter(img, float(args[0]), float(args[1]))
        case "glowpass":
            H = GaussianLowPassFilter(img, float(args[0]))
        case "highpass":
            H = IdealHighPassFilter(img, float(args[0]))
        case "bhighpass":
            H = ButterworthHighPassFilter(img, float(args[0]), float(args[1]))
        case "ghighpass":
            H = GaussianHighPassFilter(img, float(args[0]))
        
        case "bandreject":
            H = BandrejectFilter(img, float(args[1]), float(args[2]), args[0], args[3:])
        case "bandpass":
            H = BandpassFilter(img, float(args[1]), float(args[2]), args[0], args[3:])

        case "homomorphic":
            H = HomomorphicFilter(img, float(args[0]), float(args[1]), float(args[2]), float(args[3]))
           
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown type of filter.".format("0;33"))

    match len(img.shape):
        case 2:
            pass
        case 3:
            h = numpy.zeros((H.shape[0], H.shape[1], img.shape[2]))
            for i in range(img.shape[2]):
                h[:,:, i] = H  
            H = h             
        case _:
            raise Exception("\n\033[{}m[-]Warning: Unknown size of image.".format("0;33"))

    F = scipy.fft.fftn(img)
    #F = scipy.fft.fftshift(F)

    Fphase = numpy.arctan2(numpy.imag(F),numpy.real(F))

    # perform filtering
    G = numpy.abs(H)*numpy.abs(F)* numpy.exp(1j*numpy.angle(F))

    #y = scipy.fft.ifftshift(G)
    y = scipy.fft.ifftn(G) 
    y = numpy.real(y)
    y = numpy.clip(y, 0, 255).astype(numpy.uint8)
    return y



def ftcrosscorrelation(img:numpy.ndarray)->numpy.ndarray:
    """
        Function that ...
        Input:
        Output:
    """
    return img



