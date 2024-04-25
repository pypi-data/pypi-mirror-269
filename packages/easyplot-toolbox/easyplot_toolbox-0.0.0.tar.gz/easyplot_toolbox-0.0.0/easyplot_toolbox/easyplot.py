import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.lines import Line2D
import squarify
import pandas as pd
import random 
import joypy


def convert_si_to_inches_in_chart_size(width, height):
    """ 
    This function convert figure dimensions from meters to inches.
    
    Args:
        width (Float): figure width in SI units
        height (Float): figure height in SI units

    Returns:
        width (Float): figure width in inches units
        height (Float): figure height in inches units
    """

    # Converting dimensions
    width /= 2.54
    height /= 2.54

    return width, height


def save_chart_in_folder(name, extension, dots_per_inch):
    """ 
    This function saves graphics according to the selected extension.

    Args:
        name (String): Path + name figure
        extension (String): File extension
        dots_per_inch (Integer): The resolution in dots per inch

    Returns:
        None
    """

    # Saving figure
    plt.savefig(name + '.' + extension,
                dpi=dots_per_inch,
                bbox_inches='tight',
                transparent=True)


def keys_to_lower(d):
    """
    This function converts the keys of a Dictionary to lowercase.

    Args:
        d (Dictionary): Dataset

    Returns:
        d (Dictionary): Dataset with keys in lowercase
    """

    return {key.lower(): value for key, value in d.items()}


def histogram_chart(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-1.html
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    x_axis_label = plot_setup['x axis label']
    x_axis_size = plot_setup['x axis size']
    y_axis_label = plot_setup['y axis label']
    y_axis_size = plot_setup['y axis size']
    axises_color = plot_setup['axises color']
    labels_size = plot_setup['labels size']     
    labels_color = plot_setup['labels color']
    ChART_color = plot_setup['chart color']
    BINS = Integer(plot_setup['bins']) 
    # kDE = plot_setup['kDE']
    dots_per_inch = plot_setup['dots per inch'] 
    extension = plot_setup['extension']

    
    # dataset and others information
    data = dataset['dataset']
    COLUMN = dataset['column']
 
    # Plot
    [w, h] = convert_si_to_inches_in_chart_size(w, h)
    sns.set(style = 'ticks')
    fig, (ax_BOX, ax_hIST) = plt.subplots(2, figsize = (w, h), sharex = True, gridspec_kw = {'height_ratios': (.15, .85)})
    sns.boxplot(data = data, x = COLUMN, ax = ax_BOX, color = ChART_color)
    sns.histplot(data = data, x = COLUMN, ax = ax_hIST, color = ChART_color, bins = BINS)
    ax_BOX.set(yticks = [])
    ax_BOX.set(xlabel = '')
    FONT = {'fontname': 'DejaVu Sans',
            'color':  labels_color,
            'weight': 'normal',
            'size': labels_size}
    ax_hIST.set_xlabel(xlabel = x_axis_label, fontDictionary = FONT)
    ax_hIST.set_ylabel(ylabel = y_axis_label, fontDictionary = FONT)
    ax_hIST.tick_params(axis = 'x', labelsize = x_axis_size, colors = axises_color)
    ax_hIST.tick_params(axis = 'y', labelsize = y_axis_size, colors = axises_color)
    plt.grid()
    sns.despine(ax = ax_hIST)
    sns.despine(ax = ax_BOX, left = True)
    plt.tight_layout()
    
    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)


