import os, re
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np

# from bokeh.plotting import figure, show
# from bokeh.palettes import Colorblind8 as palette
# from bokeh.models import CheckboxGroup, CustomJS
# from bokeh.layouts import column, row
import matplotlib.pyplot as plt

Ryd = 13.605698066 # Rydberg energy to eV


class DOSAnalyzer:
    def __init__(self):
        self.dos_dfs = []
        self.active_xes_dos = {}
        self.active_xas_dos = {}
        self.xes_spectra = {}
        self.xas_spectra = {}
        self.xes_shift = 0
        self.xas_shift = 0
        self.xes_DOS_scale = 1
        self.xas_DOS_scale = 1
        self.staggered_spacing = 0.2
        self.title = 'DOS Analyzer'

    def __init_plt__(self, show_spectra):
        self.figsize = (15, 6)

        # create figure and axis depending on number of spectra to show
        self.fig, axis = plt.subplots(1, len(show_spectra), figsize=self.figsize, sharey=True)
        if len(show_spectra) == 1:
            if show_spectra[0] == 'XES':
                self.ax_xes = axis
                self.ax_xas = None
            elif show_spectra[0] == 'XAS':
                self.ax_xes = None
                self.ax_xas = axis
        else:
            self.ax_xes = axis[0]
            self.ax_xas = axis[1]


        self.fig.tight_layout()

        if 'XES' in show_spectra:
            self.ax_xes.set_xlabel('Energy (eV)')
            self.ax_xes.set_ylabel('DOS')
            self.ax_xes.tick_params(axis='both', direction='in', top=True, right=True)
        if 'XAS' in show_spectra:
            self.ax_xas.set_xlabel('Energy (eV)')
            self.ax_xas.set_ylabel('DOS')
            self.ax_xas.tick_params(axis='both', direction='in', top=True, right=True)
        self.fig.subplots_adjust(wspace=0, hspace=0)
        self.fig.set_size_inches(10, 6)


    def __map_single_column_names__(self, headers, name):

        for i in range(len(headers)):
            if headers[i] in ['ENERGY', 'total-DOS']:
                continue
            else:
                name_parts = headers[i].split(':')
                headers[i] = format(f'{name}_{name_parts[1]}')
        return headers
    
    def __map_column_names__(self, headers, names):

        for i in range(len(headers)):
            if headers[i] in ['ENERGY', 'total-DOS']:
                continue
            else:
                name_parts = headers[i].split(':')
                try:
                    headers[i] = format(f'{names[name_parts[0]]}_{name_parts[1]}')
                except:
                    print(f'No name found for {name_parts[0]}')
                    headers[i] = format(f'{name_parts[0]}_{name_parts[1]}')
        return headers
    
    def __join_dos_dfs__(self, dos_dfs):
        for i in range(1, len(dos_dfs)):
            if 'ENERGY' in dos_dfs[i].columns:
                dos_dfs[i] = dos_dfs[i].drop(['ENERGY'], axis=1)
        dos_data = pd.concat(dos_dfs, axis=1)
        return dos_data
    
    def __norm__(self, data, max=None):
        if max is None:
            max = data.max()
        return data / max
    
    def __get_x_lims__(self, spectra):
        min_energy = min([spectrum[spectrum['intensity'] > 0.02]['ENERGY'].min() for spectrum in spectra])
        max_energy = max([spectrum[spectrum['intensity'] > 0.02]['ENERGY'].max() for spectrum in spectra])
        return min_energy, max_energy

    def __get_dos_scale__(self, dos_dfs, xlims, shift):
        dos_max = 0
        for dos_df in dos_dfs:
            dos_cols = [col for col in dos_df.columns if col != 'ENERGY']
            dos_max = max(dos_max, dos_df[(dos_df['ENERGY'] > xlims[0] - shift) & (dos_df['ENERGY'] < xlims[1] - shift)][dos_cols].max().max())  
        return 1 / (2 * dos_max)
    
    def __filter_cols__(self, dos_dfs, active_dos_cols):
        selected_dos_dfs = []
        for dos_df in dos_dfs:
            dos_df = dos_df[['ENERGY'] + [col for col in dos_df.columns if col!= 'ENERGY' and col in active_dos_cols]]
            if(len(dos_df.columns) > 1):
                selected_dos_dfs.append(dos_df)      
        return selected_dos_dfs
    
    def __configure_plot__(self, ax, spectra, x_min, label, fig_count):
            ax.text(0.075*fig_count/self.figsize[0], 0.2/self.figsize[1], label, ha='left', va='top', color='white', size=12, bbox=dict(facecolor='black', edgecolor='none', pad=3.0), transform=ax.transAxes)   
            x_lims = self.__get_x_lims__(spectra.values())
            ax.set_xlim(x_lims)
            ax.set_ylim(x_min, 1.1)
            ax.set_yticklabels([])
            return x_lims
    
    def __plot_dos__(self, ax, dos_dfs, x_lims, x_shift, scale, staggered):        
        DOS_scale = self.__get_dos_scale__(dos_dfs, x_lims, x_shift) * scale
        dos_nr = 0
        for cur_dos in dos_dfs:
            for column in cur_dos.columns:
                if column == 'ENERGY':
                    continue
                y_offset = - (dos_nr) * self.staggered_spacing if staggered else 0
                ax.plot(cur_dos['ENERGY'] + x_shift, cur_dos[column] * DOS_scale + y_offset, label=column)
                dos_nr += 1


    def __plot_spectra__(self, ax, spectra):
        for spectrum in spectra:
            ax.plot(spectra[spectrum]['ENERGY'], spectra[spectrum]['intensity'], label=spectrum)
    

    """
    Load DOS of multiple atom files from directory with given regex and name (this can include multiple files .dos1, .dos2, ...)

    Parameters
    ----------
    dir : str
        Directory where DOS files are located
    file_name : str
        File name without extension (this make loading dos from multiple files possible)
    name : dict (string -> string)
        Name of the atoms and states (f.e. {'1': 'O1_ES', '2': 'O2_ES', ...})
    binding_energies : dict (string -> float)
        Binding energies of each site in rydberg (f.e. {'O1_ES': 10.0, 'O2_ES': 11.0, ...})
    """
    def load_dos(self, dir, file_name, names, binding_energies):
        dos_files = [f for f in os.listdir(dir) if re.match(f'{file_name}\\.dos[1-9]', f)]
        if len(dos_files) == 0:
            print(f'No files found for regex {file_name} in {dir}')
            return
        dos_files.sort()

        dos_parts = []
        for dos_file in dos_files:
            dos_data = pd.read_csv(dir + dos_file, sep='\\s+', header=None, skiprows=2)
            # remove first column (wrong format of dos file)
            headers = dos_data.iloc[0].tolist()[1:]
            headers = self.__map_column_names__(headers, names)
            dos_data = pd.read_csv(dir + dos_file, sep='\\s+', header=None, skiprows=3, names=headers)
            dos_parts.append(dos_data)

            # add each column to list of possible active dos
            self.active_xes_dos.update({col: False for col in headers if col != 'ENERGY'})
            self.active_xas_dos.update({col: False for col in headers if col != 'ENERGY'})

        dos = self.__join_dos_dfs__(dos_parts)

        # convert rydberg to eV
        dos['ENERGY'] = dos['ENERGY'] * Ryd

        # shift energy to correct scale for each of the sites
        for site_name, binding_energy in binding_energies.items():
            site_dos = dos.filter(regex=f'{site_name}.*', axis=1)
            site_dos.insert(loc=0, column='ENERGY', value=dos['ENERGY'] + binding_energy * Ryd)
            self.dos_dfs.append(site_dos)

    """
    Load DOS of the same atom from directory with given regex and name (this can include multiple files .dos1, .dos2, ...)

    Parameters
    ----------
    dir : str
        Directory where DOS files are located
    file_name : str
        File name without extension (this make loading dos from multiple files possible)
    name : str
        Name of the atom and state (e.g. 'O1_ES')
    E_Fermi : float
        Fermi energy in eV
    binding_Energy : float
        Binding energy in eV
    """
    def load_single_dos(self, dir, file_name, name, binding_Energy):
        dos_files = [f for f in os.listdir(dir) if re.match(f'{file_name}\\.dos[1-9]', f)]
        if len(dos_files) == 0:
            print(f'No files found for regex {file_name} in {dir}')
            return        
        dos_files.sort()

        dos_parts = []
        for dos_file in dos_files:
            dos_data = pd.read_csv(dir + dos_file, sep='\\s+', header=None, skiprows=2)
            # remove first column (wrong format of dos file)
            headers = dos_data.iloc[0].tolist()[1:]
            headers = self.__map_single_column_names__(headers, name)
            dos_data = pd.read_csv(dir + dos_file, sep='\\s+', header=None, skiprows=3, names=headers)
            dos_parts.append(dos_data)

            # add each column to list of possible active dos
            self.active_xes_dos.update({col: False for col in headers if col != 'ENERGY'})
            self.active_xas_dos.update({col: False for col in headers if col != 'ENERGY'})

        dos = self.__join_dos_dfs__(dos_parts)

        # convert rydberg to eV
        dos['ENERGY'] = dos['ENERGY'] * Ryd

        # shift energy to correct scale
        dos['ENERGY'] = dos['ENERGY'] + binding_Energy * Ryd
        

        self.dos_dfs.append(dos)

    """
    Load XES or XAS spectrum from file

    Parameters
    ----------
    path : str
        Path to the spectrum file
    name : str
        Name of the spectrum
    spec_type : str
        Type of the spectrum ("XES" or "XAS")
    skiprows : int
        Number of rows to skip in the file
    delim : str
        Delimiter of the file
    shift : float
        Energy shift of the spectrum
    """
    def load_spectrum(self, path, name, spec_type, skiprows=1, delim=',', shift=0):
        spectrum = pd.read_csv(path, header=None, names=['ENERGY', 'intensity'], skiprows=skiprows, delimiter=delim)
        spectrum['ENERGY'] = spectrum['ENERGY'] + shift
        if spec_type == 'XES':
            self.xes_spectra[name] = spectrum
            self.xes_spectra[name]['intensity'] = self.__norm__(self.xes_spectra[name]['intensity'])
        elif spec_type == 'XAS':
            self.xas_spectra[name] = spectrum
            self.xas_spectra[name]['intensity'] = self.__norm__(self.xas_spectra[name]['intensity'])
        else:
            print(f'Unknown spectrum type {spec_type} (only "XES" and "XAS" are supported)')


    """
    Set energy shift for XES and XAS DOS (use same values used for broadening of the spectra)

    Parameters
    ----------
    xes_shift : float
        Energy shift for XES DOS
    xas_shift : float
        Energy shift for XAS DOS
    """
    def set_shift(self, xes_shift, xas_shift):
        self.xes_shift = xes_shift
        self.xas_shift = xas_shift

    """
    Set title of the plot

    Parameters
    ----------
    title : str
        Title of the plot
    """
    def set_title(self, title):
        self.title = title
    

    """
    Set figure size of the plot

    Parameters
    ----------
    width : int
        Width of the plot
    """
    def set_figsize(self, width, height):
        self.figsize = (width, height)

    """
    Set custom DOS scaling for XES and XAS

    Parameters
    ----------
    xes_scale : float
        Custom scaling for XES DOS
    xas_scale : float
        Custom scaling for XAS DOS
    """
    def set_custom_dos_scale(self, xes_scale, xas_scale):
        self.xes_DOS_scale = xes_scale
        self.xas_DOS_scale = xas_scale

    """
    Print all available DOS to choose from    
    """
    def print_dos_options(self):
        print('DOS to choose from:')
        for dos in self.active_xes_dos.keys():
            print(dos)
        # print('XAS DOS to choose from:')
        # for dos in self.active_xas_dos.keys():
        #     print(dos)

    """
    Set active DOS for plotting

    Parameters
    ----------
    xes_names : list of str
        List of XES DOS names to plot
    xas_names : list of str
        List of XAS DOS names to plot
    """
    def set_active_dos(self, xes_names=[], xas_names=[]):
        # reset all active dos
        for dos in self.active_xes_dos.keys():
            self.active_xes_dos[dos] = False
        for dos in self.active_xas_dos.keys():
            self.active_xas_dos[dos] = False

        # set active dos
        for name in xes_names:
            if name not in self.active_xes_dos.keys():
                print(f'XES: No DOS found for {name}')
                continue
            self.active_xes_dos[name] = True
        for name in xas_names:
            if name not in self.active_xas_dos.keys():
                print(f'XAS: No DOS found for {name}')
                continue
            self.active_xas_dos[name] = True        

    """
    Set staggered spacing between DOS
    
    Parameters
    ----------
    spacing : float
        Spacing between DOS
    """
    def set_staggered_spacing(self, spacing):
        self.staggered_spacing = spacing


    """
    Plot DOS with XES and XAS spectra

    Parameters
    ----------
    staggered : bool
        Staggered DOS
    show_spectra : list of str
        List of spectra to show ("XES" or "XAS")
    """
    def plot_dos(self, staggered=False, show_spectra=['XES', 'XAS']):
        if len(show_spectra) == 0:
            print('No spectra selected for plotting, select from "XES" and "XAS"')
            return
        
        # remove duplicates from show_spectra
        show_spectra = list(set(show_spectra))
        if len(show_spectra) != len([spec_type for spec_type in show_spectra if spec_type in ['XES', 'XAS']]):
            print('Unknown spectra type, only "XES" and "XAS" are supported')
            return
        

        self.__init_plt__(show_spectra)

        self.fig.suptitle(self.title, y = 1.0)

        active_xes_dos_cols = [col for col, state in self.active_xes_dos.items() if state]
        active_xas_dos_cols = [col for col, state in self.active_xas_dos.items() if state]

        # filter DOS for active columns
        if 'XES' in show_spectra:
            selected_xes_dos_dfs = self.__filter_cols__(self.dos_dfs, active_xes_dos_cols)
        if 'XAS' in show_spectra:
            selected_xas_dos_dfs = self.__filter_cols__(self.dos_dfs, active_xas_dos_cols)

        # configure XES and XAS plots
        x_min =  -0.1 - (max(len(active_xes_dos_cols), len(active_xes_dos_cols))-1) * self.staggered_spacing if staggered else -0.1

        if 'XES' in show_spectra:
            xes_x_lims = self.__configure_plot__(self.ax_xes, self.xes_spectra, x_min, 'nXES', len(show_spectra))
        
        if 'XAS' in show_spectra:
            xas_x_lims = self.__configure_plot__(self.ax_xas, self.xas_spectra, x_min, 'XAS', len(show_spectra))
    
        # plot spectra
        if 'XES' in show_spectra:
            self.__plot_spectra__(self.ax_xes, self.xes_spectra)

        if 'XAS' in show_spectra:
            self.__plot_spectra__(self.ax_xas, self.xas_spectra)

        # plot DOS
        if 'XES' in show_spectra:
            if len(selected_xes_dos_dfs) == 0:
                print('No XES DOS selected for plotting')
            else:
                self.__plot_dos__(self.ax_xes, selected_xes_dos_dfs, xes_x_lims, self.xes_shift, self.xes_DOS_scale, staggered)
        if 'XAS' in show_spectra:
            if len(selected_xas_dos_dfs) == 0:
                print('No XAS DOS selected for plotting')
            else:
                self.__plot_dos__(self.ax_xas,selected_xas_dos_dfs, xas_x_lims, self.xas_shift, self.xas_DOS_scale, staggered)



        # add legend
        if 'XES' in show_spectra:
            self.ax_xes.legend()
        if 'XAS' in show_spectra:
            self.ax_xas.legend()


    """
    Export selected DOS to csv (individual files for XES and XAS)

    Parameters
    ----------
    path : str
        Path to the directory where to save the DOS
    name : str
        Name of the DOS file
    export_spectra : list of str
        List of spectra to export ("XES" or "XAS")
    """
    def export_dos(self, path, name, export_spectra=['XES', 'XAS']):
        if len(export_spectra) == 0:
            print('No spectra selected for export, select from "XES" and "XAS"')
            return
        
        # remove duplicates from show_spectra
        export_spectra = list(set(export_spectra))
        if len(export_spectra) != len([spec_type for spec_type in export_spectra if spec_type in ['XES', 'XAS']]):
            print('Unknown spectra type, only "XES" and "XAS" are supported')
            return
        
        # filter DOS for active columns
        if 'XES' in export_spectra:
            selected_xes_dos_cols = [col for col, state in self.active_xes_dos.items() if state]
            selected_xes_dos_dfs = self.__filter_cols__(self.dos_dfs, selected_xes_dos_cols)
            for i, dos_df in enumerate(selected_xes_dos_dfs):
                dos_df.rename({'ENERGY': f'ENERGY_{i+1}'}, axis=1, inplace=True)
        if 'XAS' in export_spectra:
            selected_xas_dos_cols = [col for col, state in self.active_xas_dos.items() if state]            
            selected_xas_dos_dfs = self.__filter_cols__(self.dos_dfs, selected_xas_dos_cols)
            for i, dos_df in enumerate(selected_xas_dos_dfs):
                dos_df.rename({'ENERGY': f'ENERGY_{i+1}'}, axis=1, inplace=True)

        
        # merge and save selected DOS into single dataframe
        if 'XES' in export_spectra:
            selected_xes_dos = pd.concat(selected_xes_dos_dfs, axis=1)
            selected_xes_dos.to_csv(f'{path}/{name}_XES.csv', index=False)
            print(f'XES DOS exported to {path}/{name}_XES.csv')
        if 'XAS' in export_spectra:
            selected_xas_dos = pd.concat(selected_xas_dos_dfs, axis=1)
            selected_xas_dos.to_csv(f'{path}/{name}_XAS.csv', index=False)
            print(f'XAS DOS exported to {path}/{name}_XAS.csv')
    
