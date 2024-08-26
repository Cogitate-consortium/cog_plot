import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import config
from matplotlib import font_manager

# get the parameters dictionary
param = config.param

# Set Helvetica as the default font:
font_path = os.path.join(os.path.dirname(__file__), "Helvetica.ttf")
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = prop.get_name()

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

fig_size = param["figure_size_mm"]
def_cmap = param["colors"]["cmap"]
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = param["font"]
plt.rc('font', size=param["font_size"])  # controls default text sizes
plt.rc('axes', titlesize=param["font_size"])  # fontsize of the axes title
plt.rc('axes', labelsize=param["font_size"])  # fontsize of the x and y labels
plt.rc('xtick', labelsize=param["font_size"])  # fontsize of the tick labels
plt.rc('ytick', labelsize=param["font_size"])  # fontsize of the tick labels
plt.rc('legend', fontsize=param["font_size"])  # legend fontsize
plt.rc('figure', titlesize=param["font_size"])  # fontsize of the fi


def mm2inch(val):
    return val / 25.4


def plot_matrix(data, x0, x_end, y0, y_end, mask=None, cmap=None, ax=None, ylim=None, midpoint=None, transparency=1.0,
                interpolation='lanczos',
                xlabel="Time (s)", ylabel="Time (s)", xticks=None, yticks=None, cbar_label="Accuracy", filename=None,
                vline=0,
                title=None, square_fig=False):
    """
    This function plots 2D matrices such as temporal generalization decoding or time frequency decompositions with or
    without significance. If a significance mask is passed, the significance pixels will be surrounded with significance
    line. The significance parts will be fully opaque but the non-significant patches transparency can be controlled
    by the transparency parameter
    :param data: (2D numpy array) data to plot
    :param x0: (float) first sample value for the x axis, for ex the first time point in the data to be able to
    create meaningful axes
    :param x_end: (float) final sample value for the x axis, for ex the last time point in the data to be able to create
    meaningful axes.
    :param y0: (float) first sample value for the y axis, for ex the first time point in the data to be able to
    create meaningful axes or the first frequency of a frequency decomposition...
    :param y_end: (float) final sample value for the y axis, for ex  the last time point in the data to be able to
    create meaningful axes or the first frequency of a frequency decomposition...
    :param mask: (2D numpy array of booleans) significance mask. MUST BE THE SAME SIZE as data. True where the data
    are significance, false elsewhere
    :param cmap: (string) name of the color map
    :param ax: (matplotlib ax object) ax on which to plot the data. If not passed, a new figure will be created
    :param ylim: (list of 2 floats) limits of the data for the plotting. If not passed, taking the 5 and 95 percentiles
    of the data
    :param midpoint: (float) midpoint of the data. Centers the color bar on this value.
    :param transparency: (float) transparency of the non-significant patches of the matrix
    :param xlabel: (string) xlabel fo the data
    :param ylabel: (string) ylabel fo the data
    :param xticks: (list of strings) xtick label names
    :param yticks: (list of strings) ytick label names
    :param cbar_label: (string) label of the color bar
    :param filename: (string or pathlib path object) name of the file to save the figures to. If not passed, nothing
    will be saved. Must be the full name with png extension. The script will take care of saving the data to svg as well
    and as csv
    :param vline: (float) coordinates of vertical and horizontal lines to plot
    :param title: (string) title of the figure
    :param square_fig: (boolean) whether or not to have the figure squared proportions. Useful for temporal
    generalization plots that are usually square!
    :return:
    """
    if ax is None:
        if square_fig:
            fig, ax = plt.subplots(figsize=[mm2inch(fig_size[0]),
                                            mm2inch(fig_size[0])])
        else:
            fig, ax = plt.subplots(figsize=[mm2inch(fig_size[0]),
                                            mm2inch(fig_size[1])])
    if ylim is None:
        ylim = [np.percentile(data, 5), np.percentile(data, 95)]

    if midpoint is None:
        midpoint = np.mean([ylim[0], ylim[1]])

    try:
        norm = matplotlib.colors.TwoSlopeNorm(vmin=ylim[0], vcenter=midpoint, vmax=ylim[1])
    except ValueError:
        print("WARNING: The midpoint is outside the range defined by ylim[0] and ylim[1]! We will continue without"
              "normalization")
        norm = None

    if cmap is None:
        cmap = def_cmap
    if square_fig:
        aspect = "equal"
    else:
        aspect = "auto"
    # Plot matrix with transparency:
    im = ax.imshow(data, cmap=cmap, norm=norm,
                   extent=[x0, x_end, y0, y_end],
                   origin="lower", alpha=transparency, aspect=aspect, interpolation=interpolation)
    # Plot the significance mask on top:
    if mask is not None:
        sig_data = data
        sig_data[~mask] = np.nan
        if not np.isnan(mask).all():
            # Plot only the significant bits:
            ax.imshow(sig_data, cmap=cmap, origin='lower', norm=norm,
                      extent=[x0, x_end, y0, y_end],
                      aspect=aspect, interpolation=interpolation)
            ax.contour(mask > 0, mask > 0, colors="k", origin="lower",
                       extent=[x0, x_end, y0, y_end])

    # Add the axis labels and so on:
    ax.set_xlim([x0, x_end])
    ax.set_ylim([y0, y_end])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)
    if title is not None:
        ax.set_title(title)
    ax.axvline(vline, color='k')
    ax.axhline(vline, color='k')
    plt.tight_layout()
    cb = plt.colorbar(im)
    cb.ax.set_ylabel(cbar_label)
    cb.ax.set_yscale('linear')  # To make sure that the spacing is correct despite normalization
    if filename is not None:
        # Save to png
        plt.savefig(filename, transparent=True, dpi=param["fig_res_dpi"])
        # Save to svg:
        filename, file_extension = os.path.splitext(filename)
        plt.savefig(filename + ".svg", transparent=True)
        # Save all inputs to csv:
        np.savetxt(filename + "_data" + ".csv", data, delimiter=",")
        if mask is not None:
            np.savetxt(filename + "_mask" + ".csv", mask, delimiter=",")

    return ax


