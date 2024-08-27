import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# Set arial as the default font:
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial'],
    'axes.unicode_minus': False  # This ensures that minus signs are rendered correctly
})

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['svg.fonttype'] = 'none'

fig_size = [183, 108]
def_cmap = 'RdYlBu_r'
plt.rc('font', size=22)  # controls default text sizes
plt.rc('axes', titlesize=22)  # fontsize of the axes title
plt.rc('axes', labelsize=22)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=22)  # fontsize of the tick labels
plt.rc('ytick', labelsize=22)  # fontsize of the tick labels
plt.rc('legend', fontsize=22)  # legend fontsize
plt.rc('figure', titlesize=22)  # fontsize of the fi


def _mm2inch(val):
    """
    Convert millimeters to inches.

    Parameters
    ----------
    val : float
        Value in millimeters.

    Returns
    -------
    float
        Value converted to inches.
    """
    return val / 25.4


def plot_matrix(data, x0, x_end, y0, y_end, mask=None, cmap=None, ax=None, ylim=None, midpoint=None, transparency=1.0,
                interpolation='lanczos',
                xlabel="Time (s)", ylabel="Time (s)", xticks=None, yticks=None, cbar_label="Accuracy", filename=None,
                vline=0,
                title=None, square_fig=False, dpi=300):
    """
    Plot a 2D matrix with optional significance mask.

    This function is used to plot 2D matrices, such as temporal generalization decoding or time-frequency decompositions,
    with or without significance masking.

    Parameters
    ----------
    data : 2D numpy array
        Data to plot.
    x0 : float
        First sample value for the x-axis (e.g., the first time point in the data).
    x_end : float
        Final sample value for the x-axis (e.g., the last time point in the data).
    y0 : float
        First sample value for the y-axis (e.g., the first time point in the data).
    y_end : float
        Final sample value for the y-axis (e.g., the last time point in the data).
    mask : 2D numpy array of booleans, optional
        Significance mask (same size as data). True where the data are significant, False elsewhere.
    cmap : str, optional
        Name of the colormap.
    ax : matplotlib.axes.Axes, optional
        Axes on which to plot the data. If not provided, a new figure will be created.
    ylim : list of 2 floats, optional
        Limits for the color scale. If not provided, the 5th and 95th percentiles of the data will be used.
    midpoint : float, optional
        Midpoint of the data. Centers the color bar on this value.
    transparency : float, optional
        Transparency of the non-significant areas of the matrix.
    interpolation : str, optional
        Interpolation method for the image.
    xlabel : str, optional
        Label for the x-axis.
    ylabel : str, optional
        Label for the y-axis.
    xticks : list of str, optional
        Labels for the x-axis ticks.
    yticks : list of str, optional
        Labels for the y-axis ticks.
    cbar_label : str, optional
        Label for the color bar.
    filename : str or pathlib.Path, optional
        Name of the file to save the figure. If not provided, the figure will not be saved.
    vline : float, optional
        X-coordinate of vertical and horizontal lines to plot.
    title : str, optional
        Title of the figure.
    square_fig : bool, optional
        Whether to enforce square proportions for the figure.
    dpi : int, optional
        Dots per inch (DPI) for the saved figure.

    Returns
    -------
    matplotlib.axes.Axes
        The axis on which the plot was drawn.
    """
    if ax is None:
        if square_fig:
            fig, ax = plt.subplots(figsize=[_mm2inch(fig_size[0]),
                                            _mm2inch(fig_size[0])])
        else:
            fig, ax = plt.subplots(figsize=[_mm2inch(fig_size[0]),
                                            _mm2inch(fig_size[1])])
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
        plt.savefig(filename, transparent=True, dpi=dpi)
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
                    title=None, square_fig=False, dpi=300):
    """
    Plot a 2D pcolormesh with optional significance mask.

    This function is used to plot 2D data with optional masking for significance.

    Parameters
    ----------
    data : 2D numpy array
        Data to plot.
    xs : 1D array-like
        X coordinates for the pcolormesh.
    ys : 1D array-like
        Y coordinates for the pcolormesh.
    mask : 2D numpy array of booleans, optional
        Significance mask (same size as data). True where the data are significant, False elsewhere.
    cmap : str, optional
        Name of the colormap.
    ax : matplotlib.axes.Axes, optional
        Axes on which to plot the data. If not provided, a new figure will be created.
    vlim : list of 2 floats, optional
        Limits for the color scale. If not provided, the 5th and 95th percentiles of the data will be used.
    transparency : float, optional
        Transparency of the non-significant areas of the matrix.
    xlabel : str, optional
        Label for the x-axis.
    ylabel : str, optional
        Label for the y-axis.
    cbar_label : str, optional
        Label for the color bar.
    filename : str or pathlib.Path, optional
        Name of the file to save the figure. If not provided, the figure will not be saved.
    vline : float, optional
        X-coordinate of vertical and horizontal lines to plot.
    title : str, optional
        Title of the figure.
    square_fig : bool, optional
        Whether to enforce square proportions for the figure.
    dpi : int, optional
        Dots per inch (DPI) for the saved figure.

    Returns
    -------
    matplotlib.axes.Axes
        The axis on which the plot was drawn.
    """
    if ax is None:
        if square_fig:
            fig, ax = plt.subplots(figsize=[_mm2inch(fig_size[0]),
                                            _mm2inch(fig_size[0])])
        else:
            fig, ax = plt.subplots(figsize=[_mm2inch(fig_size[0]),
                                            _mm2inch(fig_size[1])])

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
        plt.savefig(filename, transparent=True, dpi=300)
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
                     patches=None, patch_color="r", patch_transparency=0.2, dpi=300):
    """
    Plot time series data with optional error shading and significance patches.

    This function is used to plot time series data, with options to include error shading, significance patches, and
    vertical lines for important time points.

    Parameters
    ----------
    data : 2D numpy array
        Time series data to plot. The first dimension should represent different conditions, and the second dimension is time.
    t0 : float
        Start time (e.g., first time point in the data).
    tend : float
        End time (e.g., last time point in the data).
    ax : matplotlib.axes.Axes, optional
        Axes on which to plot the data. If not provided, a new figure will be created.
    err : 2D numpy array, optional
        Error values corresponding to the time series data. The first dimension should represent different conditions, and the second dimension is time.
    colors : list of str or RGB tuples, optional
        Colors for each condition. There should be as many colors as there are rows in the data.
    vlines : list of floats, optional
        X-coordinates at which to draw vertical lines.
    xlim : list of 2 floats, optional
        Limits for the x-axis.
    ylim : list of 2 floats, optional
        Limits for the y-axis.
    xlabel : str, optional
        Label for the x-axis.
    ylabel : str, optional
        Label for the y-axis.
    err_transparency : float, optional
        Transparency for the error shading.
    filename : str or pathlib.Path, optional
        Name of the file to save the figure. If not provided, the figure will not be saved.
    title : str, optional
        Title of the figure.
    square_fig : bool, optional
        Whether to enforce square proportions for the figure.
    conditions : list of str, optional
        Names of each condition for the legend.
    do_legend : bool, optional
        Whether to include a legend in the plot.
    patches : list of lists or list of tuples, optional
        X-coordinates of the start and end of patches to be drawn over the data.
    patch_color : str or RGB tuple, optional
        Color for the patches.
    patch_transparency : float, optional
        Transparency for the patches.
    dpi : int, optional
        Dots per inch (DPI) for the saved figure.

    Returns
    -------
    matplotlib.axes.Axes
        The axis on which the plot was drawn.
    """
    if ax is None:
        if square_fig:
            fig, ax = plt.subplots(figsize=[_mm2inch(fig_size[0]),
                                            _mm2inch(fig_size[0])])
        else:
            fig, ax = plt.subplots(figsize=[_mm2inch(fig_size[0]),
                                            _mm2inch(fig_size[1])])
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
        plt.savefig(filename, transparent=True, dpi=dpi)
        # Save to svg:
        filename, file_extension = os.path.splitext(filename)
        plt.savefig(filename + ".svg", transparent=True)
        # Save all inputs to csv:
        np.savetxt(filename + "_data" + ".csv", data, delimiter=",")
        np.savetxt(filename + "_error" + ".csv", err, delimiter=",")

    return ax


