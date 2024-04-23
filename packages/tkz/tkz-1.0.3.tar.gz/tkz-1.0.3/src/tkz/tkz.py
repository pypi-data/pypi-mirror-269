"""
--------------------------------------------------------------------------------
Copyright 2022 David Woodburn

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
--------------------------------------------------------------------------------
This package is meant for the average Python user who does not necessarily know
much of anything about the TikZ package. Its interface is meant to be similar to
other packages like MatPlotLib, though perhaps more object-oriented in its use
of object fields rather than functions (e.g., xlabel()). So, it does not require
that the user know about the various names of predefined line widths or the
names of line styles (e.g., "dashdotted"). However, it is meant to also be
flexible enough for the user who is familiar with the options of the TikZ
package. This is enabled through the "fmt" parameter.
"""

__author__ = "David Woodburn"
__license__ = "MIT"
__date__ = "2024-04-22"
__maintainer__ = "David Woodburn"
__email__ = "david.woodburn@icloud.com"
__status__ = "Development"

import os
import warnings
import math                         # 5-10x faster than NumPy for scalars
import numpy as np

# Generic constants
PT_PER_CM = 28.45274                # points per centimeter
WIDTH = 8.636                       # default figure width (cm)
TICK_SIZE = 0.1                     # default tick mark size (cm)
LEGEND_RATIO = 0.03                 # of figure width (cm/cm)

# Predefined TikZ line styles
SOLID           = 0                 # ----
DASHDOTTED      = 1                 # -.-.
DASHED          = 2                 # - -
DENSELYDOTTED   = 3                 # ....
DOTTED          = 4                 # . .
LOOSELYDOTTED   = 5                 # .  .

# Marker styles
CIRCLES         = 0                 # o
DOTS            = 1                 # .

# Predefined TikZ edge thicknesses
THINEST         = 0.05              # (pt)
ULTRA_THIN      = 0.1               # (pt)
VERY_THIN       = 0.2               # (pt)
THIN            = 0.4               # (pt)
SEMI_THICK      = 0.6               # (pt)
THICK           = 0.8               # (pt)
VERY_THICK      = 1.2               # (pt)
ULTRA_THICK     = 1.6               # (pt)
THICKEST        = 100.0             # (pt)

# Key color values
BLUE            = 0x0000ff          #   0    0  255
AZURE           = 0x0080ff          #   0  128  255
CYAN            = 0x00d1d1          #   0  209  209
GREEN           = 0x0fb400          #  15  180    0
LIME            = 0xa9cb00          # 169  203    0
YELLOW          = 0xffbf00          # 255  191    0
ORANGE          = 0xff8000          # 255  128    0
RED             = 0xff0000          # 255    0    0
MAGENTA         = 0xff00ff          # 255    0  255
PURPLE          = 0x8000ff          # 128    0  255

# Color maps
MAP_WHEEL = [BLUE, AZURE, CYAN, GREEN, LIME,
        YELLOW, ORANGE, RED, MAGENTA, PURPLE]

# Ratios of symbol widths to font size
R_SIGN = 0.75                       # sign width as ratio of font size
R_DIGIT = 0.5                       # digit width as ratio of font size
R_DECIMAL = 0.28                    # decimal width as ratio of font size
R_TIMES = 0.89                      # times width as ratio of font size
R_POWER = 0.85                      # scaling factor for widths in powers


# Library-wide attributes
class config:
    skip = False                    # flag to skip plotting
    silent = True                   # flag to silence pdflatex output
    directory = None                # directory for figure files
    colormap = MAP_WHEEL            # main color map


class GraphLayout:
    """ Settings for the layout of the graph. """
    def __init__(self): # These are the internal, calculated settings.
        self.width = 0.0            # width of figure (cm)
        self.height = 0.0           # height of figure (cm)
        self.font_size = 0.0        # font size (pt)
        self.font_size_name = ""    # font size name ("tiny", "large", ...)
        self.x_min = 0.0            # x-axis min (units)
        self.x_max = 0.0            # x-axis max (units)
        self.y_min = 0.0            # y-axis min (units)
        self.y_max = 0.0            # y-axis max (units)
        self.x_scale = 0.0          # x-axis scaling factor (cm/units)
        self.y_scale = 0.0          # y-axis scaling factor (cm/units)
        self.W_box = 0.0            # width of plotting box (cm)
        self.H_box = 0.0            # height of plotting box (cm)
        self.L_text = 0.0           # height of text (cm)
        self.X_axes = 0.0           # x position of axis origin (cm)
        self.Y_axes = 0.0           # y position of axis origin (cm)
        self.L_margin = 0.0         # left tick label margin (cm)
        self.R_margin = 0.0         # right tick label margin (cm)
        self.B_margin = 0.0         # bottom tick label margin (cm)
        self.T_margin = 0.0         # top tick label margin (cm)
        self.L_x_tick = 0.0         # estimated left x-axis tick width
        self.R_x_tick = 0.0         # estimated right x-axis tick width
        self.H_x_tick = 0.0         # estimated x-axis tick height
        self.W_y_tick = 0.0         # estimated y-axis tick width
        self.H_y_tick = 0.0         # estimated y-axis tick height
        self.x_tick_fmt = ""        # format string of x-axis tick labels
        self.y_tick_fmt = ""        # format string of y-axis tick labels
        self.L_tick_shift = 0.0     # the axis tick label shift magnitude (cm)
        self.x_tick_shift = 0.0     # x-axis tick label vertical shift (cm)
        self.y_tick_shift = 0.0     # y-axis tick label horizontal shift (cm)
        self.legend_cols = 0        # number of legend columns
        self.legend_rows = 0        # number of legend rows
        self.H_legend_row = 0.0     # height of a legend row (cm)
        self.H_legend = 0.0         # height of the entire legend (cm)
        self.invisibles = False     # flag to show invisible boundaries


def append_to_fmt(fmt, opacity, width, pattern):
    """ Add opacity, line width, and line pattern to the format string `fmt`.
    Color is not included here because all colors will be predefined and then
    referenced by short name in the path commands. """
    if opacity is not None:
        opacity = max(0.0, min(opacity, 1.0))
        if opacity != 1:
            opacity_str = f"opacity={opacity:0.3g}"
            fmt = opacity_str if fmt is None else fmt + ", " + opacity_str
    if (width is not None) and (width != THIN):
        width = max(THINEST, min(width, THICKEST))
        width_str = f"line width={width:0.3g}pt"
        fmt = width_str if fmt is None else fmt + ", " + width_str
    if pattern is not None:
        pattern_list = ["solid", "dashdotted", "dashed",
                "densely dotted", "dotted", "loosely dotted"]
        pattern = max(0, min(pattern, len(pattern_list) - 1))
        pattern_str = pattern_list[pattern]
        if pattern_str != "solid":
            fmt = pattern_str if fmt is None else fmt + ", " + pattern_str
    return fmt


class Set:
    """ Settings for a curve in the graph. """
    def __init__(self, x, y, z=None, zony=False, color=None, marker=None,
            scaling=0, func=None, label=None, simp=True, fmt=None):
        self.x = x                  # x axis, or y when y is None
        self.y = y                  # y axis
        self.z = z                  # second y array or radius (radii)
        self.zony = zony            # flag to plot `z` on y axis
        self.rows = None            # max rows of `x` and `y`
        self.color = color          # scalar color integer (0xRRGGBB)
        self.marker = marker        # marker type (circle, dot)
        self.scaling = scaling      # scaling on the rendering of data
        self.func = func            # plot, scatter, fill
        self.label = label          # data set label string
        self.simp = simp            # flag to simplify path
        self.fmt = fmt              # additional format string


