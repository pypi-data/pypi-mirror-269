import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from .XPlotLibUtils import non_uniform_savgol

class BandgapAnalyzer():
    def __init__(self):
        self.xes_exp_spectra = {}
        self.xes_calc_spectra = {}
        self.xas_exp_spectra = {}
        self.xas_calc_spectra = {}
        self.figsize = (14, 8)
        self.xes_xlims = None
        self.xas_xlims = None
        self.subplot_labels = [['XES' , 'XAS'], ['2nd der.', '2nd der.']]
        self.xes_arrow = None
        self.xas_arrow = None
        self.title = None

    def __load_spectrum(self, path, names, skiprows, sep):
        headers = [[f'{header}_energy', f'{header}_intensity'] for header in names]
        headers = [item for sublist in headers for item in sublist]
        return pd.read_csv(path, sep=sep, skiprows=skiprows, header=None, names=headers)
    
    def __normalize(self, list):
        abs_max = max(max(list), -min(list))
        return [x/abs_max for x in list]

    """
    Load experimental spectra

    Parameters
    ----------
    path : str
        Path to the file containing the spectra
    type : str
        Type of the spectra. Must be either 'xes' or 'xas'
    names : list of str
        Names of the spectra
    skiprows : int
        Number of rows to skip in the beginning of the file
    sep : str
        Separator used in the file
    """
    def load_exp_spectra(self, path, type, names, skiprows=2, sep=','):        
        if type == 'xes':
            exp_spectra = self.xes_exp_spectra
        elif type == 'xas':
            exp_spectra = self.xas_exp_spectra
        else:
            raise ValueError('type must be either "xes" or "xas"')
        

        df = self.__load_spectrum(path, names, skiprows, sep)
        for name in names:
            exp_spectra[name] = df[[f'{name}_energy', f'{name}_intensity']]


    """
    Load calculated spectra

    Parameters
    ----------
    path : str
        Path to the file containing the spectra
    type : str
        Type of the spectra. Must be either 'xes' or 'xas'
    name : str
        Name of the spectra
    skiprows : int
        Number of rows to skip in the beginning of the file
    sep : str
        Separator used in the file
    """
    def load_calc_spectra(self, path, type, name, skiprows=1, sep=','):    
        if type == 'xes':
            calc_spectra = self.xes_calc_spectra
        elif type == 'xas':
            calc_spectra = self.xas_calc_spectra
        else:
            raise ValueError('type must be either "xes" or "xas"')

        df = self.__load_spectrum(path, [name], skiprows, sep)
        calc_spectra[name] = df


    """
    Smoothen the experimental spectra using a Savitzky-Golay filter. The smoothed data will shown in a plot with the option to show the onset region. The parameters set here will be used in the plot method.

    Parameters
    ----------  
    type : str
        Type of the spectra. Must be either 'xes' or 'xas'
    name : str
        Name of the spectra
    window : int
        Window length of datapoints. Must be odd and smaller than x
    poly : int
        The order of polynom used. Must be smaller than the window size
    onset_region : tuple of float, optional
        Tuple containing the start and end of the onset region
    show : bool, optional 
        If True, the smoothed data will be plotted
    """
    def smoothen(self, type, name, window, poly, onset_region = None, show = True):         
        if type == 'xes':
            exp_spectra = self.xes_exp_spectra
        elif type == 'xas':
            exp_spectra = self.xas_exp_spectra
        else:
            raise ValueError('type must be either "xes" or "xas"')

        x = exp_spectra[name][f'{name}_energy'].values
        y = exp_spectra[name][f'{name}_intensity'].values
        y_smoothed = non_uniform_savgol(x, y, window, poly)
        exp_spectra[name][f'{name}_smoothed_intensity'] = y_smoothed
        # take second derivative
        exp_spectra[name][f'{name}_smoothed_2nd'] = np.gradient(np.gradient(y_smoothed, x), x)

        if show:
            # plot the smoothed data
            if onset_region:
                fig, (ax, ax_onset) = plt.subplots(1,2, figsize=(10,6))
                ax_onset.set_xlim(onset_region)
                ax_onset.plot(x, y, label='Raw data')
                ax_onset.plot(x, y_smoothed, label='Smoothed data')
                ax_onset.legend()
            else:
                fig, ax = plt.subplots()
            ax.plot(x, y, label='Raw data')
            ax.plot(x, y_smoothed, label='Smoothed data')
            ax.legend()

    """
    Set the title of the plot

    Parameters
    ----------
    title : str
        Title of the plot
    """
    def set_title(self, title):
        self.title = title


    """
    Set the figure size of the plot

    Parameters
    ----------
    figsize : tuple of float
        Tuple containing the width and height of the figure
    """
    def set_figsize(self, figsize):
        self.figsize = figsize


    """
    Set the x limits of the plot

    Parameters
    ----------
    xes_xlims : tuple of float
        Tuple containing the start and end of the x-axis for the XES spectra
    xas_xlims : tuple of float
        Tuple containing the start and end of the x-axis for the XAS spectra
    """
    def set_xlims(self, xes_xlims, xas_xlims):
        self.xes_xlims = xes_xlims
        self.xas_xlims = xas_xlims

    """
    Add an arrow to annotate the last/first peak of the 2nd derivative of XES/XAS spectra

    Parameters
    ----------
    type : str
        Type of the spectra. Must be either 'xes' or 'xas'
    xy : tuple of float
        Tuple containing the x and y coordinates of the peak
    xytext : tuple of float
        Tuple containing the x and y coordinates of the text
    text : str
        Text to be shown
    text_rot : float, optional
        Rotation of the text
    """
    def add_arrow(self, type, xy, xytext, text, text_rot = 0):
        if type == 'xes':
            self.xes_arrow = (xy, xytext, text, text_rot)
        elif type == 'xas':
            self.xas_arrow = (xy, xytext, text, text_rot)
        else:
            raise ValueError('type must be either "xes" or "xas"')


    """
    Plot the spectra in four plots with the XES and XAS in the top row and their 2nd derivatives in the bottom row.

    Parameters
    ----------
    xes_exp_names : list of str
        Names of the experimental XES spectra
    xes_calc_names : list of str
        Names of the calculated XES spectra
    xas_exp_names : list of str
        Names of the experimental XAS spectra
    xas_calc_names : list of str
        Names of the calculated XAS spectra
    """
    def plot(self, xes_exp_names, xes_calc_names, xas_exp_names, xas_calc_names):
        fig, axes = plt.subplots(2,2, sharex='col', gridspec_kw={'height_ratios': [2, 1]}, figsize=self.figsize)

        # XES
        if self.xes_xlims:
            axes[0,0].set_xlim(self.xes_xlims)
            axes[1,0].set_xlim(self.xes_xlims)
        for xes_exp_name in xes_exp_names:
            axes[0,0].plot(self.xes_exp_spectra[xes_exp_name][f'{xes_exp_name}_energy'], self.__normalize(self.xes_exp_spectra[xes_exp_name][f'{xes_exp_name}_intensity']), label=xes_exp_name)
            axes[1,0].plot(self.xes_exp_spectra[xes_exp_name][f'{xes_exp_name}_energy'], self.xes_exp_spectra[xes_exp_name][f'{xes_exp_name}_smoothed_2nd'])
        for xes_calc_name in xes_calc_names:
            axes[0,0].plot(self.xes_calc_spectra[xes_calc_name][f'{xes_calc_name}_energy'], self.__normalize(self.xes_calc_spectra[xes_calc_name][f'{xes_calc_name}_intensity']), label=xes_calc_name)


        # XAS
        if self.xas_xlims:
            axes[0,1].set_xlim(self.xas_xlims)
            axes[1,1].set_xlim(self.xas_xlims)
        for xas_exp_name in xas_exp_names:
            axes[0,1].plot(self.xas_exp_spectra[xas_exp_name][f'{xas_exp_name}_energy'], self.__normalize(self.xas_exp_spectra[xas_exp_name][f'{xas_exp_name}_intensity']), label=xas_exp_name)
            axes[1,1].plot(self.xas_exp_spectra[xas_exp_name][f'{xas_exp_name}_energy'], self.xas_exp_spectra[xas_exp_name][f'{xas_exp_name}_smoothed_2nd'])
        for xas_calc_name in xas_calc_names:
            axes[0,1].plot(self.xas_calc_spectra[xas_calc_name][f'{xas_calc_name}_energy'], self.__normalize(self.xas_calc_spectra[xas_calc_name][f'{xas_calc_name}_intensity']), label=xas_calc_name)

        # remove space between subplots
        fig.subplots_adjust(wspace=0, hspace=0)

        if self.title:
            fig.suptitle(self.title, y = 0.95)

        for i in range(len(axes)):
            for j in range(len(axes[i])):
                ax = axes[i,j]
                # set ticks only on outside edges
                ax.minorticks_on()
                ax.tick_params(axis='x', which='both', bottom= (i==1), top=(i==0), labelbottom=(i==1))
                ax.tick_params(axis='y', which='both', left=(j==0), right=(j==1), labelleft=(j==0), labelright=(j==1))
                # remove last tick labels for left subplots
                if j == 0 and i == 0:
                    ax.set_xticks(ax.get_xticks()[:-1])
                

                # show text in corner
                ax.text(0.11/self.figsize[0], 1 - (1+i)*0.08/self.figsize[1], self.subplot_labels[i][j], size=12, ha='left', va='top', color='white', bbox=dict(facecolor='black', edgecolor='none', pad=3), transform=ax.transAxes)
                
                if i == 0: # spectra subplots
                    ax.legend(loc='upper right')                    
                else: # 2nd derivative subplots
                    # center 0 in y-axis
                    abs_max = max(-ax.get_ylim()[0], ax.get_ylim()[1])
                    ax.set_ylim(-abs_max, abs_max)

            # annotate last XES peak
            if self.xes_arrow:
                xy, xytext, text, text_rot = self.xes_arrow
                axes[1,0].annotate(text, xy=xy, xytext=xytext, arrowprops=dict(facecolor='black', shrink=0.05), ha='center', va='center', rotation=text_rot)

            # annotate first XAS peak
            if self.xas_arrow:
                xy, xytext, text, text_rot = self.xas_arrow
                axes[1,1].annotate(text, xy=xy, xytext=xytext, arrowprops=dict(facecolor='black', shrink=0.05), ha='center', va='center', rotation=text_rot)