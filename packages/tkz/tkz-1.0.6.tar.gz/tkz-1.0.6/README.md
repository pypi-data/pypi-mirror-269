# TikZ Figure Generator

There is a need for professional-looking figures. Good quality figures in
publications are clear and easy to understand. This means they should not be
badly pixelated. Though it is tempting to take a screen shot of your figures to
then include in your papers, this is a sure way to produce poor-quality images.
Often, the text will be hard to read, the lines will be pixelated, and important
details will be lost. One solution to this is vector-based figures. Tools like
MatPlotLib can already generate vector pdf images. However, this raises another
problem. Vector plots of large data sets can consume significant disk space.
Even a paper with a few figures, each a megabyte can become too large to email.
This is very practical concern.

A typical journal paper column width is only about 3.4 in (8.636 cm). This means
figures which are large on your screen with reasonably-sized text will be
illegible when put into a paper. When the text of axis labels, tick labels, and
legends is made large enough to read, it will take up much valuable space that
would be better spent on the actual content of the figure. On top of that,
libraries like MatPlotLib will impose generous margins around the figure, which
further consume space. And when these margins are made smaller, there is no
guarantee that some of the text will not be cut off.

Even without considering these problems, the text of typical figures will not
match the type face of the rest of your document, especially if your document is
written in LaTeX, which uses its own fonts.

This library solves all these problems. It produces vector-based figures using
the popular LaTeX plugin called TikZ. The output files are native LaTeX files,
so all the text and formatting should be consistent with the rest of your
document. By default, this library automatically performs fast
line-simplification to produce the same look with less data. So, large data sets
can be plotted without consuming much disk space. By default, tick labels are
moved inside the plotting box so more space is used for the actual plotting.
Legends are moved to the bottom of the figure, beneath the x-axis label. This
way, text can be large enough to be legible without taking away from valuable
space for the content of the figure. The space required for axis labels, tick
labels, and legends is carefully calculated ensuring just the right amount of
space is provided around the content of the figure. This ensures the overall
figure sizes matches exactly what was requested by the user.

Currently, the most commonly used plotting types are supported: plots, scatter
plots, fills, and heat maps (in the form of hexagonal binning). However, much
more is planned for the future.

## Example

The following is a code example for creating a plot with this library::

```python
import numpy as np
import tkz

t = np.linspace(0, 2*np.pi, 10000)
x = np.cos(t)
y = np.sin(t)

fig = tkz.graph('test_basic')
fig.plot(x, y)
fig.xlabel = 'x axis'
fig.ylabel = 'y axis'
fig.equal = True
fig.render()
```

First, a figure object is created with `tkz.graph()`. This object holds settings
pertaining to the whole figure, like the width, height, and font size. Second,
path objects are added with `fig.plot()`. This object holds everything
pertaining to a particular path, like the `x` and `y` arrays, the line `width`,
`color`, `opacity`, `pattern` style, and `label`. To render the figure, the
`.render()` method is called on the `fig` object. Note, the default setting is
for the LaTeX file to be generated as a standalone file with its own document
class declaration and preamble. When it is standalone, this Python library will
then try to automatically compile the LaTeX file with the `pdflatex` command. If
`fig.standalone` is set to `False` then only the TikZ draw commands will be
included. This file can then be `input` within the `tikzpicture` environment of
another LaTeX file.

## Global Options

```python
tkz.config.<option> = <value>
```

There are some options you can set for all figures in your file:

| Option       | Description                                 | Default Value |
| :----------- | :------------------------------------------ | ------------- |
| `skip`       | flag to skip all subsequent plotting        | `False`       |
| `directory`  | directory of the generated figure files     | `None`        |
| `standalone` | flag to create standalone LaTeX file        | `True`        |
| `savepng`    | flag to convert pdf to png too              | `False`       |
| `savetex`    | flag to keep the LaTeX source file          | `False`       |