class graph:
    def __init__(self, filename='fig', width=None, height=None,
            xmin=None, xmax=None, ymin=None, ymax=None,
            xpad=False, ypad=True, xlog=False, ylog=False,
            equal=False, fontsize=9, xlabel=None, ylabel=None,
            xaxis=True, yaxis=True, xgrid=True, ygrid=True,
            xsubgrid=True, ysubgrid=True, xtick=True, ytick=True,
            ticksize=TICK_SIZE, xout=False, yout=False,
            rowmajor=False, columns=None, preamble=None,
            standalone=True):
        # Assign the settings. These are the user-facing options.
        self.filename = filename    # string of file without extension
        self.width = width          # width of pdf image in centimeters
        self.height = height        # height of pdf image in centimeters
        self.xmin = xmin            # x-axis minimum
        self.xmax = xmax            # x-axis maximum
        self.ymin = ymin            # y-axis minimum
        self.ymax = ymax            # y-axis maximum
        self.xpad = xpad            # use padding on x axis
        self.ypad = ypad            # use padding on y axis
        self.xlog = xlog            # flag to use log scaling on x axis
        self.ylog = ylog            # flag to use log scaling on y axis
        self.equal = equal          # flag to use equal scaling
        self.fontsize = fontsize    # font size in points
        self.xlabel = xlabel        # x-axis label
        self.ylabel = ylabel        # y-axis label
        self.xaxis = xaxis          # flag to show x axis
        self.yaxis = yaxis          # flag to show y axis
        self.xgrid = xgrid          # flag to show x grid
        self.ygrid = ygrid          # flag to show y grid
        self.xsubgrid = xsubgrid    # flag to show x sub-grid
        self.ysubgrid = ysubgrid    # flag to show y sub-grid
        self.xtick = xtick          # flag to show x ticks
        self.ytick = ytick          # flag to show y ticks
        self.ticksize = ticksize    # size of tick marks (cm)
        self.xout = xout            # flag to put x-axis ticks outside
        self.yout = yout            # flag to put y-axis ticks outside
        self.rowmajor = rowmajor    # flag to layout legend row major
        self.columns = columns      # number of legend columns
        self.preamble = preamble    # added string of LaTeX code in preamble
        self.standalone = standalone# flag to create standalone LaTeX file
        self.sets = []              # list of set objects

    def plot(self, x, y=None, color=None, opacity=1.0, width=THICK,
            pattern=None, label=None, simp=True, fmt=None):
        fmt = append_to_fmt(fmt, opacity, width, pattern)
        p = Set(x=x, y=y, color=color,
                func=plot_set, label=label, simp=simp, fmt=fmt)
        self.sets.append(p)
        return p

    def scatter(self, x, y=None, radius=0.03, color=None, opacity=1.0,
            marker=CIRCLES, label=None, fmt=None):
        # `radius` can be either a scalar or
        # an array compatible with `x` and `y`.
        fmt = append_to_fmt(fmt, opacity, None, None)
        radius = 0.01 if radius is None else radius
        p = Set(x=x, y=y, z=radius, color=color, marker=marker,
                func=scatter_set, label=label, simp=False, fmt=fmt)
        self.sets.append(p)
        return p

    def fill(self, x, y=None, z=None, color=None, opacity=1.0,
            label=None, simp=True, fmt=None):
        # If `y` and `z` are given, this becomes a fill-between.
        fmt = append_to_fmt(fmt, opacity, None, None)
        p = Set(x=x, y=y, z=z, zony=(z is not None), color=color,
                func=fill_set, label=label, simp=simp, fmt=fmt)
        self.sets.append(p)
        return p

    def hexbin(self, x, y=None, radius=0.2, color=None, opacity=1.0, scaling=0,
            label=None, fmt=None):
        # `radius` must be a scalar. A negative `radius` yields variable-size
        # hexagons. `scaling` adjusts the weighting curve to the hexagonal
        # shading (or sizing).
        fmt = append_to_fmt(fmt, opacity, None, None)
        p = Set(x=x, y=y, z=radius, color=color, scaling=scaling,
                func=hexbin_set, label=label, simp=False, fmt=fmt)
        self.sets.append(p)
        return p

    def render(self):
        # Skip all the plotting code if the flag is set.
        if config.skip:
            return

        # Ensure `x` and `y` are arrays with no more than 2 dimensions and
        # are compatibly shaped. If `z` is defined, ensure it is a scalar or
        # compatibly shaped with `x` and `y`.
        check_shapes(self.sets)

        # --------------------------------------------
        # Plan the figure dimensions and data scaling.
        # --------------------------------------------

        # Initialize the layout.
        lay = GraphLayout()

        # Get the viewing region. Find the mins and maxs,
        # ignoring nans and infs, and adjust for required padding.
        get_data_view(self, self.sets, lay)

        # Get the size of the box and margins.
        get_layout(self, self.sets, lay)

        # Get the scaling factors and conditionally apply equal scaling. Equal
        # scaling will alter the mins and maxs found in `get_data_view` and,
        # consequently, will alter the scaling factors. Getting adjusted mins
        # and maxs to satisfy equal scaling was also done by the `get_layout`
        # function, but that was necessary to make guesses about the available
        # drawing box size because of the potential impact of tick label
        # placement. Once the box size has been set, however, the mins and maxs
        # need to be recalculated if equal scaling is required.
        get_scaling(self, lay)

        # ------------------------------------------
        # Position the grids, axes, and tick labels.
        # ------------------------------------------

        # Get grid line locations (in linear scaling). This step was already
        # done once by the `get_layout` function, but that was only an
        # approximation in order to determine the required sizes for the margins
        # because of the placement of tick labels. Once the box size has been
        # set, the mins and maxs were recalculated (to satisfy possible equal
        # scaling) which requires that the grid placements be recalculated.
        if self.xlog:
            x_grids, x_sub_grids = grid_logarithmic(lay.x_min, lay.x_max)
        else:
            x_grids, x_sub_grids = grid_linear(lay.x_min, lay.x_max, lay.W_box,
                    max(lay.L_x_tick, lay.R_x_tick, lay.W_box/10))
        if self.ylog:
            y_grids, y_sub_grids = grid_logarithmic(lay.y_min, lay.y_max)
        else:
            y_grids, y_sub_grids = grid_linear(lay.y_min, lay.y_max, lay.H_box,
                    2*lay.font_size/PT_PER_CM)

        # Determine where the `x` and `y` axes would be in the drawing box. For
        # log scale or outside axes, the position in the box is left and bottom.
        # Otherwise, scale to centimeter units and bound within the box.
        if self.yout or self.xlog:
            lay.X_axes = 0.0 # bottom edge of drawing box
        else:
            lay.X_axes = to_scale(0, lay.x_min, lay.x_scale, self.xlog)
            lay.X_axes = max(0, min(lay.X_axes, lay.W_box))
        if self.xout or self.ylog:
            lay.Y_axes = 0.0 # left edge of drawing box
        else:
            lay.Y_axes = to_scale(0, lay.y_min, lay.y_scale, self.ylog)
            lay.Y_axes = max(0, min(lay.Y_axes, lay.H_box))

        # Determine what the tick format should be.
        if self.xout or lay.Y_axes > lay.L_text:
            lay.x_tick_fmt = "below"
            lay.x_tick_shift = -lay.L_tick_shift
        else:
            lay.x_tick_fmt = "above"
            lay.x_tick_shift = lay.L_tick_shift
        if self.yout or lay.X_axes > lay.W_box/2:
            lay.y_tick_fmt = "left"
            lay.y_tick_shift = -lay.L_tick_shift
        else:
            lay.y_tick_fmt = "right"
            lay.y_tick_shift = lay.L_tick_shift

        # -----------------------
        # Write the data to file.
        # -----------------------

        # Open the output file.
        filepath = "" if config.directory is None else config.directory + "/"
        filepath += self.filename + ".tex"
        fid = open(filepath, "w")

        # Open the standalone TikZ script.
        if self.standalone:
            write_open(fid, self.preamble)
        elif self.preamble is not None:
            print("Because this plot is not standalone, "
                    + "the additional preamble cannot be used.")

        # Define the font size.
        write_textstyle(fid, lay.font_size_name)

        # Define the colors.
        write_color_definitions(fid, self.sets)

        # Reserve the full figure space: the box and margins.
        write_reserve(fid, lay)

        # Draw the sub-grids and grids.
        if self.xsubgrid:
            grids = to_scale(x_sub_grids, lay.x_min, lay.x_scale, self.xlog)
            write_xgrid(fid, grids, lay.H_box, sub=True)
        if self.ysubgrid:
            grids = to_scale(y_sub_grids, lay.y_min, lay.y_scale, self.ylog)
            write_ygrid(fid, grids, lay.W_box, sub=True)
        if self.xgrid:
            grids = to_scale(x_grids, lay.x_min, lay.x_scale, self.xlog)
            write_xgrid(fid, grids, lay.H_box)
        if self.ygrid:
            grids = to_scale(y_grids, lay.y_min, lay.y_scale, self.ylog)
            write_ygrid(fid, grids, lay.W_box)

        # Begin a scope.
        write_scope_begin(fid)

        # Clip everything with this scope to the drawing box.
        write_clip(fid, lay.W_box, lay.H_box)

        # Set line style to rounded.
        write_rounded(fid)

        # Draw the sets.
        for j in range(len(self.sets)):
            # Introduce this data set.
            write_comment(fid, f"Set {j}")
            self.sets[j].func(fid, self.sets[j], lay.x_min, lay.y_min,
                    lay.x_scale, lay.y_scale, self.xlog, self.ylog,
                    lay.W_box, lay.H_box)

        # End the scope.
        write_scope_end(fid)

        # Draw the axes.
        write_comment(fid, "Draw axes.")
        if self.xaxis:
            write_line(fid, -self.ticksize/2, lay.Y_axes,
                    lay.W_box + self.ticksize, lay.Y_axes, "->")
        if self.yaxis:
            write_line(fid, lay.X_axes, -self.ticksize/2,
                    lay.X_axes, lay.H_box + self.ticksize, "->")

        # Write the x-axis ticks and labels.
        if self.xtick and self.xaxis: # Ticks without an axis look weird.
            # Comment.
            write_comment(fid, "Draw x-axis ticks and labels.")

            # Scale the grid lines to paper dimensions.
            X = to_scale(x_grids, lay.x_min, lay.x_scale, self.xlog)

            # Determine the form for the tick labels and their precision.
            format_func, precision = get_num_format(self.xlog, x_grids)

            # Get the tick label strings and their widths.
            tick_labels = []
            tick_widths = []
            tick_skip = [False for n in range(len(X))]
            for n in range(len(X)):
                txt, w_txt = format_func(x_grids[n], precision, lay.font_size)
                tick_labels.append(txt)
                tick_widths.append(w_txt/PT_PER_CM)
                if not self.xout:
                    dist_to_axis = math.fabs(X[n] - lay.X_axes)
                    if self.yaxis and dist_to_axis < tick_widths[n]/2:
                        tick_skip[n] = True
                    dist_to_edge = min(math.fabs(X[n]),
                            math.fabs(lay.W_box - X[n]))
                    if dist_to_edge < tick_widths[n]/2:
                        tick_skip[n] = True

            # Write the tick marks.
            for n in range(len(X)):
                if tick_skip[n]:
                    continue
                write_line(fid, X[n], lay.Y_axes - self.ticksize/2,
                        X[n], lay.Y_axes + self.ticksize/2)

            # Write the tick labels.
            if not self.xout:
                write_scope_begin(fid, "opacity=0.8")
                write_outline_style(fid)
                for n in range(len(X)):
                    if tick_skip[n]:
                        continue
                    write_text(fid, X[n], lay.Y_axes + lay.x_tick_shift,
                            "$" + tick_labels[n] + "$\\strut", lay.x_tick_fmt)
                write_scope_end(fid)
            for n in range(len(X)):
                if tick_skip[n]:
                    continue
                write_text(fid, X[n], lay.Y_axes + lay.x_tick_shift,
                        "$" + tick_labels[n] + "$\\strut", lay.x_tick_fmt)

        # Write the y-axis ticks and labels.
        if self.ytick and self.yaxis: # Ticks without an axis look weird.
            # Comment.
            write_comment(fid, "Draw y-axis ticks and labels.")

            # Scale the grid lines to paper dimensions.
            Y = to_scale(y_grids, lay.y_min, lay.y_scale, self.ylog)

            # Determine the form for the tick labels and their precision.
            format_func, precision = get_num_format(self.ylog, y_grids)

            # Get the tick label strings and their widths.
            tick_labels = []
            tick_skip = [False for n in range(len(Y))]
            tol_to_axis = lay.font_size/(2*PT_PER_CM)
            for n in range(len(Y)):
                txt, _ = format_func(y_grids[n], precision, lay.font_size)
                tick_labels.append(txt)
                if not self.yout:
                    dist_to_axis = math.fabs(Y[n] - lay.Y_axes)
                    if self.xaxis and dist_to_axis < tol_to_axis:
                        tick_skip[n] = True
                    dist_to_edge = min(math.fabs(Y[n]),
                            math.fabs(lay.H_box - Y[n]))
                    if dist_to_edge < tol_to_axis:
                        tick_skip[n] = True

            # Write the tick marks.
            for n in range(len(Y)):
                if tick_skip[n]:
                    continue
                write_line(fid, lay.X_axes - self.ticksize/2, Y[n],
                        lay.X_axes + self.ticksize/2, Y[n])

            # Write the tick labels.
            if not self.yout:
                write_scope_begin(fid, "opacity=0.8")
                write_outline_style(fid)
                for n in range(len(Y)):
                    if tick_skip[n]:
                        continue
                    write_text(fid, lay.X_axes + lay.y_tick_shift, Y[n],
                            "$" + tick_labels[n] + "$\\strut", lay.y_tick_fmt)
                write_scope_end(fid)
            for n in range(len(Y)):
                if tick_skip[n]:
                    continue
                write_text(fid, lay.X_axes + lay.y_tick_shift, Y[n],
                        "$" + tick_labels[n] + "$\\strut", lay.y_tick_fmt)

        # Write the axis labels (inside the figure space).
        if self.xlabel is not None:
            write_comment(fid, "Write x-axis label.")
            write_text(fid, lay.W_box/2, -lay.B_margin,
                    self.xlabel + "\\strut", "above")
        if self.ylabel is not None:
            write_comment(fid, "Write y-axis label.")
            write_text(fid, -lay.L_margin, lay.H_box/2,
                    self.ylabel + "\\strut", "below, rotate=90")

        # Write the legend labels.
        if lay.legend_cols > 0:
            # Comment.
            write_comment(fid, "Write legend.")

            row = 0
            col = 0
            for j in range(len(self.sets)):
                # Skip unlabled sets.
                label = self.sets[j].label
                if label is None:
                    continue

                # Draw the legend line.
                x = col*(lay.W_box/lay.legend_cols)
                y = -lay.B_margin - lay.H_legend \
                        + (lay.H_legend_row)*(lay.legend_rows - 0.5 - row)
                write_line(fid, x, y, x + lay.width*LEGEND_RATIO, y,
                        fmt=f"line width=3pt, C{j}")
                write_text(fid, x + lay.width*LEGEND_RATIO
                        + TICK_SIZE, y, label + "\\strut", fmt="right")

                # Increment the column number.
                if self.rowmajor:
                    row += 1
                    if row >= lay.legend_rows:
                        col += 1
                        row = 0
                else:
                    col += 1
                    if col >= lay.legend_cols:
                        row += 1
                        col = 0

        # Close the standalone TikZ script.
        if self.standalone:
            write_close(fid)

        # Close the output file.
        fid.close()

        # -----------------
        # Compile the file.
        # -----------------

        # Compile the LaTeX file.
        if self.standalone:
            cmd = 'pdflatex'
            if config.silent:
                cmd = cmd + ' --interaction=batchmode'
            if config.directory is None:
                os.system(f'{cmd} {self.filename}.tex')
                os.system(f'rm {self.filename}.aux')
                os.system(f'rm {self.filename}.log')
            else:
                pwd = os.getcwd()
                cmd = f'{cmd} -output-directory="{pwd}/{config.directory}"'
                os.system(f'{cmd} "{config.directory}/{self.filename}.tex"')
                os.system(f'rm {config.directory}/{self.filename}.aux')
                os.system(f'rm {config.directory}/{self.filename}.log')