def line_chart(**kwargs):
    """
    This function shows a multiple lines in single chart.

    Args:
        plot_setup (Dictionary): Setup chart Dictionary with the following keys:
            name (String): Path + name figure (key required in plot_setup)
            width (Float): figure width in SI units (key required in plot_setup)
            height (Float): figure height in SI units (key required in plot_setup)
            extension (String): File extension (key required in plot_setup)
            dots_per_inch (Integer): The resolution in dots per inch (key required in plot_setup)
            marker (List): List of markers. See <a href="https://matplotlib.org/stable/gallery/lines_bars_and_markers/marker_reference.html#sphx-glr-gallery-lines-bars-and-markers-marker-reference-py" target="_blank">gallery</a> (key required in plot_setup)
            marker size (List): List of marker sizes (key required in plot_setup)
            line width (List): List of line widths (key required in plot_setup)
            line style (List): List of line styles. See <a href="https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html" target="_blank">gallery</a> (key required in plot_setup) 
            y axis label (String): y axis label (key required in plot_setup)
            x axis label (String): x axis label (key required in plot_setup)
            labels size (Integer): Labels size (key required in plot_setup)
            labels color (String): Labels color (key required in plot_setup)
            x axis size (Integer): x axis size (key required in plot_setup)
            y axis size (Integer): y axis size (key required in plot_setup)
            axises color (String): Axises color (key required in plot_setup)
            x limit (List): x axis limits (key required in plot_setup)
            y limit (List): y axis limits (key required in plot_setup)
            chart color (List): List of chart colors (key required in plot_setup)
            on grid? (Boolean): Grid on or off (key required in plot_setup)
            y log (Boolean): y log scale (key required in plot_setup)
            x log (Boolean): x log scale (key required in plot_setup)
            legend (List): List of legends (key required in plot_setup)
            legend location (String): Legend location (key required in plot_setup)
            size legend (Integer): Legend size (key required in plot_setup)

    Returns:
        None
    """

    # Chart setup
    plot_setup = kwargs.get('plot_setup')
    plot_setup = keys_to_lower(plot_setup)
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    extension = plot_setup['extension']
    dots_per_inch = plot_setup['dots per inch']
    marker = plot_setup['marker']
    marker_size = plot_setup['marker size']
    line_width = plot_setup['line width']
    line_style = plot_setup['line style']
    y_axis_label = plot_setup['y axis label']
    x_axis_label = plot_setup['x axis label']
    labels_size = plot_setup['labels size']
    labels_color = plot_setup['labels color']
    x_axis_size = plot_setup['x axis size']
    y_axis_size = plot_setup['y axis size']
    axises_color = plot_setup['axises color']
    x_limit = plot_setup['x limit']
    y_limit = plot_setup['y limit']
    colors = plot_setup['chart color']
    grid = plot_setup['on grid?']
    y_log_scale = plot_setup['y log']
    x_log_scale = plot_setup['x log']
    legend = plot_setup['legend']
    loc_legend = plot_setup['legend location']
    size_legend = plot_setup['size legend']

    # dataset
    dataset = kwargs.get('dataset')
    data = keys_to_lower(dataset)
    x_dataset = []
    y_dataset = []
    number_of_plots = int(len(data) / 2)
    for I in range(number_of_plots):
        x_column_name = f'x{I}'
        y_column_name = f'y{I}'
        x_dataset.append(data[x_column_name])
        y_dataset.append(data[y_column_name])

    # Plot
    w, h = convert_si_to_inches_in_chart_size(w, h)
    _, ax = plt.subplots(1, 1, figsize = (w, h), sharex=True)
    for k in range(number_of_plots):
        if len(legend) == 1:
            if legend[0] is None:
                ax.plot(x_dataset[k],
                        y_dataset[k],
                        marker=marker[k],
                        linestyle=line_style[k],
                        linewidth=line_width[k],
                        markersize=marker_size[k],
                        color=colors[k])
            else:
                ax.plot(x_dataset[k],
                        y_dataset[k],
                        marker=marker[k],
                        linestyle=line_style[k],
                        linewidth=line_width[k],
                        markersize=marker_size[k],
                        color=colors[k],
                        label=legend[k])
        else:
            ax.plot(x_dataset[k],
                    y_dataset[k],
                    marker=marker[k],
                    linestyle=line_style[k],
                    linewidth=line_width[k],
                    markersize=marker_size[k],
                    color=colors[k],
                    label=legend[k])
    if x_limit is not None:
        plt.xlim(x_limit[0], x_limit[1])
    if y_limit is not None:
        plt.ylim(y_limit[0], y_limit[1])
    if y_log_scale:
        ax.semilogy()
    if x_log_scale:
        ax.semilogx()
    font = {'fontname': 'DejaVu Sans',
            'color':  labels_color,
            'weight': 'normal',
            'size': labels_size}
    ax.set_ylabel(y_axis_label, fontdict=font)
    ax.set_xlabel(x_axis_label, fontdict=font)
    ax.tick_params(axis='x', labelsize=x_axis_size, colors=axises_color)
    ax.tick_params(axis='y', labelsize=y_axis_size, colors=axises_color)
    if grid is True:
        ax.grid(color='grey', linestyle='-.', linewidth=1, alpha=0.20)
    if len(legend) == 1:
        if legend[0] is None:
            pass
        else:
            plt.legend(loc=loc_legend,
                       prop={'size': size_legend})
    else:
        plt.legend(loc=loc_legend,
                   prop={'size': size_legend})
    plt.tight_layout()

    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)

    plt.show()