def plot_pcolormesh(data, xs, ys, mask=None, cmap=None, ax=None, vlim=None, transparency=1.0,
                    xlabel="Time (s)", ylabel="Time (s)", cbar_label="Accuracy", filename=None, vline=0,
                    title=None, square_fig=False):
    if ax is None:
        if square_fig:
            fig, ax = plt.subplots(figsize=[mm2inch(fig_size[0]),
                                            mm2inch(fig_size[0])])
        else:
            fig, ax = plt.subplots(figsize=[mm2inch(fig_size[0]),
                                            mm2inch(fig_size[1])])

    if vlim is None:
        vlim = [np.percentile(data, 5), np.percentile(data, 95)]

    if cmap is None:
        cmap = def_cmap

    im = ax.pcolormesh(xs, ys, data,
                       cmap=cmap, vmin=vlim[0], vmax=vlim[1],
                       alpha=transparency, rasterized=True)

    if mask is not None:
        sig_data = data
        sig_data[~mask] = np.nan
        if not np.isnan(mask).all():
            ax.pcolormesh(xs, ys, sig_data,
                          cmap=cmap, vmin=vlim[0], vmax=vlim[1], rasterized=True)
            ax.contour(xs, ys, mask > 0, colors="k")

    # Add the axis labels and so on:
    ax.set_xlim([xs[0], xs[-1]])
    ax.set_ylim([ys[0], ys[-1]])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    ax.axvline(vline, color='k')
    ax.axhline(vline, color='k')
    plt.tight_layout()
    cb = plt.colorbar(im)
    cb.ax.set_ylabel(cbar_label)
    cb.ax.tick_params(labelsize=12)
    cb.ax.set_yscale('linear')  # To make sure that the spacing is correct despite normalization
    if filename is not None:
        # Save to png
        plt.savefig(filename, transparent=True, dpi=param["fig_res_dpi"])
        # Save to svg:
        filename, file_extension = os.path.splitext(filename)
        plt.savefig(filename + ".svg", transparent=True)
        plt.savefig(filename + ".pdf", transparent=True)
        # Save all inputs to csv:
        np.savetxt(filename + "_data" + ".csv", data, delimiter=",")
        if mask is not None:
            np.savetxt(filename + "_mask" + ".csv", mask, delimiter=",")

    return ax