# ---------------------
# Calculation Functions
# ---------------------

def check_shapes(sets):
    # Cycle through each data set.
    for j in range(len(sets)):
        # Parse the x and y fields.
        x = sets[j].x
        y = sets[j].y
        z = sets[j].z

        # Convert scalars, lists, and tuples to arrays.
        # None values will be unaffected.
        if isinstance(x, (int, float)):
            x = np.asarray([x], dtype=float)
        elif isinstance(x, (list, tuple)):
            x = np.asarray(x, dtype=float)
        if isinstance(y, (int, float)):
            y = np.asarray([y], dtype=float)
        elif isinstance(y, (list, tuple)):
            y = np.asarray(y, dtype=float)
        if isinstance(z, int):
            z = float(z) # Do not convert scalar z to array.
        elif isinstance(z, (list, tuple)):
            z = np.asarray(z, dtype=float)

        # Ensure some data was defined.
        if (x is None) and (y is None) and (z is None):
            raise ValueError(f"No data was defined for data set {j}.")

        # Handle undefined arrays.
        if y is None:
            if (z is not None) and sets[j].zony:
                y = z
                z = None
            elif x is not None:
                y = x
                x = None
        if x is None:
            x = np.arange(y.shape[-1], dtype=float)

        # Check for too many dimensions. At this point,
        # `x` and `y` are guaranteed to be arrays.
        if x.ndim > 2:
            raise ValueError(f"x in set {j} has too many dimensions.")
        if y.ndim > 2:
            raise ValueError(f"y in set {j} has too many dimensions.")
        if (z is not None) and (np.ndim(z) > 2):
            raise ValueError(f"z in set {j} has too many dimensions.")

        # Check for incompatible dimensions.
        xrows, xcols = (1, len(x)) if x.ndim == 1 else x.shape
        yrows, ycols = (1, len(y)) if y.ndim == 1 else y.shape
        if (xcols != ycols) or \
                ((xrows > 1) and (yrows > 1) and (xrows != yrows)):
            raise ValueError(f"x ({xrows},{xcols}) "
                    + f"and y ({yrows},{ycols}) in set {j} "
                    + "are incompatible")
        rows = max(xrows, yrows)
        if (z is not None) and (np.ndim(z) > 0):
            zrows, zcols = (1, len(z)) if z.ndim == 1 else z.shape
            if ((zcols > 1) and (zcols != xcols)) or \
                    ((zrows > 1) and (rows > 1) and (zrows != rows)):
                raise ValueError(f"x ({xrows},{xcols}) "
                        + f"and y ({yrows},{ycols}) "
                        + f"and z ({zrows},{zcols}) in set {j} "
                        + "are incompatible")
            rows = max(rows, zrows)

        # Save to the data set.
        sets[j].x = x
        sets[j].y = y
        sets[j].z = z
        sets[j].rows = rows


def get_data_view(fig, sets, lay):
    # Define constants.
    tol = 1e-45 # position tolerance
    pad_ratio = 0.1 # padding ratio of figure width

    # Initialize the minimums and maximums.
    lay.x_min = math.inf
    lay.x_max = -math.inf
    lay.y_min = math.inf
    lay.y_max = -math.inf

    # Check the range of each set.
    for j in range(len(sets)):
        # Parse the x and y fields.
        x = sets[j].x
        y = sets[j].y
        z = sets[j].z
        zony = sets[j].zony

        # Get the maximum number of rows.
        rows = max(1, x.shape[0]*(x.ndim > 1), y.shape[0]*(y.ndim > 1))
        if zony:
            rows = max(rows, z.shape[0]*(z.ndim > 1))

        # For each row in the data set,
        for row in range(rows):
            # Get the data for this row.
            xr = x if x.ndim == 1 else x[row]
            yr = y if y.ndim == 1 else y[row]
            if zony:
                zr = z if z.ndim == 1 else z[row]

            # Find the valid points (not nan, inf, or negative (for log)).
            nn = np.arange(len(xr))
            xr_fin = np.isfinite(xr)
            yr_fin = np.isfinite(yr)
            nx_valid = nn[xr_fin & (xr > 0)] if fig.xlog else nn[xr_fin]
            ny_valid = nn[yr_fin & (yr > 0)] if fig.ylog else nn[yr_fin]
            nn_valid = np.intersect1d(nx_valid, ny_valid)
            if zony:
                zr_fin = np.isfinite(zr)
                nz_valid = nn[zr_fin & (zr > 0)] if fig.ylog else nn[zr_fin]
                nn_valid = np.intersect1d(nn_valid, nz_valid)

            # Enlarge x extrema.
            x_min = xr[nn_valid].min()
            x_max = xr[nn_valid].max()
            if x_min < lay.x_min:
                lay.x_min = x_min
            if x_max > lay.x_max:
                lay.x_max = x_max

            # Enlarge y extrema.
            y_min = yr[nn_valid].min()
            y_max = yr[nn_valid].max()
            if y_min < lay.y_min:
                lay.y_min = y_min
            if y_max > lay.y_max:
                lay.y_max = y_max

            # Enlarge y extrema with z.
            if zony:
                z_min = zr[nn_valid].min()
                z_max = zr[nn_valid].max()
                if z_min < lay.y_min:
                    lay.y_min = z_min
                if z_max > lay.y_max:
                    lay.y_max = z_max

    # Add x-axis padding if requested or needed.
    tol = 1e-45
    if fig.xlog: # temporarily log scale
        lay.x_min = math.log10(lay.x_min)
        lay.x_max = math.log10(lay.x_max)
        tol = 1.0
    w = lay.x_max - lay.x_min
    lay.x_min -= (w == 0)*tol + (fig.xpad)*w*pad_ratio/2
    lay.x_max += (w == 0)*tol + (fig.xpad)*w*pad_ratio/2
    if fig.xlog: # back to linear scale
        lay.x_min = 10.0**lay.x_min
        lay.x_max = 10.0**lay.x_max

    # Add y-axis padding if requested or needed.
    tol = 1e-45
    if fig.ylog: # temporarily log scale
        lay.y_min = math.log10(lay.y_min)
        lay.y_max = math.log10(lay.y_max)
        tol = 1.0
    h = lay.y_max - lay.y_min
    lay.y_min -= (h == 0)*tol + (fig.ypad)*h*pad_ratio/2
    lay.y_max += (h == 0)*tol + (fig.ypad)*h*pad_ratio/2
    if fig.ylog: # back to linear scale
        lay.y_min = 10.0**lay.y_min
        lay.y_max = 10.0**lay.y_max

    # Override for requested limits.
    if fig.xmin is not None:
        lay.x_min = fig.xmin
    if fig.xmax is not None:
        lay.x_max = fig.xmax
    if fig.ymin is not None:
        lay.y_min = fig.ymin
    if fig.ymax is not None:
        lay.y_max = fig.ymax

    # Ensure there is a range to plot.
    if lay.x_max <= lay.x_min or lay.y_max <= lay.y_min:
        raise ValueError("Invalid range of values! "
                + f"x: ({lay.x_min},{lay.x_max}), "
                + f"y: ({lay.y_min}, {lay.y_max})")


def get_base_exp(x):
    if x == 0:
        base_exp = 0
    else:
        base_exp = int(math.floor(math.log10(math.fabs(x)) + 1e-3))
    return base_exp


def get_num_format(is_log, grids):
    # Determine the form for the tick labels and their precision.
    if is_log:
        precision = 0
        format_func = lstr
    else:
        # The decision to use scientific notation (3.14x10^1) versus
        # floating-point notation (31.4) depends on the extrema grid
        # values being larger than 999 or smaller than 0.01. The
        # 'precision' is of the whole number, not just the mantissa,
        # and depends on the grid step size.
        e_min = get_base_exp(grids[0])
        e_max = get_base_exp(grids[-1])
        precision = -get_base_exp(grids[1] - grids[0])
        if math.fabs(e_min) > 3 or math.fabs(e_max) > 3:
            format_func = gstr
        else:
            if precision < 0: # integer step size
                format_func = dstr
            else: # decimal values required for step size
                format_func = fstr
    return format_func, precision