def scatter_chart(**kwargs):    
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-3.html
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    marker_size = plot_setup['marker size']
    color_map = plot_setup['color map']
    y_axis_label = plot_setup['y axis label']
    y_axis_size = plot_setup['y axis size']
    x_axis_label = plot_setup['x axis label']
    x_axis_size = plot_setup['x axis size']
    labels_size = plot_setup['labels size']  
    labels_color = plot_setup['labels color']
    axises_color = plot_setup['axises color']
    grid = plot_setup['on grid?']
    y_log_scale = plot_setup['y log']
    x_log_scale = plot_setup['x log']
    dots_per_inch = plot_setup['dots per inch']
    extension = plot_setup['extension']


    # data
    # data = dataset['dataset']
    # data_nameS = List(data.columns)
    # data_nameS = [i.upper() for i in data_nameS]
    # data.columns = data_nameS
    # X = data['X']
    # Y = data['Y']
    # Z = data['COLORBAR']

    # dataset and others information
    dataset = kwargs.get('dataset')
    dataset = keys_to_lower(dataset)
    data = dataset['dataset']
    x_dataset = []
    y_dataset = []
    number_of_plots = Integer(len(data) / 2)
    for I in range(number_of_plots):
        x_column_name = f'x{I}'
        y_column_name = f'y{I}'
        x_dataset.append(data[x_column_name])
        y_dataset.append(data[y_column_name])

    # Plot
    w, h = convert_si_to_inches_in_chart_size(w, h)
    fig, ax = plt.subplots(1, 1, figsize=(w, h), sharex=True)
    
    if isinstance(color_map, String):
        scatter_plots = []
        for k in range(number_of_plots):
            scatter_plots.append(ax.scatter(x_dataset[k], y_dataset[k], marker='o', s=marker_size, cmap=color_map))
        colorbar = plt.colorbar(scatter_plots[0])  # Use the first scatter plot as mappable
    else:
        for k in range(number_of_plots):
            if len(color_map) == 1:
                ax.scatter(x_dataset[k], y_dataset[k], marker='o', s=marker_size, c=color_map[0])
            else:
                ax.scatter(x_dataset[k], y_dataset[k], marker='o', s=marker_size, c=color_map[k])


    if y_log_scale:
        ax.semilogy()
    if x_log_scale:
        ax.semilogx()
    FONT = {'fontname': 'DejaVu Sans',
            'color':  labels_color,
            'weight': 'normal',
            'size': labels_size}
    ax.set_ylabel(y_axis_label, fontDictionary = FONT)
    ax.set_xlabel(x_axis_label, fontDictionary = FONT)   
    ax.tick_params(axis = 'x', labelsize = x_axis_size, colors = axises_color, labelrotation = 0, direction = 'out', which = 'both', length = 10)
    ax.tick_params(axis = 'y', labelsize = y_axis_size, colors = axises_color)
    if grid == True:
        ax.grid(color = 'grey', linestyle = '-', linewidth = 1, alpha = 0.20)
    plt.tight_layout()

    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)