def plot_rasters(data, t0, tend, cmap=None, ax=None, ylim=None, midpoint=None, transparency=1.0,
                 xlabel="Time (s)", ylabel="Time (s)", cbar_label="Accuracy", filename=None, vlines=0,
                 title=None, square_fig=False, conditions=None, cond_order=None, dpi=300):
    """
    Plot raster data with optional sorting by conditions.

    This function is used to plot 2D raster data with optional sorting by conditions.

    Parameters
    ----------
    data : 2D numpy array
        Data to plot.
    t0 : float
        Start time (e.g., first time point in the data).
    tend : float
        End time (e.g., last time point in the data).
    cmap : str, optional
        Name of the colormap.
    ax : matplotlib.axes.Axes, optional
        Axes on which to plot the data. If not provided, a new figure will be created.
    ylim : list of 2 floats, optional
        Limits for the color scale.
    midpoint : float, optional
        Midpoint of the data. Centers the color bar on this value.
    transparency : float, optional
        Transparency of the non-significant areas of the matrix.
    xlabel : str, optional
        Label for the x-axis.
    ylabel : str, optional
        Label for the y-axis.
    cbar_label : str, optional
        Label for the color bar.
    filename : str or pathlib.Path, optional
        Name of the file to save the figure. If not provided, the figure will not be saved.
    vlines : float or list of floats, optional
        X-coordinates of vertical lines to draw.
    title : str, optional
        Title of the figure.
    square_fig : bool, optional
        Whether to enforce square proportions for the figure.
    conditions : list or array-like, optional
        Conditions for each trial to order them.
    cond_order : list of str, optional
        Order in which to sort the conditions.
    dpi : int, optional
        Dots per inch (DPI) for the saved figure.

    Returns
    -------
    matplotlib.axes.Axes
        The axis on which the plot was drawn.
    """
    if ax is None:
        if square_fig:
            fig, ax = plt.subplots(figsize=[_mm2inch(fig_size[0]),
                                            _mm2inch(fig_size[0])])
        else:
            fig, ax = plt.subplots(figsize=[_mm2inch(fig_size[0]),
                                            _mm2inch(fig_size[1])])
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
        plt.savefig(filename, transparent=True, dpi=dpi)
        # Save to svg:
        filename, file_extension = os.path.splitext(filename)
        plt.savefig(filename + ".svg", transparent=True)
        # Save all inputs to csv:
        np.savetxt(filename + "_data" + ".csv", data, delimiter=",")

    return ax