def get_layout(fig, sets, lay):
    # Define the default width-to-height ratio.
    ratio = 1.61803398875 # golden ratio

    # Set the figure dimensions.
    lay.width = fig.width
    lay.height = fig.height
    if lay.width is None and lay.height is None:
        lay.width = WIDTH
        lay.height = WIDTH/ratio
    elif lay.width is None:
        lay.width = lay.height*ratio
    elif lay.height is None:
        lay.height = lay.width/ratio

    # Force fontsize to be a standard value.
    font_sizes = np.array([5, 7, 8, 9, 10, 12, 14.4, 17.28, 20.74, 24.88])
    font_size_names = ["tiny", "scriptsize", "footnotesize", "small",
            "normalsize", "large", "Large", "LARGE", "huge", "Huge"]
    n = (np.abs(font_sizes - fig.fontsize)).argmin() # best-fit index
    if math.fabs(fig.fontsize - font_sizes[n]) > 0.01:
        print("The requested font size is adjusted to a standard value: "
                + f"{font_size[n]} pt.")
    lay.font_size = font_sizes[n]
    lay.font_size_name = font_size_names[n]

    # Define text-based lengths.
    lay.L_text = 1.3*lay.font_size/PT_PER_CM # (cm)

    # Get the tick shift.
    lay.L_tick_shift = fig.ticksize*0.75

    # Get impact of axis labels on the margins.
    H_x_label = lay.L_text*(fig.xlabel is not None) + fig.ticksize*0.25
    W_y_label = lay.L_text*(fig.ylabel is not None) + fig.ticksize*0.25

    # -----------------------------
    # Get dimensions of the legend.
    # -----------------------------

    # Count the number of labeled sets and the required number of rows and
    # columns for the legend, and define the height of a legend row.
    labeled = 0
    legend_buff = 0
    lay.legend_cols = 0
    lay.legend_rows = 0
    for j in range(len(sets)):
        if sets[j].label is not None:
            labeled += 1
    if labeled > 0:
        if fig.columns is None:
            lay.legend_cols = round(lay.width/2.0)
            if lay.legend_cols + 1 >= labeled:
                lay.legend_cols = labeled
        else:
            lay.legend_cols = fig.columns
        lay.legend_rows = int(math.ceil(labeled/lay.legend_cols))
        if fig.xlabel:
            legend_buff = 0.25*lay.L_text
    lay.H_legend_row = 1.5*lay.L_text

    # Get the height of the legend.
    lay.H_legend = legend_buff + lay.legend_rows*lay.H_legend_row

    # --------------------------
    # Estimate the grid numbers.
    # --------------------------

    # Copy the layout limits and size.
    x_min = lay.x_min
    x_max = lay.x_max
    y_min = lay.y_min
    y_max = lay.y_max

    # Get the tick-label dimensions, assuming the worst-case label widths.
    # This width is based on a number of the form "-m.mm x 10^(-eee)".
    if fig.xtick and fig.xaxis and fig.xout: # Ticks without an axis are weird.
        if fig.xlog:
            W_x_tick = 2.5*lay.font_size/PT_PER_CM
        else:
            W_x_tick = 6.0*lay.font_size/PT_PER_CM
    else:
        W_x_tick = 0.0
    if fig.ytick and fig.yaxis and fig.yout: # Ticks without an axis are weird.
        if fig.ylog:
            W_y_tick = 2.5*lay.font_size/PT_PER_CM
        else:
            W_y_tick = 6.0*lay.font_size/PT_PER_CM
    else:
        W_y_tick = 0.0
    H_y_tick = lay.L_text if fig.ytick and fig.yaxis else 0.0
    H_x_tick = lay.L_text + lay.L_tick_shift if fig.xout else 0.0

    # Get the dimensions of the margins around the box.
    L_margin = max(W_y_label + W_y_tick + fig.ticksize/2, W_x_tick/2)
    R_margin = max(fig.ticksize, W_x_tick/2)
    B_margin = max(H_x_label + H_x_tick + fig.ticksize/2, H_y_tick/2)
    T_margin = max(fig.ticksize, H_y_tick/2)

    # Initialize the box size.
    W_box = lay.width - L_margin - R_margin
    H_box = lay.height - B_margin - T_margin - lay.H_legend

    # Adjust the limits for equal axis scaling. For equal axis scaling to affect
    # anything, xlog must equal ylog. This operation will be repeated by the
    # `get_scaling` function once the drawing box size has been determined.
    if fig.equal and fig.xlog == fig.ylog:
        # Temporarily convert to logarithmic scaling.
        if fig.xlog and fig.ylog:
            x_min = math.log10(x_min)
            x_max = math.log10(x_max)
            y_min = math.log10(y_min)
            y_max = math.log10(y_max)

        # Get the data scaling factors. This is needed later regardless of
        # whether equal-axis scaling is required.
        x_scale = W_box/(x_max - x_min)
        y_scale = H_box/(y_max - y_min)

        # Increase the span of the axis with a larger scale (zoom out).
        if x_scale < y_scale:
            y_span = H_box/x_scale
            y_mid = (y_max + y_min)*0.5
            y_min = y_mid - y_span*0.5
            y_max = y_mid + y_span*0.5
        elif y_scale < x_scale:
            x_span = W_box/y_scale
            x_mid = (x_max + x_min)*0.5
            x_min = x_mid - x_span*0.5
            x_max = x_mid + x_span*0.5

        # Convert back to linear scaling.
        if fig.xlog and fig.ylog:
            x_min = 10.0**x_min
            x_max = 10.0**x_max
            y_min = 10.0**y_min
            y_max = 10.0**y_max

    # Get the estimated grid values so we can estimate the tick label widths.
    if fig.xlog:
        x_grids, _ = grid_logarithmic(x_min, x_max)
    else:
        x_grids, _ = grid_linear(x_min, x_max, W_box,
                5*lay.font_size/PT_PER_CM)
    if fig.ylog:
        y_grids, _ = grid_logarithmic(y_min, y_max)
    else:
        y_grids, _ = grid_linear(y_min, y_max, H_box,
                2*lay.font_size/PT_PER_CM)

    # --------------------------------------
    # Get the dimensions of the tick labels.
    # --------------------------------------

    # Get x-axis, tick-label margins.
    lay.L_x_tick = 0.0
    lay.R_x_tick = 0.0
    lay.H_x_tick = 0.0
    if fig.xtick and fig.xaxis: # Ticks without an axis look weird.
        # Height of tick label.
        lay.H_x_tick = lay.L_text + fig.ticksize*0.25

        # Determine the form for the tick labels and their precision.
        format_func, precision = get_num_format(fig.xlog, x_grids)

        # Get the left and right tick label widths in points.
        _, w_left = format_func(x_grids[0], precision, lay.font_size)
        _, w_right = format_func(x_grids[-1], precision, lay.font_size)
        lay.L_x_tick = w_left/PT_PER_CM + fig.ticksize
        lay.R_x_tick = w_right/PT_PER_CM + fig.ticksize

    # Get y-axis, tick-label margins.
    lay.W_y_tick = 0.0
    lay.H_y_tick = 0.0
    if fig.ytick and fig.yaxis: # Ticks without an axis look weird.
        # Determine the form for the tick labels and their precision.
        format_func, precision = get_num_format(fig.ylog, y_grids)

        # Get the left and right tick label widths in points.
        _, w_bot = format_func(y_grids[0], precision, lay.font_size)
        _, w_top = format_func(y_grids[-1], precision, lay.font_size)
        lay.W_y_tick = max(w_bot, w_top)/PT_PER_CM + fig.ticksize

        # Top and bottom of tick labels
        lay.H_y_tick = lay.L_text

    # --------------------------------------------------------
    # Get the margins, size of the box, and positions of text.
    # --------------------------------------------------------

    # Get the dimensions of the margins around the box.
    lay.L_margin = max(W_y_label + lay.W_y_tick*fig.yout + fig.ticksize/2,
            lay.L_x_tick/2*fig.xout)
    lay.R_margin = max(fig.ticksize, lay.R_x_tick/2*fig.xout)
    lay.B_margin = max(H_x_label + lay.H_x_tick*fig.xout + fig.ticksize/2,
            lay.H_y_tick/2*fig.yout)
    lay.T_margin = max(fig.ticksize, lay.H_y_tick/2*fig.yout)

    # Get the height of the legend.
    lay.H_legend = legend_buff + lay.legend_rows*lay.H_legend_row

    # Initialize the box size.
    lay.W_box = lay.width - lay.L_margin - lay.R_margin
    lay.H_box = lay.height - lay.B_margin - lay.T_margin - lay.H_legend


def get_scaling(fig, lay):
    # Temporarily convert to logarithmic scaling.
    if fig.xlog:
        lay.x_min = math.log10(lay.x_min)
        lay.x_max = math.log10(lay.x_max)
    if fig.ylog:
        lay.y_min = math.log10(lay.y_min)
        lay.y_max = math.log10(lay.y_max)

    # Get the data scaling factors. This is needed later regardless of
    # whether equal-axis scaling is required.
    lay.x_scale = lay.W_box/(lay.x_max - lay.x_min)
    lay.y_scale = lay.H_box/(lay.y_max - lay.y_min)

    # Increase the span of the axis with a larger scale (zoom out).
    if fig.equal:
        if fig.xlog == fig.ylog:
            if lay.x_scale < lay.y_scale:
                lay.y_scale = lay.x_scale
                y_span = lay.H_box/lay.y_scale
                y_mid = (lay.y_max + lay.y_min)*0.5
                lay.y_min = y_mid - y_span*0.5
                lay.y_max = y_mid + y_span*0.5
            elif lay.y_scale < lay.x_scale:
                lay.x_scale = lay.y_scale
                x_span = lay.W_box/lay.x_scale
                x_mid = (lay.x_max + lay.x_min)*0.5
                lay.x_min = x_mid - x_span*0.5
                lay.x_max = x_mid + x_span*0.5
        else:
            print("Semi-log scaling does not make sense with equal axes. "
                    + "The equal-axis setting will be ignored.")

    # Convert back to linear scaling.
    if fig.xlog:
        lay.x_min = 10.0**lay.x_min
        lay.x_max = 10.0**lay.x_max
    if fig.ylog:
        lay.y_min = 10.0**lay.y_min
        lay.y_max = 10.0**lay.y_max

def dstr(x, p=0, f=10):
    """
    Given a floating-point number `x`, the precision `p`, and  the font size `f`
    in points, return a LaTeX string `s` of the number as an integer and the
    estimated width `w` in points. 'p' is unused.
    """
    x = int(round(x))
    s = "%d" % x
    if x >= 0:
        w = (len(s)*R_DIGIT)*f
    else:
        w = (R_SIGN + (len(s) - 1)*R_DIGIT)*f
    return s, w


def fstr(x, p=4, f=10):
    """
    Given a floating-point number `x`, the precision `p`, and  the font size `f`
    in points, return a LaTeX string `s` of the number as a floating-point value
    and the estimated width `w` in points.
    """
    s = "%.*f" % (p, x)
    if x > 0:
        w = (R_DECIMAL + (len(s) - 1)*R_DIGIT)*f
    else:
        w = (R_SIGN + R_DECIMAL + (len(s) - 2)*R_DIGIT)*f
    return s, w


def gstr(x, p=6, f=10):
    """
    Given a floating-point number `x`, the precision `p`, and  the font size `f`
    in points, return a LaTeX string `s` of the number in the format `m x 10^e`
    and the estimated width `w` in points. 'p' is the precision of the whole
    number, not of the mantissa alone.
    """

    # Simplify for zero.
    if x == 0:
        return "0", (R_DIGIT*f)

    # Get the base exponent.
    e = get_base_exp(x)

    # Get the mantissa string and width.
    mt = x*10.0**(-e) # mantissa value
    if p > -e: # More precision than the units place is required.
        sm, wm = fstr(mt, p + e, f)
    else: # An integer will satisfy the precision requirement.
        sm, wm = dstr(mt, 0, f)

    # Get the times string and width.
    st = "\\!\\times\\!10^{{"
    wt = (R_TIMES + 2*R_DIGIT)*f

    # Get the exponent string and width.
    se = "%d" % (e)
    if e > 0:
        we = (R_POWER*(len(se)*R_DIGIT))*f
    else:
        we = (R_POWER*(R_SIGN + (len(se) - 1)*R_DIGIT))*f

    # Assemble the full string and width.
    s = sm + st + se + "}}"
    w = wm + wt + we

    return s, w


