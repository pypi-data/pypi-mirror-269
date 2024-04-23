Preprocessing system ([TerMPS](http://tesla.parallel.ru/Ryazanova/TerMPS)) delivering the land surface parameters for the INM RAS-MSU ([TerM](http://tesla.parallel.ru/vbogomolov/INMCM37B_lake)) model.

Preprocessing system was developed in the Python programming language (Python 3) in the form of a py-module (**preprocessing_module.py**). The module (preprocessing_module.py) consists of several parts.
1. Functions for generating data on an arbitrary uniform latitude-longitude grid:
    - read_data
    - create_grid
    - select_cells
    - calc_area_cell
    - calc_weighted_average
    - calc_weighted_average4grid (multiprocessor mode)
    - calc_percentage_type
2. Functions for generating data on an arbitrary vertical (depth) grid:
   - calc_layer_bounds 
   - calc_delta_layer
   - recalc_levels
3. Additional functions:
    - write_netcdf_2d
    - write_netcdf_3d
    - convert_tiff_to_netcdf

A detailed description of the package is presented on the [Wiki](http://tesla.parallel.ru/Ryazanova/TerMPS/-/wikis/home).