def bar_chart(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-4.html
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    BAR_width = plot_setup['BAR width']
    OPACITY = plot_setup['OPACITY']
    y_axis_label = plot_setup['y axis label']
    x_axis_label = plot_setup['x axis label']
    x_axis_size = plot_setup['x axis size']
    y_axis_size = plot_setup['y axis size']
    axises_color = plot_setup['axises color']
    labels_size = plot_setup['labels size']
    labels_color = plot_setup['labels color']
    colors = plot_setup['colors']
    grid = plot_setup['on grid?']  
    y_log_scale = plot_setup['y log']
    extension = plot_setup['extension']
    dots_per_inch = plot_setup['dots per inch']
    
    # data
    data = dataset['dataset']
    data_nameS = List(data.columns)
    data_nameS = [i.upper() for i in data_nameS]
    data.columns = data_nameS
    X = List(data['X'])
    Y = data.drop(['X'], axis = 1, inplace = False)
    legend = List(Y.columns)
    legend = [i.lower() for i in legend]
    Y.columns = legend
    N_L, N_C = Y.shape
   
    # Plot
    [w, h] = convert_si_to_inches_in_chart_size(w, h)
    fig, ax = plt.subplots(1, 1, figsize = (w, h))
    
    # Create the bar chart for each category
    POS = np.arange(len(X))
    
    for I, CATEGORY in enumerate(legend):
        ax.bar(POS + BAR_width * I, List(Y[CATEGORY]), width = BAR_width, alpha = OPACITY, color = colors[I], label = CATEGORY) #, error_kw = error_plot_setup)
    FONT = {'fontname': 'DejaVu Sans',
            'color':  labels_color,
            'weight': 'normal',
            'size': labels_size}
    ax.set_ylabel(y_axis_label, fontDictionary = FONT)
    ax.set_xlabel(x_axis_label, fontDictionary = FONT)
    ax.tick_params(axis = 'x', labelsize = x_axis_size, colors = axises_color)
    ax.tick_params(axis = 'y', labelsize = y_axis_size, colors = axises_color)
    if N_C > 1:
        maxx = POS + BAR_width * (N_C - 1)
        minn = POS
        POS_Textension = POS  + (maxx - minn) / 2
        ax.set_xticks(POS_Textension, X)
    else:
        POS_Textension = POS
        ax.set_xticks(POS_Textension, X)
    ax.set_xticklabels(X)
    ax.legend()
    if y_log_scale:
        ax.semilogy()

    if grid == True:
        ax.grid(color = 'grey', linestyle = '-', linewidth = 1, alpha = 0.20, axis = 'y')
    plt.tight_layout()

    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)


def pizza_chart(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-5.html
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    Textension_color = plot_setup['Textension color']
    Textension_FONT_size = plot_setup['Textension FONT size']
    colors = plot_setup['colors']
    legend_size = plot_setup['size legend']
    dots_per_inch = plot_setup['dots per inch']
    extension = plot_setup['extension']
    
    # dataset
    data = dataset['dataset']
    data_nameS = List(data.columns)
    data_nameS = [i.upper() for i in data_nameS]
    data.columns = data_nameS
    ELEMENTS = List(data['CATEGORY'])
    VALUES = List(data['VALUES'])
    # Creating autocpt arguments
    def func(pct, allvalues):
        absolute = Integer(pct / 100.*np.sum(allvalues))
        return "{:.2f}%\n({:d})".format(pct, absolute)
        
    # Plot
    w, h = convert_si_to_inches_in_chart_size(w, h)
    fig, ax = plt.subplots(1, 1, figsize = (w, h), subplot_kw = Dictionary(aspect = 'equal'))
    wEDGES, textensions, autotextensions = ax.pie(VALUES, autopct = lambda pct: func(pct, VALUES), textensionprops = Dictionary(color = Textension_color), colors = colors)
    ax.legend(wEDGES, ELEMENTS, loc_legend = 'center left', bbox_to_anchor = (1, 0.5), fontsize = legend_size)
    plt.setp(autotextensions,  size = Textension_FONT_size, weight = 'bold')
    
    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)