def lstr(x, p=6, f=10):
    """
    Given a floating-point number `x`, the precision `p`, and  the font size `f`
    in points, return a LaTeX string `s` of the number and the estimated width
    `w` in points. `p` is unused.
    """
    e = get_base_exp(x)
    se = "%d" % (e)
    s = "10^{{" + se + "}}"
    if e > 0:
        we = (len(se)*R_DIGIT)*f
    else:
        we = (R_SIGN + (len(se) - 1)*R_DIGIT)*f
    w = (2*R_DIGIT)*f + R_POWER*(we)
    return s, w


def grid_linear(u_min, u_max, L_box, L_tick):
    # Get the normalized span. Every span will map to [1,10).
    u_span = u_max - u_min # guaranteed to be positive
    base = 10.0**get_base_exp(u_span)
    u_span_normalized = u_span/base # [1, 10)

    # Choose a nice step and sub-step based on the normalized span.
    u_cnt_preferred = math.floor(L_box/L_tick)
    step_sizes =  np.array([5.0, 2.0, 1.0, 0.5, 0.2,  0.1,  0.05, 0.02])
    sub_step_sizes = np.array([1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01, 0.005])
    grid_cnts = np.round(u_span_normalized/step_sizes)
    n_min = np.argmax(grid_cnts >= 3) # first count to satisfy
    n_pref = np.argmax(grid_cnts > u_cnt_preferred) - 1
    n = max(n_pref, n_min)
    step_size = step_sizes[n]*base
    sub_step_size = sub_step_sizes[n]*base

    # Get the nice extrema. The major grid lines may go to the very edge.
    # The minor grid lines may not.
    grid_min = u_min if math.fmod(u_min, step_size) == 0 else \
            (math.floor(u_min/step_size) + 1)*step_size
    grid_max = u_max if math.fmod(u_max, step_size) == 0 else \
            (math.ceil(u_max/step_size) - 1)*step_size
    sub_grid_min = (math.floor(u_min/sub_step_size) + 1)*sub_step_size
    sub_grid_max =  (math.ceil(u_max/sub_step_size) - 1)*sub_step_size

    # Build the grids arrays.
    N_grids = round((grid_max - grid_min)/step_size) + 1
    N_sub_grids = round((sub_grid_max - sub_grid_min)/sub_step_size) + 1
    grids = np.linspace(grid_min, grid_max, N_grids)
    sub_grids = np.linspace(sub_grid_min, sub_grid_max, N_sub_grids)

    # Remove the major grid lines from the minor set.
    sub_grids = np.array([u for u in sub_grids if u not in grids])

    return grids, sub_grids


def grid_logarithmic(u_min, u_max):
    # Convert to log scale.
    e_min = math.log10(u_min)
    e_max = math.log10(u_max)

    # Build the grids array.
    e_min_base = int(math.floor(e_min))
    e_max_base = int(math.floor(e_max))
    if e_min_base == e_min:
        e_grids = np.arange(e_min_base, e_max_base + 1)
    else:
        e_grids = np.arange(e_min_base + 1, e_max_base + 1)
    grids = 10.0**e_grids

    # Get the normalized limits of the sub-grids.
    u_min_mod = math.ceil(10.0**math.fmod(e_min, 1)) # [1, 10]
    if u_min_mod == 1:
        u_min_mod = 2
    u_max_mod = math.floor(10.0**math.fmod(e_max, 1)) # [0, 9]

    # Build the first, middle, and end parts of the sub_grids.
    e_sub_grids = np.log10(np.arange(u_min_mod, 10)) + e_min_base
    for e_base in range(e_min_base + 1, e_max_base):
        e_set = np.log10(np.arange(2, 10)) + e_base
        e_sub_grids = np.append(e_sub_grids, e_set)
    if u_max_mod > 1:
        e_set = np.log10(np.arange(2, u_max_mod + 1)) + e_max_base
        e_sub_grids = np.append(e_sub_grids, e_set)
    sub_grids = 10.0**e_sub_grids

    return grids, sub_grids


def to_scale(u, u_min, u_scale, u_log):
    if u_log:
        U = np.log10(u/u_min)*u_scale
    else:
        U = (u - u_min)*u_scale
    return U


def simp_chunks(u, v, chunks):
    """
    Simplify the u and v data path by uniform index chunking along the u axis.
    """

    # Get the number of points.
    K = len(u)

    # Get the number of chunks.
    if K <= chunks:
        return u, v

    # Get the array of chunking indices: [0, K].
    kk = np.round(np.arange(chunks + 1)/chunks*K).astype(int)

    # Allocate memory for the new set of indices.
    nn = np.zeros(2*chunks, dtype=int)

    # For each chunk, store the min and max.
    for n_chunk in range(chunks):
        na = kk[n_chunk]
        nb = kk[n_chunk + 1]
        n_min = np.argmin(v[na:nb]) + na
        n_max = np.argmax(v[na:nb]) + na
        if n_min < n_max:
            nn[2*n_chunk] = n_min
            nn[2*n_chunk + 1] = n_max
        else:
            nn[2*n_chunk] = n_max
            nn[2*n_chunk + 1] = n_min

    return nn


def simp_map(u, v, tol):
    """
    Simplify the u and v data path by replacement with a line that breaks when
    points are too far from the line. This algorithm works by setting a range of
    angles of tangent lines to a circle about the last pinned point. All future
    points must be between those tangent lines. This algorithm achieves a
    similar result to the Ramer-Douglas-Peucker algorithm, but with far fewer
    calculations.

    Parameters
    ----------
    u : (N,) float np.ndarray
        x-axis array of points.
    v : (N,) float np.ndarray
        y-axis array of points.
    tol : float
        Maximum allowable distance of points from fitting lines.

    Returns
    -------
    nn : (M,) int np.ndarray
        Array of indices to keep from original (u, v) path. (u[nn], v[nn])
        defines the simplified path.

    Notes
    -----
    A single tolerance assumes equal units and scaling between `u` and `v`. If
    this is not the case, simply prescale the `u` or `v` values according to
    preference.

    This algorithm was developed by David Woodburn.
    """

    # Get the circle radius.
    h = tol/2

    # Initialize the pin index and array.
    N = len(u)
    n_pin = 0
    nn = np.zeros(N, dtype=np.int32)
    nn[0] = 0
    m = 1 # index into nn

    # Clear the bounding angles, A and B. A is also used as a state. It is None
    # when we are searching for a new point outside the radius of the last
    # pinned point.
    A = None # lower angle
    B = None # upper angle

    # Clear the maximum distance down the tube.
    d_max = 0.0
    n_max = 0

    # For each point,
    n = 1
    while (n < N):
        # Get the displacement from the pin.
        du = u[n] - u[n_pin]
        dv = v[n] - v[n_pin]
        d = math.sqrt(du**2 + dv**2)

        # Skip all points within radius h of p.
        if d <= h:
            n += 1
            continue

        # Initialize angles.
        if A is None:
            C = math.atan2(dv, du)
            dC = math.pi - math.acos(h/d)
            A = (C - dC + math.pi) % math.tau - math.pi
            B = (C + dC + math.pi) % math.tau - math.pi
            d_max = d
            n_max = n
            n += 1
            continue

        # Get the circle-edge points.
        uA = h*math.cos(A) + u[n_pin]
        vA = h*math.sin(A) + v[n_pin]
        uB = h*math.cos(B) + u[n_pin]
        vB = h*math.sin(B) + v[n_pin]

        # Get the angles relative to the circle-edge points.
        CA = math.atan2(v[n] - vA, u[n] - uA)
        CB = math.atan2(v[n] - vB, u[n] - uB)

        # Get the angle margins to the edge lines.
        dA = (CA - (A + math.pi/2) + math.pi) % math.tau - math.pi
        dB = ((B - math.pi/2) - CB + math.pi) % math.tau - math.pi

        # Check if this point is out of bounds.
        if dA < 0 or dB < 0:
            # Pin previous point.
            n_pin = n_max
            nn[m] = n_pin
            m += 1
            # Clear the bounding angles.
            A = None
            B = None
            d_max = 0.0
            continue # without incrementing n

        # Remember this point if it is furthest down the tube.
        if d > d_max:
            d_max = d
            n_max = n

        # Get new potential a and b bounding angles.
        C = math.atan2(dv, du)
        dC = math.pi - math.acos(h/d)
        a = (C - dC + math.pi) % math.tau - math.pi
        b = (C + dC + math.pi) % math.tau - math.pi

        # Get the margins between the old and new bounding angles.
        dA = (a - A + math.pi) % math.tau - math.pi
        dB = (B - b + math.pi) % math.tau - math.pi

        # Check if the new bounds are more restrictive.
        if dA > 0: # a more so than A
            A = a
        if dB > 0: # b more so than B
            B = b
        n += 1

    # Add end point to list and crop.
    if m >= N:
        m = N - 1
    nn[m] = N - 1
    nn = nn[:m + 1]

    # Return just the pinned points.
    return nn


def simp_best(X, Y, W_box, H_box):
    tol = THINEST/PT_PER_CM
    nn = simp_map(X, Y, tol)
    x_chunks = round(W_box/(tol/2))
    y_chunks = round(H_box/(tol/2))
    if len(nn) > 2*max(x_chunks, y_chunks):
        dX = np.diff(X)
        dY = np.diff(Y)
        if np.all(dX >= 0) or np.all(dX <= 0): # X is monotonic
            nn = simp_chunks(X, Y, x_chunks)
        elif np.all(dY >= 0) or np.all(dY <= 0): # Y is monotonic
            nn = simp_chunks(Y, X, y_chunks)
    return nn

# ------------------
# Plotting Functions
# ------------------

def plot_set(fid, setj, x_min, y_min, x_scale, y_scale,
        x_log, y_log, W_box, H_box):
    # Make a reusable index array.
    nn = np.arange(setj.x.shape[-1])

    # For each row of the data set,
    for row in range(setj.rows):
        # Get this row of data. `z` will be None.
        x = setj.x.copy() if setj.x.ndim == 1 else setj.x[row].copy()
        y = setj.y.copy() if setj.y.ndim == 1 else setj.y[row].copy()

        # Find the valid points (not nan, inf, or negative (for log)).
        x_fin = np.isfinite(x)
        y_fin = np.isfinite(y)
        nx_valid = nn[x_fin & (x > 0)] if x_log else nn[x_fin]
        ny_valid = nn[y_fin & (y > 0)] if y_log else nn[y_fin]
        nn_valid = np.intersect1d(nx_valid, ny_valid)

        # Scale the data.
        X = x; Y = y # aliases of copied rows
        X[nn_valid] = np.log10(x[nn_valid]/x_min)*x_scale if x_log \
                else (x[nn_valid] - x_min)*x_scale
        Y[nn_valid] = np.log10(y[nn_valid]/y_min)*y_scale if y_log \
                else (y[nn_valid] - y_min)*y_scale

        # Split the indices of valid points into contiguous segments.
        nn_segs = np.split(nn_valid, np.where(np.diff(nn_valid) != 1)[0] + 1)

        # For each segment,
        if setj.rows > 1:
            write_comment(fid, f"Row {row}")
        for m, nn_seg in enumerate(nn_segs):
            # Get the points of this segment.
            X_seg = X[nn_seg]
            Y_seg = Y[nn_seg]

            # Simplify the data if requested.
            if setj.simp:
                nn_simp = simp_best(X_seg, Y_seg, W_box, H_box)
                X_seg = X_seg[nn_simp]
                Y_seg = Y_seg[nn_simp]

            # Ensure segment is at least partially within the viewing region.
            if (X_seg.min() > W_box) or (X_seg.max() < 0) or \
                    (Y_seg.min() > H_box) or (Y_seg.max() < 0):
                continue

            # Write the code for this segment.
            if len(nn_segs) > 1:
                write_comment(fid, f"Segment {m}")
            write_draw(fid, setj.fmt, X_seg, Y_seg, W_box, H_box)


