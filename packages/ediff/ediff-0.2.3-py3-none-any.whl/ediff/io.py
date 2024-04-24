'''
Module: ediff.io
----------------
Input/output functions for package ediff.    
'''

from PIL import Image

import numpy as np
import matplotlib.pyplot as plt

import ediff.radial

def read_image(image_name, itype=None):
    '''
    Read grayscale image into 2D numpy array.
    
    Parameters
    ----------
    image_name : string or pathlib object
        Name of image that should read into numpy 2D array.
    itype: string ('8bit'  or '16bit')
        type of the image: 8 or 16 bit grayscale    
        
    Returns
    -------
    2D numpy array
    '''
    img = Image.open(image_name)
    if itype=='8bit':
        arr = np.asarray(img, dtype=np.uint8)
    else:
        arr = np.asarray(img, dtype=np.uint16)
    return(arr)


def set_plot_parameters(
        size=(8,6), dpi=100, fontsize=8, my_defaults=True, my_rcParams=None):
    '''
    Set global plot parameters (mostly for plotting in Jupyter).

    Parameters
    ----------
    size : tuple of two floats, optional, the default is (8,6)
        Size of the figure (width, height) in [cm].
    dpi : int, optional, the defalut is 100
        DPI of the figure.
    fontsize : int, optional, the default is 8
        Size of the font used in figure labels etc.
    my_defaults : bool, optional, default is True
        If True, some reasonable additional defaults are set,
        namely line widths and formats.
    my_rcParams : dict, optional, default is None
        Dictionary in plt.rcParams format
        containing any other allowed global plot parameters.

    Returns
    -------
    None; the result is a modification of the global plt.rcParams variable.
    '''
    # (1) Basic arguments -----------------------------------------------------
    if size:  # Figure size
        # Convert size in [cm] to required size in [inch]
        size = (size[0]/2.54, size[1]/2.54)
        plt.rcParams.update({'figure.figsize' : size})
    if dpi:  # Figure dpi
        plt.rcParams.update({'figure.dpi' : dpi})
    if fontsize:  # Global font size
        plt.rcParams.update({'font.size' : fontsize})
    # (2) Additional default parameters ---------------------------------------
    if my_defaults:  # Default rcParams if not forbidden by my_defaults=False
        plt.rcParams.update({
            'lines.linewidth'    : 0.8,
            'axes.linewidth'     : 0.6,
            'xtick.major.width'  : 0.6,
            'ytick.major.width'  : 0.6,
            'grid.linewidth'     : 0.6,
            'grid.linestyle'     : ':'})
    # (3) Further user-defined parameter in rcParams format -------------------
    if my_rcParams:  # Other possible rcParams in the form of dictionary
        plt.rcParams.update(my_rcParams)


def plot_radial_distributions(
        data_to_plot, xlimit, ylimit, output_file=None):
    """
    Plot one or more 1D-radial distrubution files in one graph.

    Parameters
    ----------
    data_to_plot : 2D-list 
        * list with several rows containing [data, linestyle, label]
        * data = data for plotting - they can be one of the following:
            - PNG filename = str, a PNG-file = 2D diffraction pattern
            - TXT filename = str, a text file = 1D diffraction profile
            - 2D-array = a numpy array, containg 2D diffraction pattern
            - 1D-array = a numpy array, containing 1D diffraction profile
            - Note1: 2D-pattern = a square image/array with intensities
            - Note2: 1D-profile = a text file/array with two cols/rows = [R,I],
              where R = distance from center, I = diffraction intensity
        * linestyle = matplotlib.pyplot format, such as 'r-' (red line)
        * label = name of the data, which will appear in the plot legend
    xlimit : int
        maximum of the X-axis
    ylimit : int
        maximum of the Y-axis
    output_file : int, optional, default=None
        Name of the output file;
        if the *output* argument is given,
        the plot is not only shown on screen, but also saved in *output* file. 

    Returns
    -------
    Nothing
        The output is the plot on screen
        (and in *output file* if the *output* argument was given).
    
    Technical notes
    ---------------
    * This function is quite flexible.
    * It can plot one radial distribution or more.
    * It can take data from PNG-files, TXT-files, 2D-arrays and 1D-arrays.
    * If the input is a PNG-file or2D-array,
      the center is just *estimated* as as the center of intensity;
      therefore, this works only for good diffractograms with a central spot.
    * This makes the code a more complex, but it is convenient for the user.
    * An example of fast comparison of three 1D-distributions
      taken from three 2D-diffractograms in the form of 16-bit PNG images:
    
    >>> ediff.io.plot_radial_distributions(
    >>>     data_to_plot = [
    >>>         ['sum_all_16bit.png', 'k:',  'All data'],
    >>>         ['sum_f_16bit.png',   'b--', 'F data'],
    >>>         ['sum_fd_16bit.png',  'r-',  'FD data']]
    >>>     xlimit=200, ylimit=300,
    >>>     output_file='sums_final_1d.png')
    """
    # Initialize
    n = len(data_to_plot)
    rdist = data_to_plot
    # Plot radial distribution files
    for i in range(n):
        # Read data
        data = rdist[i][0]
        if type(data) == str:  # Datafile
            if data.lower().endswith('.png'):  # ....PNG file, 2D-diffractogram
                arr = read_image(data)
                profile = ediff.radial.calc_radial_distribution(arr)
            else:  # ......................................TXT file, 1D-profile
                profile = ediff.radial.read_radial_distribution(data)
        elif type(data) == np.ndarray:  # Numpy array
            if data.shape[0] == data.shape[1]:  # sqare array, 2D-diffractogram
                profile = ediff.radial.calc_radial_distribution(data)
            else:  # ..............................non-square rrray, 1D-profile
                profile = data
        # Read plot parameters        
        my_format = rdist[i][1]
        my_label  = rdist[i][2]
        # Plot data
        R,I = profile
        plt.plot(R,I, my_format, label=my_label)
    # ...adjust plot
    plt.xlabel('Radial distance [pixel]')
    plt.ylabel('Intensity [grayscale]')
    plt.xlim(0,xlimit)
    plt.ylim(0,ylimit)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    # ...change Jupyter default transparent color to white
    plt.gcf().patch.set_facecolor('white')
    # ...save plot as PNG (only if argument [output] was given)
    if output_file: plt.savefig(output_file, dpi=300)
    # ...show plot
    plt.show()