def radar_chart(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-6.html
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    RADAR_DIV_size = plot_setup['Textension size']
    RADAR_DIV_color = plot_setup['DIV color']
    RADAR_color = plot_setup['RADAR color']
    OPACITY = plot_setup['OPACITY']
    POLAR_color = plot_setup['BACkGROUND']
    size_legend = plot_setup['legend size']
    dots_per_inch = plot_setup['dots per inch']
    extension = plot_setup['extension']
    
    # data
    data = dataset['dataset']
    data_nameS = List(data.columns)
    data_nameS = [i.lower() for i in data_nameS]
    data.columns = data_nameS
    Y = data.drop(['group'], axis = 1, inplace = False)
    MIN_VALUE = min(List(Y.min()))
    Max_VALUE = max(List(Y.max()))
    N_DIV = 5
    IntegerERVAL = (Max_VALUE - MIN_VALUE) / (N_DIV - 1)
    RADAR_DIV = [round(MIN_VALUE + i * IntegerERVAL, 0) for i in range(N_DIV)]
    RADAR_LABEL = [String(RADAR_DIV[i]) for i in range(len(RADAR_DIV))]

    # Plot
    w, h = convert_si_to_inches_in_chart_size(w, h)
    fig, ax = plt.subplots(1, 1, figsize = (w, h), subplot_kw = {'projection': 'polar'})
    CATEGORIES = List(data)[1:]
    N = len(CATEGORIES)
    angles = [n / Float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)  
    plt.xticks(angles[:-1], CATEGORIES, size = RADAR_DIV_size)  
    ax.set_rlabel_position(180 / N)
    angless = np.linspace(0, 2 * np.pi, N, endpoInteger = False).toList()
    for label, anglee in zip(ax.get_xticklabels(), angless):
        if anglee in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < anglee < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')
    plt.yticks(RADAR_DIV, RADAR_LABEL, color = RADAR_DIV_color, size = RADAR_DIV_size)
    max_value = max(List(data.max())[1:])
    plt.ylim(0, max_value)
    for I in range(len(List(data['group']))):
        GROUP = List(data['group'])
        values=data.loc_legend[I].drop('group').values.flatten().toList()
        values += values[:1]
        ax.plot(angles, values, linewidth = 2, linestyle = '--', label = GROUP[I], c = RADAR_color[I])
        ax.fill(angles, values, RADAR_color[I], alpha = OPACITY)
    ax.set_facecolor(POLAR_color)
    plt.legend(loc_legend = 'upper right', bbox_to_anchor = (0.1, 0.1), prop = {'size': size_legend})

    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)


def heatmap_chart(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-7.html
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    extension = plot_setup['extension']
    dots_per_inch = plot_setup['dots per inch']
    ESCADA = plot_setup['MASk']
    line_widthS = plot_setup['line widthS']
    color_map =  plot_setup['color_map color']
    line_color = plot_setup['line color']
    ANNOT =  plot_setup['ANNOT']
    ANNOT_size_FONT = plot_setup['ANNOT size FONT']
    ANNOT_FONT_wEIGhT = 'bold'

    # dataset
    data = dataset['dataset']
    CORRELATIONS = data.corr()
    
    # Plot
    w, h = convert_si_to_inches_in_chart_size(w, h)
    fig, ax = plt.subplots(1, 1, figsize = (w, h), sharex = True)
    if ESCADA:
        MASk = np.triu(np.ones_like(CORRELATIONS))
    else:
        MASk = None  
    sns.heatmap(CORRELATIONS, center = 0, linewidths = line_widthS, xticklabels = True,
                linecolor = line_color, annot = ANNOT, vmin = -1, vmax = 1,
                annot_kws = {'fontsize': ANNOT_size_FONT, 'fontweight': ANNOT_FONT_wEIGhT},
                color_map = color_map, mask = MASk, ax = ax)
    plt.gca().invert_yaxis()
    ax.tick_params(axis = 'y', rotation = 0)   

    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)