def scatter_set(fid, setj, x_min, y_min, x_scale, y_scale,
        x_log, y_log, W_box, H_box):
    # Make a reusable index array.
    nn = np.arange(setj.x.shape[-1])

    # For each row of the data set,
    for row in range(setj.rows):
        # Get this row of data. `z` will not be None.
        x = setj.x.copy() if setj.x.ndim == 1 else setj.x[row].copy()
        y = setj.y.copy() if setj.y.ndim == 1 else setj.y[row].copy()
        radius = math.fabs(setj.z) if np.ndim(setj.z) == 0 else setj.z.copy()
        if np.ndim(radius) == 2:
            radius = radius[row]

        # Find the valid points (not nan, inf, or negative (for log)).
        x_fin = np.isfinite(x)
        y_fin = np.isfinite(y)
        nx_valid = nn[x_fin & (x > 0)] if x_log else nn[x_fin]
        ny_valid = nn[y_fin & (y > 0)] if y_log else nn[y_fin]
        nn_valid = np.intersect1d(nx_valid, ny_valid)
        if np.ndim(radius) > 0:
            nr_valid = nn[np.isfinite(radius) & (radius > 0)]
            nn_valid = np.intersect1d(nn_valid, nr_valid)

        # Scale the `x` and `y` data.
        X = x; Y = y; R = radius # aliases of copied rows
        X[nn_valid] = np.log10(x[nn_valid]/x_min)*x_scale if x_log \
                else (x[nn_valid] - x_min)*x_scale
        Y[nn_valid] = np.log10(y[nn_valid]/y_min)*y_scale if y_log \
                else (y[nn_valid] - y_min)*y_scale

        # Split the indices of valid points into contiguous segments. Though
        # continuity is not necessary for scatter plot points, it does simplify
        # the filtering process during the write function.
        nn_segs = np.split(nn_valid, np.where(np.diff(nn_valid) != 1)[0] + 1)

        # For each segment,
        if setj.rows > 1:
            write_comment(fid, f"Row {row}")
        for m, nn_seg in enumerate(nn_segs):
            # Get the points of this segment.
            X_seg = X[nn_seg]
            Y_seg = Y[nn_seg]
            R_seg = R if np.ndim(R) == 0 else R[nn_seg]

            # The `simp` option will always be False.

            # Ensure segment is at least partially within the viewing region.
            if ((X_seg - R_seg).min() > W_box) or \
                    ((X_seg + R_seg).max() < 0) or \
                    ((Y_seg - R_seg).min() > H_box) or \
                    ((Y_seg + R_seg).max() < 0):
                continue

            # Write the code for this segment.
            if len(nn_segs) > 1:
                write_comment(fid, f"Segment {m}")
            write_mark(fid, setj.marker, setj.fmt,
                    X_seg, Y_seg, R_seg, W_box, H_box)


def fill_set(fid, setj, x_min, y_min, x_scale, y_scale,
        x_log, y_log, W_box, H_box):
    # Make a reusable index array.
    nn = np.arange(setj.x.shape[-1])

    # For each row of the data set,
    for row in range(setj.rows):
        # Get this row of data. `z` could be None or an array, not a scalar.
        x = setj.x.copy() if setj.x.ndim == 1 else setj.x[row].copy()
        y = setj.y.copy() if setj.y.ndim == 1 else setj.y[row].copy()
        if setj.z is not None:
            z = setj.z.copy() if setj.z.ndim == 1 else setj.z[row].copy()
        else:
            z = None

        # Find the valid points (not nan, inf, or negative (for log)).
        x_fin = np.isfinite(x)
        y_fin = np.isfinite(y)
        nx_valid = nn[x_fin & (x > 0)] if x_log else nn[x_fin]
        ny_valid = nn[y_fin & (y > 0)] if y_log else nn[y_fin]
        nn_valid = np.intersect1d(nx_valid, ny_valid)
        if z is not None:
            z_fin = np.isfinite(z)
            nz_valid = nn[z_fin & (z > 0)] if y_log else nn[z_fin]
            nn_valid = np.intersect1d(nn_valid, nz_valid)

        # Scale the `x` and `y` data.
        X = x; Y = y; Z = z # aliases of copied rows
        X[nn_valid] = np.log10(x[nn_valid]/x_min)*x_scale if x_log \
                else (x[nn_valid] - x_min)*x_scale
        Y[nn_valid] = np.log10(y[nn_valid]/y_min)*y_scale if y_log \
                else (y[nn_valid] - y_min)*y_scale
        if Z is not None:
            Z[nn_valid] = np.log10(z[nn_valid]/y_min)*y_scale if y_log \
                    else (z[nn_valid] - y_min)*y_scale

        # Split the indices of valid points into contiguous segments. Each
        # contiguous segment will be plotted as a separate fill.
        nn_segs = np.split(nn_valid, np.where(np.diff(nn_valid) != 1)[0] + 1)

        # For each segment,
        if setj.rows > 1:
            write_comment(fid, f"Row {row}")
        for m, nn_seg in enumerate(nn_segs):
            # Get the points of this segment.
            X_seg = X[nn_seg]
            Y_seg = Y[nn_seg]
            if Z is not None: # Append Z segment in reverse order.
                X_seg = np.concatenate((X_seg, np.flip(X_seg)))
                Y_seg = np.concatenate((Y_seg, np.flip(Z[nn_seg])))

            # Simplify the data if requested.
            if setj.simp:
                nn_simp = simp_best(X_seg, Y_seg, W_box, H_box)
                X_seg = X_seg[nn_simp]
                Y_seg = Y_seg[nn_simp]

            # Ensure segment is at least partially within the viewing region.
            if (X_seg.min() > W_box) or (X_seg.max() < 0) or \
                    (Y_seg.min() > H_box) or (Y_seg.max() < 0):
                continue

            # Write the code for this segment.
            if len(nn_segs) > 1:
                write_comment(fid, f"Segment {m}")
            write_fill(fid, setj.fmt, X_seg, Y_seg, W_box, H_box)


