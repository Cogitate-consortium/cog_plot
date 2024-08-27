<div style="width: 100%; display: flex; justify-content: space-between; align-items: center;">
  <img src="img/cogitate_logo.png" alt="Left Logo" width="200">
  <h1 style="text-align: center; flex-grow: 1;">cog_lib</h1>
  <img src="img/templeton_logo.png" alt="Right Logo" width="200">
</div>

This repository contains a package called cog_plot containing functions to generate the default plot types used in the cogitate papers

It can generate three types of plots:
- time series plot with statistical significance (plot_time_series)
- Matrices with statistical significance, such as time frequency decomposition or temporal generalization (plot_matrix)
- Singe trial data using a raster plot and a time series plot of the evoked response (plot_raster)
## Setup guide:
The package can be install via pip, like so:
```
pip install https://github.com/Cogitate-consortium/cog_plot
```

## Support
This repository is meant mostly for internal use by the cogitate project. But if you find it useful, don't hesitate to 
contact us.

## Questions?

If you have any questions, feel free to open an issue or contact the maintainers (alex.lepauvre@ae.mpg.de).

# Acknowledgments
We would like to thank all the COGITATE consortium members:
<div style="display: flex; flex-wrap: wrap; justify-content: space-around;">
   <div style="text-align: center;">
      <a href="https://www.arc-cogitate.com/our-team" target="_blank">
         <img src="img/IEEG DP Authors.png" alt="COGITATE team">
      </a>
   </div>
</div>
<img style="float: right;" src="img/templeton_logo.png" width=200;>
<br />
<br />

This research was supported by Templeton World Charity Foundation ([TWCF0389](https://doi.org/10.54224/20389)) and the Max Planck Society. The opinions expressed in this publication are those of the authors and do not necessarily reflect the views of TWCF.