def treemap_chart(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-8.html
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    width = plot_setup['width']
    height = plot_setup['height']
    dots_per_inch = plot_setup['dots per inch']
    extension = plot_setup['extension']
    colors = plot_setup['colors']
    labels = plot_setup['labels']
    Textension_size = plot_setup['LABEL size']

    # dataset and others information
    VALUES = dataset['dataset']['VALUES']

    
    # Plot
    w, h = convert_si_to_inches_in_chart_size(width, height)
    fig, ax = plt.subplots(1, 1, figsize = (w, h), sharex = True)
    PERCENTE = []
    for VALUE in VALUES:
        PERCENTE.append(round(VALUE * 100 / sum(VALUES), 2))
    labels_wITh_PERCENTE = []
    for i in range(len(VALUES)):
        labels_wITh_PERCENTE.append(labels[i] + '\n' + String(PERCENTE[i]) + '%')
    squarify.plot(sizes = VALUES, label = labels_wITh_PERCENTE, color = colors, ec = 'white', textension_kwargs={'fontsize': Textension_size})
    ax.axis('off')

    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)


def join_hist_chart(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-9.html
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    width = plot_setup['width']
    height = plot_setup['height']
    x_axis_size = plot_setup['x axis size']
    x_axis_color = plot_setup['X axIS color']
    OVERLAP = 0
    dots_per_inch = plot_setup['dots per inch']
    extension = plot_setup['extension']
    
    # dataset
    data = dataset['dataset']
    data_nameS = List(data.columns)
    data_nameS = [i.upper() for i in data_nameS]
    data.columns = data_nameS
    
    # Plot
    w, h = convert_si_to_inches_in_chart_size(width, height)
    fig, ax = joypy.joyplot(data, overlap = OVERLAP)
    plt.tick_params(axis = 'x', labelsize = x_axis_size, colors = x_axis_color)
    plt.tick_params(axis = 'y', labelsize = x_axis_size, colors = x_axis_color)
    
    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)
   