class HexGrid:
    def __init__(self, radius, W_box, H_box):
        # Mark if the hexagons should vary in size.
        self.radius = math.fabs(radius)
        self.variable = (radius < 0)

        # Build the rectangular grid.
        SQ3 = math.sqrt(3)
        self.W_rect = SQ3/2 * self.radius # width of each rectangle
        self.H_rect = 3/2 * self.radius # height of each rectangle
        self.C_rect = math.ceil(W_box/self.W_rect) # columns of rectangles
        self.R_rect = math.ceil(H_box/self.H_rect) # rows of rectangles
        self.dX_rect = (self.C_rect*self.W_rect - W_box)/2 # rect x-axis shift
        self.dY_rect = (self.R_rect*self.H_rect - H_box)/2 # rect y-axis shift

        # Build the hexagonal bin grid.
        self.C_hex = 1 + self.C_rect//2 # columns of hexagons
        self.R_hex = 1 + self.R_rect # rows of hexagons
        self.hexs = np.zeros((self.R_hex, self.C_hex))

        # Define the hexagon vertex arrays.
        C_vert = 2*self.C_hex + 2 # columns of vertices
        R_vert = 2*self.R_hex + 2 # rows of vertices
        cc_vert = np.arange(C_vert) # vertex column indices
        rr_vert = np.arange(R_vert//2) # vertex row indices
        s = self.radius
        self.X_vert = np.round(cc_vert*(s*SQ3/2) - s*SQ3/2 - self.dX_rect, 4)
        self.Y_vert = np.zeros(R_vert)
        self.Y_vert[::2] = np.round(rr_vert*(3*s/2) - s - self.dY_rect, 4)
        self.Y_vert[1::2] = np.round(rr_vert*(3*s/2) - s/2 - self.dY_rect, 4)


def hexbin_set(fid, setj, x_min, y_min, x_scale, y_scale,
        x_log, y_log, W_box, H_box):
    # Define the hexagonal grid.
    hex_grid = HexGrid(setj.z, W_box, H_box)

    # Make a reusable index array.
    nn = np.arange(setj.x.shape[-1])

    # For each row of the data set,
    for row in range(setj.rows):
        # Get this row of data. Each row is weighted independently.
        x = setj.x.copy() if setj.x.ndim == 1 else setj.x[row].copy()
        y = setj.y.copy() if setj.y.ndim == 1 else setj.y[row].copy()

        # Find the valid points (not nan, inf, or negative (for log)).
        x_fin = np.isfinite(x)
        y_fin = np.isfinite(y)
        nx_valid = nn[x_fin & (x > 0)] if x_log else nn[x_fin]
        ny_valid = nn[y_fin & (y > 0)] if y_log else nn[y_fin]
        nn_valid = np.intersect1d(nx_valid, ny_valid)

        # Scale the `x` and `y` data.
        X = x; Y = y # aliases of copied rows
        X[nn_valid] = np.log10(x[nn_valid]/x_min)*x_scale if x_log \
                else (x[nn_valid] - x_min)*x_scale
        Y[nn_valid] = np.log10(y[nn_valid]/y_min)*y_scale if y_log \
                else (y[nn_valid] - y_min)*y_scale

        # Split the indices of valid points into contiguous segments. Though
        # continuity is not necessary for hexagonal binning, it does simplify
        # the filtering process during the write function.
        nn_segs = np.split(nn_valid, np.where(np.diff(nn_valid) != 1)[0] + 1)

        # For each segment,
        for m, nn_seg in enumerate(nn_segs):
            # Get the points of this segment.
            X_seg = X[nn_seg]
            Y_seg = Y[nn_seg]

            # The `simp` option will always be False.

            # Ensure segment is at least partially within the viewing region.
            if (X_seg.min() > W_box) or (X_seg.max() < 0) or \
                    (Y_seg.min() > H_box) or (Y_seg.max() < 0):
                continue

            # Add these points to the hexagonal bins.
            hexbin_row(X_seg, Y_seg, hex_grid)

    # Write hexagons.
    write_hexs(fid, hex_grid, setj.scaling, setj.fmt)


def hexbin_row(X, Y, hex_grid):
    # Rectangularly bin.
    cr_rect = (X + hex_grid.dX_rect)/hex_grid.W_rect # real rect x-axis indices
    rr_rect = (Y + hex_grid.dY_rect)/hex_grid.H_rect # real rect y-axis indices
    nn_in = np.asarray((cr_rect >= 0) & (cr_rect < hex_grid.C_rect) \
            & (rr_rect >= 0) & (rr_rect < hex_grid.R_rect)).nonzero()[0]
    cr_rect = cr_rect[nn_in] # only points within bounds
    rr_rect = rr_rect[nn_in] # only points within bounds
    c_rect = np.floor(cr_rect).astype(int) # integer rectangle x-axis indices
    r_rect = np.floor(rr_rect).astype(int) # integer rectangle y-axis indices
    u = cr_rect - c_rect # normalized x-axis position within rectangle [0, 1)
    v = rr_rect - r_rect # normalized y-axis position within rectangle [0, 1)

    # Check which points are over or under the dividing line. Here, `vs` is the
    # normalized y-axis position of the sloped dividing line within a rectangle.
    # The `even_odd` array marks whether a point in on a black (True) or white
    # (False) "chess board" position in this grid of rectangular bins.
    even_odd = (c_rect % 2 == r_rect % 2)
    vs = even_odd*(2.0/3 - u/3) + (~even_odd)*(1.0/3 + u/3)
    over = (v >= vs) # over the dividing line
    under = ~over # under the dividing line

    # Check if this is an even or odd row.
    even_row = (r_rect % 2 == 0)
    odd_row = ~even_row

    # Get the indices of the left and right columns.
    left_col = np.floor(c_rect/2)
    right_col = np.floor((c_rect + 1)/2)

    # Get the hexagon column and row indices.
    c_hex = (even_row*(under*right_col + over*left_col)
            + odd_row*(under*left_col + over*right_col)).astype(int)
    r_hex = (over*(r_rect + 1) + under*r_rect).astype(int)

    # Increment the appropriate hexagon bins.
    np.add.at(hex_grid.hexs, (r_hex, c_hex), 1)


def three_sigmas(y, Tf=None):
    """
    Create a probability-density contour plot of `y` as a function of `t`.

    Parameters
    ----------
    y : (M, K) np.ndarray
        Matrix of M rows and K columns. Each row represents a realization of K
        samples in time.
    Tf : float, default None
        A factor between 0 and 0.5 equal to the product of the positive pole
        frequency in hertz and the sampling period in seconds. This is used to
        low-pass filter the resulting bands.

    Returns
    -------
    Y : (8, K) np.ndarray
        Four pairs of bands: the outer band of minimum and maximum values, the
        band of 3 sigma values, the band of 2 sigma values, and the band of 1
        sigma values. This function does not properly handle multi-modal
        densities.
    """
    # Get the number of row and columns of y.
    J, K = y.shape

    # Choose the number of bins and bands.
    bands = 4
    bins = np.ceil(math.sqrt(J)).astype(int)
    band_heights = np.array([0, 0.011, 0.135, 0.605])
    b = np.zeros(bins + 2)
    h = np.zeros(bins + 2)

    # Initialize the lower and upper edges of the bands.
    Y = np.zeros((2*bands, K))

    # For each instance in time,
    for k in range(K):
        # Get this row of y.
        y_k = y[:, k]

        # Get the histogram of this row of the y data.
        (yh, b_edges) = np.histogram(y_k, bins)

        # Get the mid-points of the bins.
        bm = (b_edges[0:bins] + b_edges[1:bins + 1])/2

        # Pad the histogram with zero bins.
        db = bm[1] - bm[0]
        b[1:-1] = bm
        b[0] = bm[0] - db
        b[-1] = bm[-1] + db
        h[1:-1] = yh

        # Normalize the bin counts.
        h /= h.max()

        # For this row of y, define the lower and upper edges of the bands.
        b_min = y_k.min()
        b_max = y_k.max()
        Y[0, k] = b_min
        Y[1, k] = b_max
        for n_band in range(1, bands):
            # Get the index before the first value greater than the threshold
            # and the last index of the last value greater than the threshold.
            z = h - band_heights[n_band]
            n = np.nonzero(z >= 0)[0]
            n_a = n[0] - 1
            n_b = n[-1]

            # Interpolate bin locations to find the correct y values of the
            # bands.
            b_a = b[n_a] + db*(0 - z[n_a])/(z[n_a + 1] - z[n_a])
            b_b = b[n_b] + db*(0 - z[n_b])/(z[n_b + 1] - z[n_b])
            if b_a < b_min:
                b_a = b_min
            if b_b > b_max:
                b_b = b_max

            # Store the interpolated bin values.
            Y[n_band*2, k] = b_a
            Y[n_band*2 + 1, k] = b_b

    # Apply filtering.
    if Tf is not None:
        Y = lpf(Y, Tf)

    return Y


def lpf(x, Tf):
    """
    Discrete, first-order, low-pass, infinite impulse response (IIR) filter,
    using the bilinear transform, applied twice, once forwards and then once
    backwards, effectively making it a second-order filter with no phase shift.
    This function uses frequency pre-warping.

    Parameters
    ----------
    x : (J, K) np.ndarray
        Input to the filter as a time-history profile of K samples.
    Tf : float
        A factor between 0 and 0.5 equal to the product of the positive pole
        frequency in hertz and the sampling period in seconds.

    Returns
    -------
    y : (J, K) np.ndarray
        Output from the filter as a time-history profile of K samples.
    """

    # Define coefficients.
    c = np.tan(math.pi*Tf)
    N1 = c/(c + 1)
    N0 = c/(c + 1)
    D0 = (c - 1)/(c + 1)
    EOld = x[:, 0]/(1 + D0)

    # Forward filter the whole array.
    J, K = x.shape
    y = np.zeros((J, K))
    for k in range(K):
        E = x[:, k] - D0*EOld
        y[:, k] = N1*E + N0*EOld
        EOld = E

    # Backward filter the whole array.
    EOld = x[:, -1]/(1 + D0)
    for k in range(K-1, -1, -1):
        E = y[:, k] - D0*EOld
        y[:, k] = N1*E + N0*EOld
        EOld = E

    return y

# --------------------------
# LaTeX Code Write Functions
# --------------------------

def write_open(fid, preamble=None):
    fid.write("% Preamble")
    fid.write("\n\\batchmode")
    fid.write("\n\\documentclass{standalone}")
    fid.write("\n\\usepackage{bm}")
    fid.write("\n\\usepackage{tikz}")
    fid.write("\n\\usepackage{pdfrender}")
    fid.write("\n\\newcommand{\\ul}[1] % vectors")
    fid.write("\n    {{}\\mkern1mu\\underline")
    fid.write("{\\mkern-1mu#1\\mkern-1mu}\\mkern1mu}")
    fid.write("\n\\DeclareSymbolFont{euler}{U}{eur}{m}{n}")
    fid.write("\n\\DeclareMathSymbol{\\PI}{\\mathord}{euler}{25}")
    if preamble is not None:
        fid.write("\n\\errorstopmode")
        fid.write("\n%s" % preamble)
        fid.write("\n\\batchmode")
    fid.write("\n% Document contents")
    fid.write("\n\\begin{document}")
    fid.write("\n\\begin{tikzpicture}")
    fid.write("\n\\errorstopmode")


def write_textstyle(fid, font_size_name):
    txt = "\n% Set the style of all text."
    txt += "\n\\tikzset{every node/.style={inner sep=0pt"
    if font_size_name != "normalsize":
        txt += ", font=\\" + font_size_name
    txt += "}}"
    fid.write(txt)


# FIXME Calculating missing colors and writing them should be separated.
def write_color_definitions(fid, sets):
    def hex_to_rgb(color):
        B = np.bitwise_and(color, 0xFF)
        RG = np.right_shift(color, 8)
        G = np.bitwise_and(RG, 0xFF)
        R = np.right_shift(RG, 8)
        return R, G, B

    # Get the scaling factor from set index to color map index.
    J = len(sets);  L = len(config.colormap)
    scale = L/max(J, L/3) if J < 5 else L/max(J, L/2)

    fid.write("\n% Define the plot colors.")
    for j in range(J):
        # Pick a color using the `colormap`.
        if sets[j].color is None:
            # Get the weight and integer map index.
            r = j*scale # real weight
            n = int(r) # integer weight
            w = r - n # fractional weight

            if n >= len(config.colormap) - 1: # end of map
                # Get the last color.
                color = config.colormap[-1]
            else: # not at end of map
                # Get the two nearest-neighbor map colors.
                C0, C1 = config.colormap[n:n + 2]
                R0, G0, B0 = hex_to_rgb(C0)
                R1, G1, B1 = hex_to_rgb(C1)

                # Mix the colors in square space using the weight.
                R = int(math.sqrt(w*R1**2 + (1 - w)*R0**2))
                G = int(math.sqrt(w*G1**2 + (1 - w)*G0**2))
                B = int(math.sqrt(w*B1**2 + (1 - w)*B0**2))

                # Convert color back to hex value.
                color = np.left_shift(R, 16) + np.left_shift(G, 8) + B
        else: # Get the color.
            color = sets[j].color

        # Write color definition.
        fid.write("\n\\definecolor{C" + str(j) + "}{HTML}{"
                + f"{color:06x}" + "}")

        # Append color to the format specifier.
        fmt = sets[j].fmt
        sets[j].fmt = f"C{j}" if fmt is None else fmt + f", C{j}"


def write_reserve(fid, lay):
    # Calculate dimensions.
    xb = lay.W_box + lay.R_margin
    yb = lay.H_box + lay.T_margin
    xa = xb - lay.width
    ya = yb - lay.height

    # Comment.
    fid.write("\n% Reserve the full figure space.")

    # Draw the sets.
    if lay.invisibles:
        # Outer figure box
        fid.write(f"\n\\draw[ultra thin, red] ({xa:0.4f},{ya:0.4f}) rectangle "
                + f"({xb:0.4f},{yb:0.4f});")
        # Margins
        xc = -lay.L_margin
        yc = -lay.B_margin
        fid.write(f"\n\\draw[ultra thin, red] ({xc:0.4f},{yc:0.4f}) rectangle "
                + f"({xb:0.4f},{yb:0.4f});")
        # Legend
        yd = -lay.H_legend - lay.B_margin
        for row in range(lay.legend_rows):
            yd += lay.H_legend_row
            fid.write(f"\n\\draw[ultra thin, red] "
                    + f"({xa:0.4f},{yd:0.4f}) -- ({xb:0.4f},{yd:0.4f});")
    else:
        fid.write(f"\n\\path ({xa:0.4f},{ya:0.4f}) rectangle "
                + f"({xb:0.4f},{yb:0.4f});")


def write_clip(fid, W_box, H_box):
    fid.write(f"\n\\clip (0,0) rectangle ({W_box:0.4f},{H_box:0.4f});")


def write_scope_begin(fid, opts=None):
    fid.write("\n% Draw the plot contents, clipping it to the box area.")
    if opts is None:
        fid.write("\n\\begin{scope}")
    else:
        fid.write("\n\\begin{scope}" + f"[{opts}]")


def write_scope_end(fid):
    fid.write("\n\\end{scope}")


def write_comment(fid, txt):
    fid.write(f"\n% {txt}")


def write_xgrid(fid, X_list, Y_max, sub=False):
    if sub:
        fid.write("\n% Draw x-axis minor grid.")
        fid.write("\n\\draw[very thin, lightgray!10]")
    else:
        fid.write("\n% Draw x-axis major grid.")
        fid.write("\n\\draw[very thin, lightgray!40]")
    for n, X in enumerate(X_list):
        if n % 2 == 0:
            fid.write("\n    ")
        else:
            fid.write("  ")
        fid.write(f"({X:0.4f},0) -- ({X:0.4f},{Y_max:0.4f})")
    fid.write(";")


def write_ygrid(fid, Y_list, X_max, sub=False):
    if sub:
        fid.write("\n% Draw y-axis minor grid.")
        fid.write("\n\\draw[very thin, lightgray!10]")
    else:
        fid.write("\n% Draw y-axis major grid.")
        fid.write("\n\\draw[very thin, lightgray!40]")
    for n, Y in enumerate(Y_list):
        if n % 2 == 0:
            fid.write("\n    ")
        else:
            fid.write("  ")
        fid.write(f"(0,{Y:0.4f}) -- ({X_max:0.4f},{Y:0.4f})")
    fid.write(";")


def write_rounded(fid):
    fid.write("\n% Round every subsequent path until the end of the clip.")
    fid.write("\n\\tikzset{every path/.style="
            + "{line cap=round, line join=round}}")


def write_draw(fid, fmt, X, Y, W_box, H_box):
    # Start the drawing command.
    fid.write("\n\\draw")
    if fmt is not None:
        fid.write(f"[{fmt}]\n   ")

    # Run state machine.
    path_visible = False
    points_on_line = 0
    for k in range(len(X)):
        # Check if this point is in the box.
        in_box = (X[k] >= 0) and (X[k] <= W_box) \
                and (Y[k] >= 0) and (Y[k] <= H_box)

        # Continue a path or start it depending on
        # if the path was visible and if it is in the box.
        if path_visible:
            if points_on_line == 3:
                fid.write("\n   ")
                points_on_line = 0
            fid.write(f" -- ({X[k]:0.4f},{Y[k]:0.4f})")
            points_on_line += 1
            if not in_box:
                path_visible = False
        elif in_box:
            if points_on_line == 3:
                fid.write("\n   ")
                points_on_line = 0
            if k == 0:
                fid.write(f" ({X[k]:0.4f},{Y[k]:0.4f})")
                points_on_line += 1
            else:
                fid.write(f" ({X[k-1]:0.4f},{Y[k-1]:0.4f})")
                fid.write(f" -- ({X[k]:0.4f},{Y[k]:0.4f})")
                points_on_line += 2
            path_visible = True

    # Close the drawing command.
    fid.write(";")


def write_mark(fid, marker, fmt, X, Y, R, W_box, H_box):
    # Build the beginning of the command.
    if marker == CIRCLES:
        cmd = "\n\\draw"
    elif marker == DOTS:
        cmd = "\n\\fill"
    if fmt is not None:
        cmd += f"[{fmt}]"

    # Write the drawing commands.
    scalar_R = (np.ndim(R) == 0)
    points_in_cmd = 0
    for k in range(len(X)):
        # Get the radius of this point.
        r = R if scalar_R else R[k]

        # Skip if this point is not in the box.
        in_box = (X[k] + r >= 0) and (X[k] - r <= W_box) \
                and (Y[k] + r >= 0) and (Y[k] - r <= H_box)
        if not in_box:
            continue

        # Restart the drawing command periodically.
        if points_in_cmd == 0:
            fid.write(f"{cmd}")

        # Write the symbol.
        fid.write(f"\n     ({X[k]:0.4f},{Y[k]:0.4f})"
                + f" circle ({r:0.4f})")
        points_in_cmd += 1

        if points_in_cmd == 32:
            fid.write(";")
            points_in_cmd = 0

    # Close the last drawing command.
    if points_in_cmd != 0:
        fid.write(";")


def write_fill(fid, fmt, X, Y, W_box, H_box):
    # Start the drawing command.
    fid.write("\n\\fill")
    if fmt is not None:
        fid.write(f"[{fmt}]\n   ")

    # Run state machine.
    path_visible = False
    points_on_line = 0
    for k in range(len(X)):
        # Check if this point is in the box.
        in_box = (X[k] >= 0) and (X[k] <= W_box) \
                and (Y[k] >= 0) and (Y[k] <= H_box)

        # Continue a path or start it depending on
        # if the path was visible and if it is in the box.
        if path_visible:
            if points_on_line == 3:
                fid.write("\n   ")
                points_on_line = 0
            fid.write(f" -- ({X[k]:0.4f},{Y[k]:0.4f})")
            points_on_line += 1
            if not in_box:
                path_visible = False
        elif in_box:
            if points_on_line == 3:
                fid.write("\n   ")
                points_on_line = 0
            if k == 0:
                fid.write(f" ({X[k]:0.4f},{Y[k]:0.4f})")
                points_on_line += 1
            else:
                fid.write(f" ({X[k-1]:0.4f},{Y[k-1]:0.4f})")
                fid.write(f" -- ({X[k]:0.4f},{Y[k]:0.4f})")
                points_on_line += 2
            path_visible = True

    # Close the drawing command.
    fid.write(";")


def write_hexs(fid, hex_grid, scaling, fmt):
    def split_hex(U):
        U1a = U[::2, ::3].flatten()
        U1b = U[1::2, 1::3].flatten()
        U2a = U[::2, 1::3].flatten()
        U2b = U[1::2, 2::3].flatten()
        U3a = U[::2, 2::3].flatten()
        U3b = U[1::2, ::3].flatten()
        U1 = np.concatenate((U1a, U1b))
        U2 = np.concatenate((U2a, U2b))
        U3 = np.concatenate((U3a, U3b))
        return U1, U2, U3

    def sort_hex(X, Y, P):
        nn = np.argsort(P)
        P = P[nn]
        X = X[nn]
        Y = Y[nn]
        return X, Y, P

    # FIXME Compensate for partially-visible hexagons.
    # FIXME Scale each row of the data set independently.
    # Normalize the hexagon counts and build matrices of indices. Testing was
    # done to show that there is no higher color mixing precision than integer
    # percentages. In other words, 100 variations is the maximum and rounding pp
    # to integers from 0 to 100 is fine.
    pp = hex_grid.hexs/np.max(hex_grid.hexs)
    if scaling != 0:
        pp = np.sqrt(scaling*(2*pp - 1) + scaling**2 + 1/4)/scaling \
                - pp - 1/(2*scaling) + 1
    pp = np.round(99*pp + 1).astype(int) # point scaling
    cc = np.outer(np.ones(hex_grid.R_hex),
            np.arange(hex_grid.C_hex)).astype(int)
    rr = np.outer(np.arange(hex_grid.R_hex),
            np.ones(hex_grid.C_hex)).astype(int)

    # Split and flatten the matrices into three sets.
    pp1, pp2, pp3 = split_hex(pp)
    cc1, cc2, cc3 = split_hex(cc)
    rr1, rr2, rr3 = split_hex(rr)

    # Sort within each set by the scaling.
    cc1, rr1, pp1 = sort_hex(cc1, rr1, pp1)
    cc2, rr2, pp2 = sort_hex(cc2, rr2, pp2)
    cc3, rr3, pp3 = sort_hex(cc3, rr3, pp3)

    # Concatenate the sets.
    pp = np.concatenate((pp1, pp2, pp3))
    cc = np.concatenate((cc1, cc2, cc3))
    rr = np.concatenate((rr1, rr2, rr3))

    # Write the hexagons.
    p_last = None # last percentage
    tol = 100.0*(ULTRA_THIN/PT_PER_CM)/hex_grid.radius
    p_smallest = 1 if not hex_grid.variable else tol
    for n in range(len(pp)):
        # Get this percentage.
        p = pp[n]
        if p <= p_smallest:
            continue

        # Start a new fill command.
        if p != p_last:
            if p_last is not None:
                fid.write(";")
            if hex_grid.variable:
                fid.write(f"\n\\fill[{fmt}]")
                s = (1.0 - p*0.01)*hex_grid.radius/2 # short-side shrink
                l = math.sqrt(3.0)*s # long-side shrink
            else:
                fid.write(f"\n\\fill[{fmt}!{p}]")
            p_last = p

        # Column of left vertex and row of bottom vertex
        cv = 2*cc[n] + int(rr[n] % 2) # column
        rv = 2*rr[n] # row

        # Coordinates of bottom half vertices, left to right
        Xa = hex_grid.X_vert[cv + 0];    Ya = hex_grid.Y_vert[rv + 1]
        Xb = hex_grid.X_vert[cv + 1];    Yb = hex_grid.Y_vert[rv + 0]
        Xc = hex_grid.X_vert[cv + 2];    Yc = hex_grid.Y_vert[rv + 1]
        # Coordinates of top half vertices, right to left
        Xd = hex_grid.X_vert[cv + 2];    Yd = hex_grid.Y_vert[rv + 2]
        Xe = hex_grid.X_vert[cv + 1];    Ye = hex_grid.Y_vert[rv + 3]
        Xf = hex_grid.X_vert[cv + 0];    Yf = hex_grid.Y_vert[rv + 2]
        # Adjust size of hexagon in variable radius mode.
        if hex_grid.variable:
            Xa += l;    Ya += s;    Yb += 2*s;  Xc -= l;    Yc += s
            Xd -= l;    Yd -= s;    Ye -= 2*s;  Xf += l;    Yf -= s

        # Write the hexagon vertices.
        fid.write("\n") # bottom half, left to right
        fid.write("    (%.4g,%.4g)" % (Xa, Ya))
        fid.write(" -- (%.4g,%.4g)" % (Xb, Yb))
        fid.write(" -- (%.4g,%.4g)" % (Xc, Yc))
        fid.write("\n   ") # top half, right to left
        fid.write(" -- (%.4g,%.4g)" % (Xd, Yd))
        fid.write(" -- (%.4g,%.4g)" % (Xe, Ye))
        fid.write(" -- (%.4g,%.4g)" % (Xf, Yf))

    # Write the closing and close the file.
    fid.write(";")


def write_line(fid, xa, ya, xb, yb, fmt=None):
    # Draw the line.
    fid.write("\n\\draw")
    if fmt is not None:
        fid.write(f"[{fmt}]")
    fid.write(f" ({xa:0.4f},{ya:0.4f}) -- ({xb:0.4f},{yb:0.4f});")


def write_text(fid, x, y, txt, fmt=None):
    if fmt is None:
        fid.write(f"\n\\node at ({x:0.4f},{y:0.4f}) {{{txt}}};")
    else:
        fid.write(f"\n\\node[{fmt}] at ({x:0.4f},{y:0.4f}) {{{txt}}};")


def write_outline_style(fid):
    fid.write("\n\\pdfrender{TextRenderingMode=1, LineWidth=1.2pt,\n"
            + "        LineCapStyle=1, LineJoinStyle=1}\\color{white}")


def write_close(fid):
    fid.write("\n\\end{tikzpicture}")
    fid.write("\n\\end{document}")
