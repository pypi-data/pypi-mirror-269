#!/usr/bin/env python3

import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
from typing import Union

from .configuration import Config
from .statsdata import WorkStatsData, TotStatsData


_plotkwargs = {
    "linewidth": 2,
    "linestyle": "-",
    "alpha": 0.75,
}

_scatterkwargs = {
    "s": 10,
    "alpha": 0.75,
}


def _set_matplotlib_style():
    styles = [
        #  "seaborn-v0_8-darkgrid",
        "ggplot"
    ]

    for style in styles:
        if style in matplotlib.style.available:
            plt.style.use(style)
            return


def _plot_on_axis(
    ax: matplotlib.axes.Axes,
    abscissa: Union[pd.DataFrame, pd.Series],
    ordinate: Union[pd.DataFrame, pd.Series],
    prettify: bool = True,
):
    """
    Plot abscissa data on the x-axis and ordinate data on the y-axis.
    Set x_label and y_label according to data names.
    """

    ax.plot(abscissa, ordinate, **_plotkwargs)
    ax.scatter(abscissa, ordinate, **_scatterkwargs)

    #  ax.set_xlabel(abscissa.name)
    ax.set_ylabel(ordinate.name)
    if prettify:
        ax.grid(True)
        ax.tick_params(axis="x", labelrotation=45)

    return


def _plot_all_normalized_on_axis(
    ax: matplotlib.axes.Axes,
    data: pd.DataFrame,
    legendax: matplotlib.axes.Axes = None,
    prettify: bool = True,
):
    """
    plot all columns of the dataframe and normalize data by setting the last
    entry as 1.

    If `legendax` is not none, that axis will be used to display the legend.
    """

    time = data["Timestamp"]
    handles = []
    labels = []

    skip_columns = ["Timestamp", "index", "Title", "Fandom", "ID"]

    for col in data.columns:
        if col in skip_columns:
            continue

        d = data[col]
        val = d.iat[-1]
        d_norm = d / val

        (h,) = ax.plot(time, d_norm, label=col, **_plotkwargs)
        ax.scatter(time, d_norm, **_scatterkwargs)

        handles.append(h)
        labels.append(col)

    #  ax.set_xlabel("Timestamp")
    ax.set_ylabel("All data (normalized)")

    if legendax is None:
        ax.legend(loc="upper left", ncols=2, frameon=True)
    else:
        legendax.grid(False)
        legendax.axis("off")
        legendax.legend(handles=handles, labels=labels, loc="center left")

    if prettify:
        ax.tick_params(axis="x", labelrotation=45)
        ax.grid(True)

    return


def plot_total_stats(tsfiles: list, conf: Config):
    """
    Plots the total user statistics.

    tsfiles: list
        list of file names of total user statistics to read in

    conf:
        AO3Stats configuration object
    """

    prettify = conf.plotting.prettify

    # Grab data
    ts_data = []

    for f in tsfiles:
        ts = TotStatsData(conf, source=f)
        ts.data["Timestamp"] = ts.timestamp

        ts_data.append(ts.data)

    # Combine it into a single dataframe
    alldata = pd.concat(ts_data)
    alldata.reset_index(inplace=True)
    alldata.sort_values(by="Timestamp")

    # get shorthands
    time = alldata["Timestamp"]
    user_subscriptions = alldata["User Subscriptions"]
    kudos = alldata["Kudos"]
    comments = alldata["Comment Threads"]
    bookmarks = alldata["Bookmarks"]
    subscriptions = alldata["Subscriptions"]
    words = alldata["Word Count"]
    hits = alldata["Hits"]

    if prettify:
        _set_matplotlib_style()

    fig = plt.figure()
    fig.suptitle("Total User Statistics")

    ax1 = fig.add_subplot(3, 3, 1)
    ax2 = fig.add_subplot(3, 3, 2)
    ax3 = fig.add_subplot(3, 3, 3)
    ax4 = fig.add_subplot(3, 3, 4)
    ax5 = fig.add_subplot(3, 3, 5)
    ax6 = fig.add_subplot(3, 3, 6)
    ax7 = fig.add_subplot(3, 3, 7)
    ax8 = fig.add_subplot(3, 3, 8)
    ax9 = fig.add_subplot(3, 3, 9)

    _plot_on_axis(ax1, time, user_subscriptions, prettify)
    _plot_on_axis(ax2, time, kudos, prettify)
    _plot_on_axis(ax3, time, comments, prettify)
    _plot_on_axis(ax4, time, bookmarks, prettify)
    _plot_on_axis(ax5, time, subscriptions, prettify)
    _plot_on_axis(ax6, time, words, prettify)
    _plot_on_axis(ax7, time, hits, prettify)
    _plot_all_normalized_on_axis(ax8, alldata, ax9, prettify)

    if prettify:
        plt.subplots_adjust(
            top=0.952, bottom=0.078, left=0.044, right=0.992, hspace=0.337, wspace=0.169
        )

    plt.show()

    return


def plot_work_stats(wsfiles: list, ID: int, conf: Config):
    """
    Plots the statistics of a single work specified via its AO3 ID.

    wsfiles: list
        list of file names of work statistics to read in

    ID: int
        AO3 ID of work to plot

    conf:
        AO3Stats configuration object
    """

    prettify = conf.plotting.prettify

    # Grab data
    ws_data = []

    for f in wsfiles:
        ws = WorkStatsData(conf, source=f)
        ws.data["Timestamp"] = ws.timestamp

        work = ws.data[ws.data["ID"] == ID]
        if work.empty:
            continue
        else:
            ws_data.append(work)

    if len(ws_data) == 0:
        raise ValueError(f"Didn't find any data on work with ID {ID}.")

    # Combine it into a single dataframe
    alldata = pd.concat(ws_data)
    alldata.reset_index(inplace=True)
    alldata.sort_values(by="Timestamp")

    # get shorthands
    time = alldata["Timestamp"]
    words = alldata["Words"]
    hits = alldata["Hits"]
    kudos = alldata["Kudos"]
    comments = alldata["Comment Threads"]
    bookmarks = alldata["Bookmarks"]
    subscriptions = alldata["Subscriptions"]

    title = alldata["Title"].at[0]

    if prettify:
        _set_matplotlib_style()

    fig1 = plt.figure()
    fig1.suptitle(f"Work Statistics for '{title}'")

    ax1 = fig1.add_subplot(2, 3, 1)
    ax2 = fig1.add_subplot(2, 3, 2)
    ax3 = fig1.add_subplot(2, 3, 3)
    ax4 = fig1.add_subplot(2, 3, 4)
    ax5 = fig1.add_subplot(2, 3, 5)
    ax6 = fig1.add_subplot(2, 3, 6)

    _plot_on_axis(ax1, time, words, prettify)
    _plot_on_axis(ax2, time, hits, prettify)
    _plot_on_axis(ax3, time, kudos, prettify)
    _plot_on_axis(ax4, time, comments, prettify)
    _plot_on_axis(ax5, time, bookmarks, prettify)
    _plot_on_axis(ax6, time, subscriptions, prettify)

    if prettify:
        plt.subplots_adjust(
            top=0.952, bottom=0.078, left=0.044, right=0.992, hspace=0.337, wspace=0.169
        )

    fig2, axes2 = plt.subplots(1, 2, width_ratios=[3, 1])
    fig2.suptitle(f"Work Statistics for '{title}'")
    ax21 = axes2[0]
    ax22 = axes2[1]

    _plot_all_normalized_on_axis(ax21, alldata, ax22, prettify)

    plt.show()

    return
