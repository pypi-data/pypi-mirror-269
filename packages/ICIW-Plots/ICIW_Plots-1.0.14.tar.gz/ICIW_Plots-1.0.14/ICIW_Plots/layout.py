import matplotlib
import matplotlib.gridspec
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import Divider, Size
import numpy.typing as npt


def make_square_ax(
    fig: matplotlib.figure.Figure,
    left_h: float,
    bottom_v: float,
    ax_width: float,
) -> matplotlib.axes.Axes:
    fig_width, fig_height = fig.get_size_inches()

    if ax_width + left_h >= fig_width:
        raise ValueError("Axes width exceeds figure width")
    if ax_width + bottom_v >= fig_height:
        raise ValueError("Axes height exceeds figure height")

    top_v = fig_height - ax_width - bottom_v
    right_h = fig_width - ax_width - left_h
    h = [Size.Fixed(left_h), Size.Scaled(1), Size.Fixed(right_h)]
    v = [Size.Fixed(bottom_v), Size.Scaled(1), Size.Fixed(top_v)]
    div = Divider(fig, (0.0, 0.0, 1.0, 1.0), h, v, aspect=False)
    ax = fig.add_axes(div.get_position(), axes_locator=div.new_locator(nx=1, ny=1))
    return ax


def make_square_axs(
    fig: matplotlib.figure.Figure,
    left_h: float,
    bottom_v: float,
    ax_width: float,
    ax_layout: tuple[int, int] = (1, 1),
    v_sep: float = 0.05,
    h_sep: float = 0.05,
):

    fig_width = float(fig.get_figwidth())
    fig_height = float(fig.get_figheight())

    n_rows, n_cols = ax_layout
    n_row_skips = n_rows - 1
    n_col_skips = n_cols - 1

    if (n_rows * ax_width) + left_h + (n_row_skips * v_sep) >= fig_width:
        raise ValueError(
            "Axes widths exceed figure width. Try adjusting v_sep or fig_height."
        )
    if (n_cols * ax_width) + bottom_v + (n_col_skips * h_sep) >= fig_height:
        raise ValueError(
            "Axes heights exceed figure height. Try adjusting h_sep or fig_width."
        )

    h_frac = left_h / fig_width
    v_frac = bottom_v / fig_height

    axs_width = n_cols * ax_width + n_col_skips * h_sep
    axs_width_frac = axs_width / fig_width
    axs_height = n_rows * ax_width + n_row_skips * v_sep
    axs_height_frac = axs_height / fig_height

    total_height_frac = axs_height_frac + v_frac
    total_width_frac = axs_width_frac + h_frac

    gs = fig.add_gridspec(
        nrows=n_rows,
        ncols=n_cols,
        wspace=h_frac,
        hspace=v_frac,
        left=h_frac,
        bottom=v_frac,
        right=total_width_frac,
        top=total_height_frac,
    )

    for i in range(n_rows):
        for j in range(n_cols):
            fig.add_subplot(gs[i, j])