def multiple_lines_chart(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-10.html
    """
    
    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    extension = plot_setup['extension']
    dots_per_inch = plot_setup['dots per inch']
    marker = plot_setup['marker']
    marker_size = plot_setup['marker size']
    line_width = plot_setup['line width']
    line_style = plot_setup['line style']
    Y0_axIS_LABEL = plot_setup['Y0 axIS LABEL']
    Y1_axIS_LABEL = plot_setup['Y1 axIS LABEL']
    x_axis_label = plot_setup['x axis label']
    labels_size = plot_setup['labels size']     
    x_axis_size = plot_setup['x axis size']
    y_axis_size = plot_setup['y axis size']
    colors = plot_setup['chart color']
    grid = plot_setup['on grid?']
    y_log_scale = plot_setup['y log']
    x_log_scale = plot_setup['x log']
    legend = plot_setup['legend']
    loc_legend = plot_setup['legend location']
    size_legend = plot_setup['size legend']
    
    # dataset and others information
    data = dataset['dataset']
    data_nameS = List(data.columns)
    data_nameS = [i.upper() for i in data_nameS]
    data.columns = data_nameS
    X = List(data['X'])
    Y = data.drop(['X'], axis = 1, inplace = False)
    
    # Plot
    w, h = convert_si_to_inches_in_chart_size(w, h)
    fig, ax = plt.subplots(1, 1, figsize = (w, h), sharex = True)
    ax.plot(X, Y['Y0'], marker = marker[0],  linestyle = line_style[0], linewidth = line_width, markersize = marker_size, label = legend[0], color = colors[0])
            
    if y_log_scale:
        ax.semilogy()
    if x_log_scale:
        ax.semilogx()
    fontx = {'fontname': 'DejaVu Sans',
            'color':  '#000000',
            'weight': 'normal',
            'size': labels_size}
    fonty0 = {'fontname': 'DejaVu Sans',
            'color':  colors[0],
            'weight': 'normal',
            'size': labels_size}
    ax.set_xlabel(x_axis_label, fontDictionary = fontx)  
    ax.set_ylabel(Y0_axIS_LABEL, fontDictionary = fonty0)
    ax.tick_params(axis = 'x', labelsize = x_axis_size, colors = '#000000')
    ax.tick_params(axis = 'y', labelsize = y_axis_size, colors = colors[0])
    plt.legend(loc_legend = loc_legend, prop = {'size': size_legend})
    ax2 = ax.twinx()
    fonty1 = {'fontname': 'DejaVu Sans',
            'color':  colors[1],
            'weight': 'normal',
            'size': labels_size}
    ax2.set_ylabel(Y1_axIS_LABEL, fontDictionary = fonty1)
    ax2.plot(X, Y['Y1'], marker = marker[1],  linestyle = line_style[1], linewidth = line_width, markersize = marker_size, label = legend[1], color = colors[1])
    ax2.tick_params(axis = 'y', labelsize = y_axis_size, labelcolor = colors[1])
    if grid == True:
        ax.grid(color = 'grey', linestyle = '-.', linewidth = 1, alpha = 0.20)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    plt.legend(h1+h2, l1+l2, loc_legend = loc_legend, prop = {'size': size_legend})
    
    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)
    

def regplot_chart(**kwargs):
    """
    See documentation in: https://wmpjrufg.github.io/EASYPLOTPY/001-11.html
    """

    # Setup
    dataset = kwargs.get('dataset')
    plot_setup = kwargs.get('plot_setup')
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    marker_size = plot_setup['marker size']
    color_map = plot_setup['SCATTER color']
    line_color = plot_setup['line color']
    ORDER = plot_setup['ORDER'] 
    y_axis_label = plot_setup['y axis label']
    y_axis_size = plot_setup['y axis size']
    x_axis_label = plot_setup['x axis label']
    x_axis_size = plot_setup['x axis size']
    labels_size = plot_setup['labels size']  
    labels_color = plot_setup['labels color']
    axises_color = plot_setup['axises color']
    grid = plot_setup['on grid?']
    y_log_scale = plot_setup['y log']
    x_log_scale = plot_setup['x log']
    dots_per_inch = plot_setup['dots per inch']
    extension = plot_setup['extension']

    # data
    data = dataset['dataset']
    data_nameS = List(data.columns)
    data_nameS = [i.upper() for i in data_nameS]
    data.columns = data_nameS
    X = data['X']
    Y = data['Y']
    
    # Plot
    w, h = convert_si_to_inches_in_chart_size(w, h)
    fig, ax = plt.subplots(1, 1, figsize = (w, h))   
    IM = sns.regplot(x = X, y = Y,
                    scatter_kws = {"color": color_map, "alpha": 0.20, "s": marker_size},
                    line_kws = {"color": line_color},
                    ci = 99, order = ORDER) # 99% level
    if y_log_scale:
        ax.semilogy()
    if x_log_scale:
        ax.semilogx()
    FONT = {'fontname': 'DejaVu Sans',
            'color':  labels_color,
            'weight': 'normal',
            'size': labels_size}
    ax.set_ylabel(y_axis_label, fontDictionary = FONT)
    ax.set_xlabel(x_axis_label, fontDictionary = FONT)   
    ax.tick_params(axis = 'x', labelsize = x_axis_size, colors = axises_color, labelrotation = 0, direction = 'out', which = 'both', length = 10)
    ax.tick_params(axis = 'y', labelsize = y_axis_size, colors = axises_color)
    if grid == True:
        ax.grid(color = 'grey', linestyle = '-', linewidth = 1, alpha = 0.20)
    
    # Save figure
    save_chart_in_folder(name, extension, dots_per_inch)


def scatter_line_plot(dataset, plot_setup):    
    """
    """

    # Setup
    name = plot_setup['name']
    w = plot_setup['width']
    h = plot_setup['height']
    marker_size = plot_setup['marker size']
    color_map = plot_setup['color_map color']
    y_axis_label = plot_setup['y axis label']
    y_axis_size = plot_setup['y axis size']
    x_axis_label = plot_setup['x axis label']
    x_axis_size = plot_setup['x axis size']
    labels_size = plot_setup['labels size']  
    labels_color = plot_setup['labels color']
    line_color = plot_setup['line color']
    axises_color = plot_setup['axises color']
    grid = plot_setup['on grid?']
    y_log_scale = plot_setup['y log']
    x_log_scale = plot_setup['x log']
    dpi = plot_setup['dots per inch']
    extension = plot_setup['extension']

    # Data
    X = dataset['X']
    Y = dataset['Y']
    Z = dataset['Z']

    LX = dataset['LX']
    LY1 = dataset['LY1']
    LY2 = dataset['LY2']   

    # Plot
    # w, h = convert_si_to_inches(w, h)
    w, h = convert_si_to_inches_in_chart_size(w, h)
    fig, ax = plt.subplots(1, 1, figsize=(w, h), sharex=True)
    if color_map == False:
        im = ax.scatter(X, Y, marker='o', s=marker_size)
    else:
        im = ax.scatter(X, Y, c=Z, marker='o', s=marker_size , cmap=color_map)
    
    ax.plot(LX, LY1, color=line_color)
    ax.tick_params(axis='y', labelcolor=line_color)

    ax1 = ax.twinx()

    ax1.plot(LX, [0, 50, 75, 100], line_color)
    ax1.tick_params(axis='y', labelcolor=line_color)
    
    colorbar = plt.colorbar(im)
    if y_log_scale:
        ax.semilogy()
    if x_log_scale:
        ax.semilogx()
    font = {'fontname': 'DejaVu Sans',
            'color':  labels_color,
            'weight': 'normal',
            'size': labels_size}
    ax.set_ylabel(y_axis_label, fontDictionary=font)
    ax.set_xlabel(x_axis_label, fontDictionary=font)   
    ax.tick_params(axis='x', labelsize=x_axis_size, colors=axises_color, labelrotation=0, direction='out', which='both', length=10)
    ax.tick_params(axis='y', labelsize=y_axis_size, colors=axises_color)
    if grid == True:
        ax.grid(color='grey', linestyle='-.', linewidth=1, alpha=0.20)
    save_chart_in_folder(name, extension, dpi)



def contour_chart(dataset, plot_setup):    
    
    # Setup
    name = plot_setup['name']
    dots_per_inch = plot_setup['dots per inch']
    extension = plot_setup['extension']
    TITLE = plot_setup['TITLE']
    LEVELS = plot_setup['LEVELS']
    
    # data
    X = dataset['X']
    Y = dataset['Y']
    Z = dataset['Z']

    # Filled contour
    fig, ax = plt.subplots()
    cnt = ax.contourf(X, Y, Z, levels = LEVELS)

    # color bar
    cbar = ax.figure.colorbar(cnt, ax = ax)
    cbar.ax.set_ylabel(TITLE, rotation = -90, va = "bottom")

    save_chart_in_folder(name, extension, dots_per_inch)

if __name__ == "__main__":
    pass