def plot_time_series(data, t0, tend, ax=None, err=None, colors=None, vlines=None, xlim=None, ylim=None,
                     xlabel="Time (s)", ylabel="Activation", err_transparency=0.2,
                     filename=None, title=None, square_fig=False, conditions=None, do_legend=True,
                     patches=None, patch_color="r", patch_transparency=0.2):
    """
    This function plots times series such as average of iEEG activation across trials and/or electrodes... If the error
    parameter is passed, the error will be plotted as shaded around the main line. Additionally, patches
    can be plotted over the data to represent significance or time windows of interest... Additionally, vertical lines
    can be plotted to delimitate relevant time points.
    :param data: (2D numpy array) contains time series to plot. The first dimension should be different conditiosn
    and the last dimension is time! The first dimension here should be ordered according to the other parameters,
    such as the conditions, errors...
    :param t0: (float) time 0, i.e. the first time point in the data to be able to create meaningful axes
    :param tend: (float) final time point, i.e. the last time point in the data to be able to create meaningful axes
    :param ax: (matplotlib ax object) ax on which to plot the data. If not passed, a new figure will be created
    :param err: (2D numpy array) contains errors of the time series to plot. The first dimension should be different
    conditions and the last dimension is time! The first dimension here should be ordered according to the other
    parameters, such as the data, conditions...
    :param colors: (list of string or RGB float triplets) colors of each condition. There should be as many as there
    are rows in the data
    :param vlines: (list of floats) x coordinates at which to draw the vertical lines
    :param xlim: (list of 2 floats) limits of the x axis if any
    :param ylim: (list of 2 floats) limits of the y axis if any
        :param xlabel: (string) xlabel fo the data
    :param ylabel: (string) ylabel fo the data
    :param filename: (string or pathlib path object) name of the file to save the figures to. If not passed, nothing
    will be saved. Must be the full name with png extension. The script will take care of saving the data to svg as well
    and as csv
    :param title: (string) title of the figure
    :param square_fig: (boolean) whether or not to have the figure squared proportions. Useful for temporal
    generalization plots that are usually square!
    :param err_transparency: (float) transparency of the errors around the mean
    :param conditions: (list of strings) name of each condition to be plotted, for legend
    :param do_legend: (boolean) whether or not to plot the legend
    :param patches: (list of 2 floats of list of list) x coordinates of the start and end of a patch
    :param patch_color: (string or RGB triplet) color of the patch
    :param patch_transparency: (float) transparency of the patch
    :return:
    """
    if ax is None:
        if square_fig:
            fig, ax = plt.subplots(figsize=[mm2inch(fig_size[0]),
                                            mm2inch(fig_size[0])])
        else:
            fig, ax = plt.subplots(figsize=[mm2inch(fig_size[0]),
                                            mm2inch(fig_size[1])])
    if conditions is None:
        conditions = ["" for i in range(data.shape[0])]
    if colors is None:
        colors = [None for i in range(data.shape[0])]
    # Create the time axis:
    times = np.linspace(t0, tend, num=data.shape[1])
    # Plot matrix with transparency:
    for ind in range(data.shape[0]):
        ax.plot(times, data[ind], color=colors[ind],
                label=conditions[ind])
        # Plot the errors:
        if err is not None:
            ax.fill_between(times, data[ind] - err[ind], data[ind] + err[ind],
                            color=colors[ind], alpha=err_transparency)
    # Set the x limits:
    ax.set_xlim(times[0], times[-1])
    if xlim is not None:
        ax.set_xlim(xlim[0], xlim[-1])
    if ylim is not None:
        ax.set_ylim(ylim[0], ylim[-1])
    # Adding vlines:
    if vlines is not None:
        ax.vlines(vlines, ax.get_ylim()[0], ax.get_ylim()[1], linestyles='dashed', linewidth=1.5, colors='k')
    # Adding patches:
    if patches is not None:
        if not isinstance(patches[0], list):
            ax.axvspan(patches[0], patches[1], fc=patch_color, alpha=patch_transparency)
        else:
            for patch in patches:
                ax.axvspan(patch[0], patch[1], fc=patch_color, alpha=patch_transparency)

    # Add the labels title and so on:
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    if do_legend:
        ax.legend()
    plt.tight_layout()
    if filename is not None:
        # Save to png
        plt.savefig(filename, transparent=True, dpi=param["fig_res_dpi"])
        # Save to svg:
        filename, file_extension = os.path.splitext(filename)
        plt.savefig(filename + ".svg", transparent=True)
        # Save all inputs to csv:
        np.savetxt(filename + "_data" + ".csv", data, delimiter=",")
        np.savetxt(filename + "_error" + ".csv", err, delimiter=",")

    return ax