Because compiling LaTeX files can be slow, it might be helpful sometimes to turn
off all tkz renders. This can be done by setting `skip` to `True`. If
`directory` is left as `None` then the figures will be generated in the current
working directory. If the `standalone` flag is `True`, this library will attempt
to call the `pdflatex` command line program to compile the `.tex` file and
produce a pdf image. Because you may need a rasterized version of your figure
after all (see Microsoft Office's lack of support for pdf vector images), the
`savepng` option will produce a png version of the image from the pdf version.
This requires the program `pdftoppm` from the `poppler` command line utilities
package, and that the `standalone` option is set to `True`. By default, after a
standalone LaTeX file is created and the pdf file is compiled, the source LaTeX
file will be deleted. If you want to save the LaTeX file for inspection or
tweaking, set the `savetex` option to `True`.

## Figure Options

```python
fig = tkz.graph(<options>)
```

All of the following options can be set after the `graph` object is created or
during as class arguments.

| Property      | Description                            | Default Value     |
| :------------ | :------------------------------------- | :---------------: |
| `filename`    | string of file without extension       | `'fig'`           |
| `width`       | width of pdf image in centimeters      | 8.636 cm (3.4 in) |
| `height`      | height of pdf image in centimeters     | 5.337 cm (2.1 in) |
| `xmin`        | x-axis minimum                         | min of `x`        |
| `xmax`        | x-axis maximum                         | max of `x`        |
| `ymin`        | y-axis minimum                         | min of `y`        |
| `ymax`        | y-axis maximum                         | max of `y`        |
| `xpad`        | use padding on x axis                  | `False`           |
| `ypad`        | use padding on y axis                  | `True`            |
| `xlog`        | flag to use log scaling on x axis      | `False`           |
| `ylog`        | flag to use log scaling on y axis      | `False`           |
| `equal`       | flag to use axis equal scaling         | `False`           |
| `fontsize`    | font size in points                    | 9 pt              |
| `xlabel`      | x-axis label                           | `None`            |
| `ylabel`      | y-axis label                           | `None`            |
| `xaxis`       | flag to show x axis                    | `True`            |
| `yaxis`       | flag to show y axis                    | `True`            |
| `xgrid`       | flag to show x grid                    | `True`            |
| `ygrid`       | flag to show y grid                    | `True`            |
| `xsubgrid`    | flag to show x sub-grid                | `True`            |
| `ysubgrid`    | flag to show y sub-grid                | `True`            |
| `xtick`       | flag to show x ticks                   | `True`            |
| `ytick`       | flag to show y ticks                   | `True`            |
| `ticksize`    | size of tick marks (cm)                | 0.1 cm            |
| `xout`        | flag to put x-axis ticks outside       | `False`           |
| `yout`        | flag to put y-axis ticks outside       | `False`           |
| `rowmajor`    | flag to layout legend row major        | `False`           |
| `columns`     | number of legend columns               | `None`            |
| `preamble`    | added string of LaTeX code in preamble | `None`            |

If either the `width` or `height` is specified, but not both, the other
dimension will be calculated based on an aspect ratio equal to the golden ratio.

Setting `equal` to `True` is equivalent to `plt.axis('equal')` in MatPlotLib.

## Data Set Options

### Plot

```python
tkz.plot(x, y=None, color=None, opacity=1.0, width=THICK,
        pattern=None, label=None, simp=True, fmt=None)
```

Create a graph of a connected path defined by `x` and `y`. If `y` is not
provided, the values in `x` will be used as the `y` values and the integer
indices will be used for the `x` values.

-   `color` should be a 6-character hexadecimal value for the color in the form
    `0xRRGGBB`. If `color` is not given, a value will automatically be chosen
    from the color map.
-   `opacity` should be a floating-point value between 0 and 1.
-   `width` is the line width in pixels. The following values are predefined:

    | Name        | Pixels |
    | ----------: | -----: |
    | THINEST     | 0.05   |
    | ULTRA_THIN  | 0.10   |
    | VERY_THIN   | 0.20   |
    | THIN        | 0.40   |
    | SEMI_THICK  | 0.60   |
    | THICK       | 0.80   |
    | VERY_THICK  | 1.20   |
    | ULTRA_THICK | 1.60   |
    | THICKEST    | 100.00 |

-   `pattern` is the line pattern index. The following values are predefined.

    | Name          | Index | Pattern |
    | ------------: | :---: | ------: |
    | SOLID         |   0   | `----`  |
    | DASHDOTTED    |   1   | `-.-.`  |
    | DASHED        |   2   | `- - `  |
    | DENSELYDOTTED |   3   | `....`  |
    | DOTTED        |   4   | `. . `  |
    | LOOSELYDOTTED |   5   | `. ` ` .` |

-   `label` is the text with which to identify the path in the legend. Unlike
    MatPlotLib, if any path object has a label defined, a legend will be
    created. There is no additional `legend` command required.
-   `simp` is the boolean flag used to control whether the path will be subject
    to line simplification. Please note that TeX is memory limited and can run
    out of memory for large data sets if `simp` is not `True`.
-   `fmt` is an optional string used to specify any additional formatting
    options which TikZ would understand. This option is meant for users who are
    experienced using the TikZ library.

### Scatter

```python
tkz.scatter(x, y=None, radius=0.03, color=None, opacity=1.0,
        marker=CIRCLES, label=None, fmt=None)
```

Create a scatter plot of circles or dots defined by `x` and `y`. If `y` is not
provided, the values in `x` will be used as the `y` values and the integer
indices will be used for the `x` values.

-   `radius` is the radius of the circles or dots in units of pixels.
-   `color` should be a 6-character hexadecimal value for the color in the form
    `0xRRGGBB`. If `color` is not given, a value will automatically be chosen
    from the color map.
-   `opacity` should be a floating-point value between 0 and 1.
-   `marker` is the style of the scatter plot. More styles might be added in the
    future, but for now the possible values are

    | Name    | Index |
    | ------: | :---: |
    | CIRCLES |   0   |
    | DOTS    |   1   |

-   `label` is the text with which to identify the path in the legend. Unlike
    MatPlotLib, if any path object has a label defined, a legend will be
    created. There is no additional `legend` command required.
-   `fmt` is an optional string used to specify any additional formatting
    options which TikZ would understand. This option is meant for users who are
    experienced using the TikZ library.

Note that no `simp` option is available, because it would not make sense for
there to be.

### Fill

```python
fill(x, y=None, z=None, color=None, opacity=1.0,
        label=None, simp=True, fmt=None)
```

Create a filled-area plot defined by `x` and `y`. If `y` is not provided, the
values in `x` will be used as the `y` values and the integer indices will be
used for the `x` values. If `z` is also provided, the area between `y` and `z`
will be filled.

-   `color` should be a 6-character hexadecimal value for the color in the form
    `0xRRGGBB`. If `color` is not given, a value will automatically be chosen
    from the color map.
-   `opacity` should be a floating-point value between 0 and 1.
-   `label` is the text with which to identify the path in the legend. Unlike
    MatPlotLib, if any path object has a label defined, a legend will be
    created. There is no additional `legend` command required.
-   `simp` is the boolean flag used to control whether the path will be subject
    to line simplification. Please note that TeX is memory limited and can run
    out of memory for large data sets if `simp` is not `True`.
-   `fmt` is an optional string used to specify any additional formatting
    options which TikZ would understand. This option is meant for users who are
    experienced using the TikZ library.

No edge options exist, but it is simple enough to create another plot on top of
a filled-area, providing the edges. This in fact does not consume any more disk
space than having a single fill command with edges.

### Hex Bin

```python
hexbin(x, y=None, radius=0.2, color=None, opacity=1.0, scaling=0,
        label=None, fmt=None)
```

Create a 2D mesh of hexagons, representing the binning of the values in `x` and
`y`. If `y` is not provided, the values in `x` will be used as the `y` values
and the integer indices will be used for the `x` values.

-   `radius` is the distance from the center of the hexagon to any vertex of the
    hexagon in units of centimeters. By default, hexagons with higher bin values
    will be more saturated with whatever the color is that is chosen for that
    path. Hexagons with lower bin values will be more white, blending into the
    color of the background. However, if `radius` is negative, then rather than
    varying the color saturation, the hexagons will vary their size. The
    hexagons with the highest bin values will be the full `radius` in size.
    Hexagons with lower bin values will be smaller.
-   `color` should be a 6-character hexadecimal value for the color in the form
    `0xRRGGBB`. If `color` is not given, a value will automatically be chosen
    from the color map.
-   `opacity` should be a floating-point value between 0 and 1.
-   `scaling` represents a bending of the otherwise linear relationship between
    the bin count and color saturation (or hexagon size). If `scaling` is
    greater than zero, color (size) will be skewed towards saturated (large). If
    `scaling` is less than zero, color (size) will be skewed towards white
    (small).
-   `label` is the text with which to identify the path in the legend. Unlike
    MatPlotLib, if any path object has a label defined, a legend will be
    created. There is no additional `legend` command required.
-   `fmt` is an optional string used to specify any additional formatting
    options which TikZ would understand. This option is meant for users who are
    experienced using the TikZ library.

Note that no `simp` option is available, because it is unnecessary since all the
points are compressed into bins.

## Dual Axes

This library does not support dual axes. This is on purpose. See
<https://blog.datawrapper.de/dualaxis/>.
