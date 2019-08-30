About colormapize
=================

About
-----

This is a small package to easily generate colormaps from images which was
built as a fun hack and should *not* be used to generate colormaps for
serious visualization work since there is no guarantee that the colormaps
made will be e.g. perceptually uniform.

Installing
----------

To install::

    pip install colormapize

Using
-----

To use, run::

    colormapize your_image.jpg colormap_name

where ``colormap_name`` is what you want to call your colormap, for example::

    colormapize your_image.jpg kittens

This should open a Matplotlib window. Click once to define the
start of a path and click again to define the end of the path. You can then use
the + and - keys to add more samples along the path. If you are not happy with
the path, just click twice again to define a new path. Once you are happy with
it, press 'enter' and you will see a preview of the colormap on the right of the
image, and the colormap will also be saved to e.g.``cmap_kittens.py``. You can
continue to redefine the path until you are happy with it, and the file will be
overwritten every time you press enter. Close the window once you are done.

To use, make sure the colormap file (e.g. ``cmap_kittens.py``) is in the same
directory as the directory where you want to make plots, and you can then use it
as follows in other scripts::

    import colormap_kittens

    ...

    plt.imshow(mydata, cmap='kittens')