def plot_rasters(data, t0, tend, cmap=None, ax=None, ylim=None, midpoint=None, transparency=1.0,
                 xlabel="Time (s)", ylabel="Time (s)", cbar_label="Accuracy", filename=None, vlines=0,
                 title=None, square_fig=False, conditions=None, cond_order=None):
    """
    This function plots 2D matrices such as temporal generalization decoding or time frequency decompositions with or
    without significance. If a significance mask is passed, the significance pixels will be surrounded with significance
    line. The significance parts will be fully opaque but the non-significant patches transparency can be controlled
    by the transparency parameter
    :param data: (2D numpy array) data to plot
    :param t0: (float) time 0, i.e. the first time point in the data to be able to create meaningful axes
    :param tend: (float) final time point, i.e. the last time point in the data to be able to create meaningful axes
    :param cmap: (string) name of the color map
    :param ax: (matplotlib ax object) ax on which to plot the data. If not passed, a new figure will be created
    :param ylim: (list of 2 floats) limits of the data for the plotting. If not passed, taking the 5 and 95 percentiles
    of the data
    :param midpoint: (float) midpoint of the data. Centers the color bar on this value.
    :param transparency: (float) transparency of the non-significant patches of the matrix
    :param xlabel: (string) xlabel fo the data
    :param ylabel: (string) ylabel fo the data
    :param cbar_label: (string) label of the color bar
    :param filename: (string or pathlib path object) name of the file to save the figures to. If not passed, nothing
    will be saved. Must be the full name with png extension. The script will take care of saving the data to svg as well
    and as csv
    :param vlines: (float) coordinates of vertical and horizontal lines to plot
    :param title: (string) title of the figure
    :param square_fig: (boolean) whether or not to have the figure squared proportions. Useful for temporal
    generalization plots that are usually square!
    :param conditions: (list or iterable of some sort) condition of each trial to order them properly.
    :param cond_order: (list) order in which to sort the conditions. So say you are trying to plot faces,
    objects, letters and so on, and you want to enforce that in the plot the faces appear first, then the objects,
    then the letters, pass the list ["face", "object", "letter"]
    :return:
    """
    if ax is None:
        if square_fig:
            fig, ax = plt.subplots(figsize=[mm2inch(fig_size[0]),
                                            mm2inch(fig_size[0])])
        else:
            fig, ax = plt.subplots(figsize=[mm2inch(fig_size[0]),
                                            mm2inch(fig_size[1])])
    if ylim is None:
        ylim = [np.percentile(data, 5), np.percentile(data, 95)]
    if midpoint is not None:
        try:
            norm = matplotlib.colors.TwoSlopeNorm(vmin=ylim[0], vcenter=midpoint, vmax=ylim[1])
        except ValueError:
            print("WARNING: The midpoint is outside the range defined by ylim[0] and ylim[1]! We will continue without"
                  "normalization")
            norm = None
    else:
        norm = None
    if cmap is None:
        cmap = def_cmap
    if square_fig:
        aspect = "equal"
    else:
        aspect = "auto"
    # Sorting the epochs if not plotting:
    if conditions is not None:
        conditions = np.array(conditions)
        if cond_order is not None:
            inds = []
            for cond in cond_order:
                inds.append(np.where(conditions == cond)[0])
            inds = np.concatenate(inds)
        else:
            inds = np.argsort(conditions)
        data = data[inds, :]
    # Plot matrix with transparency:
    im = ax.imshow(data, cmap=cmap, norm=norm,
                   extent=[t0, tend, 0, data.shape[0]],
                   origin="lower", alpha=transparency, aspect=aspect)
    # Sort the conditions accordingly:
    if conditions is not None:
        conditions = conditions[inds]
        if cond_order is not None:
            y_labels = cond_order
        else:
            y_labels = np.unique(conditions)
        # Convert the conditions to numbers:
        for ind, cond in enumerate(y_labels):
            conditions[np.where(conditions == cond)[0]] = ind
        hlines_loc = np.where(np.diff(conditions.astype(int)) == 1)[0] + 1
        # Plot horizontal lines to delimitate the conditions:
        [ax.axhline(loc, color='k', linestyle=":") for loc in hlines_loc]
        # Add the tick marks in between each hline:
        ticks = []
        for ind, loc in enumerate(hlines_loc):
            if ind == 0:
                ticks.append(loc / 2)
            else:
                ticks.append(loc - ((loc - hlines_loc[ind - 1]) / 2))
        # Add the last tick:
        ticks.append(hlines_loc[-1] + ((data.shape[0] - hlines_loc[-1]) / 2))
        ax.set_yticks(ticks)
        ax.set_yticklabels(y_labels)

    # Add the axis labels and so on:
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    if vlines is not None:
        ax.vlines(vlines, ax.get_ylim()[0], ax.get_ylim()[1], linestyles='dashed', linewidth=1, colors='k')
    plt.tight_layout()
    cb = plt.colorbar(im)
    cb.ax.set_ylabel(cbar_label)
    cb.ax.set_yscale('linear')  # To make sure that the spacing is correct despite normalization
    if filename is not None:
        # Save to png
        plt.savefig(filename, transparent=True, dpi=param["fig_res_dpi"])
        # Save to svg:
        filename, file_extension = os.path.splitext(filename)
        plt.savefig(filename + ".svg", transparent=True)
        # Save all inputs to csv:
        np.savetxt(filename + "_data" + ".csv", data, delimiter=",")

    return ax
