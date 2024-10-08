.. cog_plot documentation master file, created by
   sphinx-quickstart on Tue Aug 27 11:10:27 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. raw:: html

cog_plot
========

This repository contains a package called ``cog_plot`` containing functions to generate the default plot types used in the cogitate papers.

It can generate three types of plots:

- Time series plot with statistical significance (``plot_time_series``)
- Matrices with statistical significance, such as time-frequency decomposition or temporal generalization (``plot_matrix``)
- Single trial data using a raster plot and a time series plot of the evoked response (``plot_raster``)

Setup guide
===========

The package can be installed via pip, like so:

.. code-block:: bash

   pip install git+https://github.com/Cogitate-consortium/cog_plot.git

Support
=======

This repository is meant mostly for internal use by the cogitate project. But if you find it useful, don't hesitate to contact us.

Questions?
==========

If you have any questions, feel free to open an issue or contact the maintainers (alex.lepauvre@ae.mpg.de).

Acknowledgments
===============

We would like to thank all the COGITATE consortium members:

.. raw:: html

   <div style="display: flex; flex-wrap: wrap; justify-content: space-around;">
      <div style="text-align: center;">
         <a href="https://www.arc-cogitate.com/our-team" target="_blank">
            <img src="./_static/IEEG DP Authors.png" alt="COGITATE team">
         </a>
      </div>
   </div>

.. image:: ./_static/templeton_logo.png
   :width: 200
   :align: right

This research was supported by Templeton World Charity Foundation (`TWCF0389 <https://doi.org/10.54224/20389>`_) and the Max Planck Society. The opinions expressed in this publication are those of the authors and do not necessarily reflect the views of TWCF.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   colors

   plot_matrix <generated/cog_plot.plotters.plot_matrix>
   plot_time_series <generated/cog_plot.plotters.plot_time_series>
   plot_rasters <generated/cog_plot.plotters.plot_rasters>