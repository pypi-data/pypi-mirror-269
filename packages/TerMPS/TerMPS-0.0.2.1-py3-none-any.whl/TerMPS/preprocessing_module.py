import numpy as np
import xarray as xr
import re
import time
from datetime import datetime

from netCDF4 import Dataset
from multiprocessing import Pool

def read_data(datainfo_in):
    """
    This function reads original input netcdf data file,
    read latitudes, longitudes and 
    calculate grid step, up and low border of cell of original data
    input: datainfo_in - dictionary with:
    (string) path - path to netcdf dataset
    (string) latname_in, lonname_in - name of lat/lon variable in netcdf file
    output: 
    (netCDF Dataset) ds -  A netCDF Dataset is a collection of dimensions, groups, variables and attributes.
    (dict) grid_src
    {(np. array) Lats, LatsUp, LatsOLow
    (np.array) Lons, LonsLeft, LonsRight
    (float) LatStep, LonStep}
    """
    ds = Dataset(datainfo_in['path_in'])
    grid_src = {}
    # read latitudes, longitudes and calc grid step, up and low border of cell of original data
    grid_src['Lats'] = ds.variables[datainfo_in['latname_in']][:]
    grid_src['LatStep'] = abs(grid_src['Lats'][0] - grid_src['Lats'][-1])/ds.variables[datainfo_in['latname_in']].size
    grid_src['LatsUp'] = grid_src['Lats'] + grid_src['LatStep']/2 # the upper border of the cell in latitude
    grid_src['LatsLow'] = grid_src['Lats'] - grid_src['LatStep']/2 # the lower border of the cell in latitude
    if(any(abs(grid_src['Lats']) == 90)):
        print('warning: Grid cells centered at poles will have zero area.')
        grid_src['LatsLow'][grid_src['LatsLow'] < -90] = -90
        grid_src['LatsUp'][grid_src['LatsUp'] > 90] = 90

    grid_src['Lons'] = ds.variables[datainfo_in['lonname_in']][:]
    grid_src['LonStep'] = abs(grid_src['Lons'][0] - grid_src['Lons'][-1])/ds.variables[datainfo_in['lonname_in']].size
    grid_src['LonsLeft'] = grid_src['Lons'] - grid_src['LonStep']/2 # the left border of the cell in longitude
    grid_src['LonsRight'] = grid_src['Lons'] + grid_src['LonStep']/2 # the right border of the cell in longitude
    if(any(abs(grid_src['Lons']) == 180)):
        print('warning: Grid cells centered at poles will have zero area.')
        grid_src['LonsLeft'][grid_src['LonsLeft'] < -180] = -180
        grid_src['LonsRight'][grid_src['LonsRight'] > 180] = 180
    return ds, grid_src

def create_grid(grid_dst):
    """
    This function creates a regulat lat-lon grid with a given lat-lon region and step
    at this stage, LonStart/LatStart should be the same as the start/end of the original data
    The VALUE of the coordinate is the center of the cell
    input: (dict) grid_dst
    {(float) LonStart, LonEnd, LonStep - region by longitude with a given Lon-step
    (float) LatStart, LatStart, LatStep - region by latitude with a given Lat-step}
    output: (dict) grid_dst
    {(np.array) Lons - array of longitude values
    (np.array) Lats - array of latitude values
    (np.array) LatsUp, LatsLow, LonsLeft, LonsRight - arrays of upper/lower and left/right borders of the cell}
    """
    if grid_dst['LonStart'] > 0:
        if grid_dst['LonStart'] > grid_dst['LonEnd']:
            grid_dst['Lons'] = np.arange(grid_dst['LonStart'], grid_dst['LonEnd'] - grid_dst['LonStep'], -grid_dst['LonStep'])
        else:
            grid_dst['Lons'] = np.arange(grid_dst['LonStart'], grid_dst['LonEnd'] + grid_dst['LonStep'], grid_dst['LonStep'])
        
    else:
        if grid_dst['LonStart'] > grid_dst['LonEnd']:
            grid_dst['Lons'] = np.arange(grid_dst['LonStart'], grid_dst['LonEnd'] - grid_dst['LonStep'], -grid_dst['LonStep'])
        else:
            grid_dst['Lons'] = np.arange(grid_dst['LonStart'], grid_dst['LonEnd'] + grid_dst['LonStep'], grid_dst['LonStep'])
    grid_dst['LonsRight'] = grid_dst['Lons'] + grid_dst['LonStep']/2 # the right border of the cell in longitude
    grid_dst['LonsLeft'] = grid_dst['Lons'] - grid_dst['LonStep']/2 # the left border of the cell in longitude
        
    if grid_dst['LatStart'] > 0:
        if grid_dst['LatStart'] > grid_dst['LatEnd']:
            grid_dst['Lats'] = np.arange(grid_dst['LatStart'], grid_dst['LatEnd'] - grid_dst['LatStep'], -grid_dst['LatStep'])
        else:
            grid_dst['Lats'] = np.arange(grid_dst['LatStart'], grid_dst['LatEnd'] + grid_dst['LatStep'], grid_dst['LatStep'])
    else:
        if grid_dst['LatStart'] > grid_dst['LatEnd']:
            grid_dst['Lats'] = np.arange(grid_dst['LatStart'], grid_dst['LatEnd'] - grid_dst['LatStep'], -grid_dst['LatStep']) 
        else:
            grid_dst['Lats'] = np.arange(grid_dst['LatStart'], grid_dst['LatEnd'] + grid_dst['LatStep'], grid_dst['LatStep'])
    grid_dst['LatsLow'] = grid_dst['Lats'] - grid_dst['LatStep']/2 # the upper border of the cell in latitude
    grid_dst['LatsUp'] = grid_dst['Lats'] + grid_dst['LatStep']/2 # the lower border of the cell in latitude
    
    if(any(abs(grid_dst['Lats']) == 90)):
        print('warning: Grid cells centered at poles will have zero area.')
        grid_dst['LatsLow'][grid_dst['LatsLow'] < -90] = -90
        grid_dst['LatsUp'][grid_dst['LatsUp'] > 90] = 90
    if(any(abs(grid_dst['Lons']) == 180)):
        print('warning: Grid cells centered at poles will have zero area.')
        grid_dst['LonsLeft'][grid_dst['LonsLeft'] < -180] = -180
        grid_dst['LonsRight'][grid_dst['LonsRight'] > 180] = 180

    return grid_dst

def select_cells(grid_src, LatLow, LatUp, LonRight, LonLeft):
    """
    This function selects cells from the original grid
    The VALUE of the coordinate is the center of the cell
    input: 
    (dict) grid_src {(np.arrays) LatsLow, LatsUp, LonsRight, LonsLeft - arrays of upper/lower and left/right borders of the cell}
    (float) LatLow, LatUp, LonRight, LonLeft - upper/lower and left/right borders of the cell
    output:
    IdxsLat, IdxsLon - indexes of original cells inside the given cell
    """
    IdxsLat = np.where((grid_src['LatsLow'] >= LatLow) & (grid_src['LatsUp'] <= LatUp))
    IdxsLon = np.where((grid_src['LonsRight'] <= LonRight) & (grid_src['LonsLeft'] >= LonLeft))
    
    return IdxsLat, IdxsLon

def calc_area_cell(grid_src):
    """
    This function calculates the area of a cell depending on its latitude
    The VALUE of the coordinate is the center of the cell
    Formula taken from Kathe Todd-Brown and Ben Bond-Lamberty. 
    RCMIP5: easy exploration, manipulation, and summarizing of CMIP5 data, EOS, submitted, 2015
    input:
    (dict) grid_src
    {(np.array) LatsUp, LonLow, Lats - arrays of upper/lower borders of the cell and latitudes of the given grid
    (float) LonStep - longitude step of the given grid}
    
    output:
    (np.array) s - the grid cell area in m2
    """
    
    R = 6371 # Earth radius, const, km
    s = np.abs(R*(np.deg2rad(grid_src['LatsUp']) - np.deg2rad(grid_src['LatsLow'])) * 
               (R*np.cos(np.deg2rad(grid_src['Lats']))*np.deg2rad(grid_src['LonStep']))) # km2
    
    return s

def calc_weighted_average(VarsOrig, s, params = None):
    """
    This function calculates the weighted average.
    Weights are area of the origin grid cells
    input:
    (np.array) VarsOrig - input original variable values
    (np.array) s - area of original cells
    output:
    (float) Var - weighted average of the output variable
    """
    
    if VarsOrig.shape[0] == 0 or VarsOrig.shape[1] == 0:
        return np.nan
    
    VarsOrigMask = VarsOrig.mask
    Weights = np.ma.masked_array(np.tile(s, (VarsOrig.shape[1], 1)).transpose(), VarsOrigMask)

    Vars = np.ma.sum(VarsOrig.transpose()*s)/np.ma.sum(Weights)
    
    
    return Vars

def calc_weighted_variance(VarsOrig, s, params = None):
    """
    This function calculates the weighted variance.
    Weights are area of the origin grid cells
    input:
    (np.array) VarsOrig - input original variable values
    (np.array) s - area of original cells
    output:
    (float) Var - weighted variance of the output variable
    """
    
    if VarsOrig.shape[0] == 0 or VarsOrig.shape[1] == 0:
        return np.nan
    
    VarsOrigMask = VarsOrig.mask
    Weights = np.ma.masked_array(np.tile(s, (VarsOrig.shape[1], 1)).transpose(), VarsOrigMask)
    
    mean = calc_weighted_average(VarsOrig, s)
    Vars = np.ma.sum((VarsOrig.transpose() - mean)**2 * s)/np.ma.sum(Weights)
    return Vars

def calc_percentage_type(VarsOrig, s, params):
    """
    This function calculates percentage of the type from the source data 
    relative to the area of the given cell.
    input:
    (np.array) VarsOrig - input original variable values
    (np.array) s - area of original cells (vector)
    (dict) params - dictionary with parametes, including:
        (np.array) categories - types of categorical variable
        (bool) normalize - switch to apply normalization or not 
    output:
    (np.array) PercType - the percentage of the types (categories) from the source data
    taking into account the area of the origin cell
    """
    
    categories = params['categories']
    
    if VarsOrig.shape[0] == 0 or VarsOrig.shape[1] == 0:
        return np.zeros_like (categories) * np.nan
    
    VarsOrigMask = VarsOrig.mask
    
    areas = np.tile(s, (VarsOrig.shape[1], 1)).transpose()
    TotS = np.ma.sum(np.ma.masked_array(areas, VarsOrigMask))
    PercType = np.empty(len(categories))
    if TotS is not np.ma.masked:
        for cat in range(0, len(categories)):
            TotS_cat = np.sum(areas[np.where(VarsOrig == categories[cat])])
            if TotS_cat is not np.ma.masked: 
                PercType[cat] = TotS_cat/TotS*100
            else:
                PercType[cat] = 0    
        if 'normalize' not in params.keys() or ~params['normalize']:
            summa = np.sum(PercType)
            if len(categories) > 1 and (summa != 100):
                PercType = PercType / summa * 100  
    else:
        PercType = np.ma.masked

    return PercType

def calc_percentage_type_with_reclassification(VarsOrig, s, params):
    """
    This function calculates percentage of the type from the source data 
    relative to the area of the given cell.
    input:
    (np.array) VarsOrig - input original variable values
    (np.array) s - area of original cells (vector)
    (dict) params - dictionary with parametes, including:
        (np.array) categories_old - types of original categorical variable
        (np.array) categories_new - types of new categorical variable
        (dict) reclassification_rule - correspondence between original and new types of categorical variable
    output:
    (np.array) PercType - the percentage of the types (categories_new) from the source data
    taking into account the area of the origin cell
    """
    
    categories_old = params['categories_old']
    categories_new = params['categories_new']
    reclassification_rule = params['reclassification_rule']

    if VarsOrig.shape[0] == 0 or VarsOrig.shape[1] == 0:
        #Аня, Саша, посмотрите, пожалуйста (здесь должен возвращаться массивов из nan-ов той же длины, что и для непустых ячеек)    
        return np.zeros_like (categories_new) * np.nan
    
    VarsOrigMask = VarsOrig.mask
    areas = np.tile(s, (VarsOrig.shape[1], 1)).transpose()
    TotS = np.ma.sum(np.ma.masked_array(areas, VarsOrigMask))
    PercType = np.zeros(len(categories_new))
    for cat in range(0, len(categories_old)):
        TotS_cat = np.sum(areas[np.where(VarsOrig == categories_old[cat])])
        if TotS_cat is not np.ma.masked:
            PercType[reclassification_rule[cat]] = PercType[reclassification_rule[cat]] + TotS_cat/TotS*100

    
    summa = np.sum(PercType)
    if (summa != 100):
        PercType = PercType / summa * 100
    
    return PercType

def add_new_frac(base_data, flag, new_area_frac, *args):
    '''
    This function adds a new fraction to aggregated categorical data.
    base_data[num_type, lat, lon] (np.array) - aggregated categorical data (area fraction of types in each cell), %
    flag (str) choice of action: 
        - "replace": replace the existing area fraction of type with a new one and recalculate the remaining area fractions
        - "add": add a area fraction of a new type and recalculate the old ones based on the added one
    new_area_frac[lat,lon] (np.array) - aggregated categorical data (area fraction of one type in each cell), %
    *args: 
        -"replace": idx - index number of the type to be replaced
                    idx_axis - number of the axis containing area fraction of types
        -"add": idx_axis - number of the axis containing area fraction of types
    '''
    if (flag == 'replace') & (len(args) > 1):
        
        base_data_new = np.ma.empty(base_data.shape)
        
        base_data = np.delete(base_data, args[0], args[1])
        total = np.ma.sum(base_data, axis = args[1])
        delta = 100. - new_area_frac
        corr_factor = delta/total
        
        base_data_corr = base_data * corr_factor
        
        base_data_new[:args[0],:,:] = base_data_corr[:args[0],:,:]
        base_data_new[args[0],:,:] = new_area_frac
        base_data_new[args[0] + 1:,:,:] = base_data_corr[args[0]:,:,:]  
        
        tot_mask = np.sum(base_data_new, axis = args[1]) == 0.
        tot_mask = np.repeat(tot_mask[np.newaxis, :, :], base_data_new.shape[0], axis=0)
        base_data_new = np.ma.array(base_data_new, mask = tot_mask)
        
        return base_data_new
        
    else: print("Mismatch in the number of arguments, see the function description")
        
    if (flag == 'add') & (len(args) == 1):
        total = np.ma.sum(base_data, axis = args[1])
        delta = 100. - new_area_frac
        corr_factor = delta/total
    
        base_data_corr = base_data * corr_factor
        
        base_data_new = np.ma.empty([base_data.shape[0] + 1, base_data.shape[1], base_data.shape[2]])
        base_data_new[:-1,:,:] = base_data_corr
        base_data_new[-1,:,:] = new_area_frac
        
        return base_data_new
        
    else: print("Mismatch in the number of arguments, see the function description")

def aggregate4row (param_dict:dict): 

    data        = param_dict['data']
    grid_src    = param_dict['grid_src']
    grid_dst    = param_dict['grid_dst']
    fill_value  = param_dict['fill_value']
    nan2zeros   = param_dict['nan2zeros']
    aggr_func   = param_dict['aggr_func']
    func_params = param_dict['func_params']
    
    i = param_dict['i']
    
    with open('log.txt', 'a') as f:
        f.write('aggregation for row %d of %d started\n'% (i, len(grid_dst['Lats'])))

    for j in range (0, len(grid_dst['Lons'])):
        IdxsLatOrig, IdxsLonOrig = select_cells(grid_src, grid_dst['LatsLow'][i],  grid_dst['LatsUp'][i],  grid_dst['LonsRight'][j],  grid_dst['LonsLeft'][j])
        
        grid_src_cr = {'LatsUp':  grid_src['LatsUp'][IdxsLatOrig],
                       'LatsLow': grid_src['LatsLow'][IdxsLatOrig],
                       'Lats':    grid_src['Lats'][IdxsLatOrig], 
                       'LonStep': grid_src['LonStep']}
        
        VarsOrig = data[IdxsLatOrig[0], IdxsLonOrig[0]].copy()
        
        s = calc_area_cell(grid_src_cr)
         
            
        if VarsOrig.shape[0] > 0 and VarsOrig.shape[1] > 0:
            if fill_value is not None:
                filling_ok = False
                n_attemts = 0
                # the following loop is needed to avoid HDF errors that sometimes appear in parallel mode
                while not filling_ok:
                    try:
                        VarsOrig = VarsOrig.where(VarsOrig != fill_value)  
                        if nan2zeros:
                            VarsOrig = VarsOrig.fillna(0)
                        filling_ok = True      
                    except RuntimeError as err: 
                        if n_attemts < 10:
                            print ('RuntimeError appears, waiting for next attempt')
                            time.sleep(1)
                        else:
                            print ('Exception still appears after 10 attempts')
                            raise
                        n_attemts += 1

            VarsOrig = VarsOrig.to_masked_array()
        
        res = aggr_func(VarsOrig, s, func_params)
        
        if isinstance (res, (float, int)):
            # for the case if aggregation function returns not an array, but one number
            res = np.array ([res])
        
        n = res.shape[0]
        
        if n == 1:
            if j == 0:    
                row = np.ma.empty([1, len(grid_dst['Lons'])])
            row[0,j] = res
        elif n > 1:
            if j == 0:    
                row = np.ma.empty([n, 1, len(grid_dst['Lons'])])
            row[:, 0, j] = res
        
    with open('log.txt', 'r') as f:
        words = f.read().split()
        count = 0
        for w in words:
            if w == 'finished':
                count += 1

    with open('log.txt', 'a') as f:
        
        f.write('aggregation for row %d finished (progress %2f %%)\n'% (i, 100*count/len(grid_dst['Lats'])))
        
    return row


        

def aggregate4grid (datainfo_in:dict, varname_in:str, grid_dst:dict, aggr_func, func_params:dict = None, n_jobs:int=1, nan2zeros:bool=False):

    """
    This function calculates the weighted average over a given coare grid, 
    by running calc_weighted_average () for each cell of a given grid. 
    Weights are area of the origin grid cells
    input: 
    datainfo_in - dictionary with:
        (string) path_in - path to netcdf dataset
        (string) latname_in, lonname_in - name of lat/lon variable in netcdf file
    
    (str) varname_in     - variable in input nectdf file
    (dict) grid_dst      - dictionary with parameters of the coase grid (grid_dst['Lons'], grid_dst['Lats'], grid_dst['LatsUp'], grid_dst['LatsLow'], grid_dst['LonsLeft'], grid_dst['LonsRight']) or path to grid namelist (*.json)
    (callable) aggr_func - function used to aggegate data for specific grid cell (e.g. calc_weighted_mean(), calc_percentage_type())
    (dict) func_params   - dict with parameters with should be passed to  aggegation function (structure depends on specific function)
    (int) n_jobs         - number of parallel processes (if n_jobs = 1, multiprocessing is not activated)
    (bool) nan2zeros     - logical key to convert nans to zeros when averaging 
    
    output:
    (np.array) res - 2d matrics with aggregated data
    """
        
    assert callable (aggr_func), 'aggr_func should be function'
        
    grid_src = {}
    ds_nc, grid_src = read_data(datainfo_in)
    
    ds_xr = xr.open_dataset(datainfo_in['path_in']) 
    
    var_info = str (ds_nc[varname_in])
    if '_FillValue of' in var_info:
        fill_value = int (re.findall('_FillValue of.*ignored', var_info)[0].replace('_FillValue of', '').replace('ignored',''))
    else:
        fill_value = None
        

    map_params = [{'data':ds_xr[varname_in],'grid_src':grid_src, 'grid_dst':grid_dst, 'fill_value': fill_value, 
                   'nan2zeros': nan2zeros, 'i': i, 'aggr_func':aggr_func, 'func_params':func_params} for i in  range(0, len(grid_dst['Lats']))]

    with open('log.txt', 'w') as f:
        f.write('calculation started\n')
    
    start = datetime.now ()
    print ('aggregate4grid() started with n_jobs = %d'%n_jobs)
    
    if n_jobs > 1:
        p = Pool (n_jobs)
        rows = p.map(aggregate4row, map_params)
        p.close()
    else:
        rows = [aggregate4row (p) for p in map_params] 
    
    print ('aggregate4grid() finished, elapsed time %s'%str(datetime.now () - start))
    
    
    res = np.concatenate(rows, axis = rows[0].ndim-2)
        
    with open('log.txt', 'a') as f:
        f.write('calculation finished\n')
    
    return res


# Block for recalculating levels by depth
# calculation of layer boundary values
def calc_layerBounds(z):
    delta = np.empty([len(z)])

    # length for edge levels
    delta[0] = (z[1] - z[0]) / 2
    delta[-1] = (z[-1] - z[-2]) / 2

    # length for all other layers
    for i in range(1, len(z)-1):
        delta[i] = (z[i+1] - z[i-1])/2
      
    # calculation of layer boundary values
    layer_bounds = np.empty([len(z)])
    # if the first level is 0, i.e. surface, then
    a = z[0]
    for i in range(0, len(z)):
        a = a  + delta[i]
        layer_bounds[i] = a
    return layer_bounds

# layer length calculation
def calc_deltaLayer(layers):
    delta = np.empty([len(layers)])
    delta[0] = layers[0] - 0
    for i in range(1, len(layers)):
        delta[i] = layers[i] - layers[i-1]
    return delta
    

# recalculation of values to required depth levels
def recalc_soilProfile(vals_orig, layers_req, layers_orig, delta_orig, param):
    if param == 'recalc':
        dim = vals_orig.shape
        vals_req = np.ma.empty([len(layers_req), dim[1], dim[2]])
        j = 0
        for i in range(0, len(layers_req)):

            if layers_req[i] <= layers_orig[j]:
                vals_req[i,:,:] = vals_orig[j,:,:]
            else:
                if (j != len(layers_orig)-1) and len(layers_orig[np.where((layers_req[i-1] <= layers_orig) & (layers_req[i] >= layers_orig))]) == 1:
                    k1 = (layers_orig[j] - layers_req[i-1])
                    k2 = (layers_req[i] - layers_orig[j])
                    vals_req[i, :, :] = (np.ma.multiply(k1,vals_orig[j,:,:]) + np.ma.multiply(k2,vals_orig[j+1,:,:]))/(k1+k2)
                    j = j + 1
                elif (j != len(layers_orig)-1) and len(layers_orig[np.where((layers_req[i-1] <= layers_orig) & (layers_req[i] >= layers_orig))]) != 1:
                    k1 = (layers_orig[j] - layers_req[i-1])
                    k2 = (layers_req[i] - layers_orig[j+1])
                    vals_req[i, :,:] = (np.ma.multiply(k1,vals_orig[j,:,:])+np.ma.multiply(vals_orig[j+1,:,:],delta_orig[j+1])+np.ma.multiply(k2,vals_orig[j+2,:,:]))/(k1+k2+delta_orig[j+1])
                    j = j + 2                
                else:
                    vals_req[i,:,:] = vals_orig[j,:,:]
    
    if param == 'average':
        vals_req = np.ma.sum(vals_orig*delta_orig, axis = 0)/np.ma.sum(delta_orig)
        
    return vals_req

def write_netcdf_2d(path:str, lats:np.array, lons:np.array, data:np.array, metadata_var:dict, metadata_file:dict):
    """
    This function writes 2 dimensional netcdf4
    input:
    (string) path - path where the file is written
    (np.array) lats, lons - array of latitude/longitude values of the given grid
    (np.array) data - data array (parameter values) on the given grid
    (dict) metadata_var - metadata for netCDF variable, following fields are neccecery: var_name, long_name, units, missing_value, source
    (dict) metadata_file - metadata for netCDF file
    
    output:
    recorded 2d netcdf4 file with data on the given grid
    """
    
    assert 'var_name' in metadata_var.keys() and \
           'long_name' in metadata_var.keys() and \
           'units' in metadata_var.keys() and \
           'missing_value' in metadata_var.keys() and \
           'source' in metadata_var.keys(), 'metadata should contain following neccecery fields: var_name, missing_value, units, long_name, source'
    
    nc = Dataset(path, 'w', format='NETCDF4')
    
    for key in metadata_file.keys():
         setattr (nc, key, metadata_file[key])

    # dimensions
    nc.createDimension('lat', len(lats))
    nc.createDimension('lon', len(lons))

    # variables
    lat = nc.createVariable('lat', 'f4', ('lat',))
    lat.units = 'degrees_north'
    lat.long_name = 'latitude'
    lon = nc.createVariable('lon', 'f4', ('lon',))
    lon.units = 'degrees_east'
    lon.long_name = 'longitude'
    par_vals = nc.createVariable(metadata_var['var_name'], 'f4', ('lat', 'lon',), fill_value = metadata_var['missing_value'])
    
    for key in metadata_var.keys():
        if key != 'var_name' and key != 'missing_value':  # @a_medvedev нужны ли эти атрибуты повторно?
            setattr (par_vals, key, metadata_var[key])
    
    lon[:] = lons
    lat[:] = lats
    par_vals[:, :] = data

    nc.close()

def write_netcdf_3d(path:str, lats:np.array, lons:np.array, data:np.array, fractions:np.array, metadata_var:dict, metadata_file:dict):
    """
    This function writes 3 dimensioanal netcdf4
    input:
    (string) path - path where the file is written
    (np.array, dtype = string) fractions - fractions of categorical data
    (np.array) lats, lons - array of latitude/longitude values of the given grid
    (np.array) data - data array (parameter values) on the given grid
    (dict) metadata_var - metadata for netCDF variable, following fields are neccecery: var_name, long_name, units, missing_value, source
    (dict) metadata_file - metadata for netCDF file
    
    output:
    recorded 3d netcdf4 file with data on the given grid
    """
    assert 'var_name' in metadata_var.keys() and \
           'long_name' in metadata_var.keys() and \
           'units' in metadata_var.keys() and \
           'missing_value' in metadata_var.keys() and \
           'source' in metadata_var.keys(), 'metadata should contain following neccecery fields: var_name, missing_value, units, long_name, source'

    nc = Dataset(path, 'w', format='NETCDF4')
    
    for key in metadata_file.keys():
         setattr (nc, key, metadata_file[key])

    # dimensions
    nc.createDimension('lat', len(lats))
    nc.createDimension('lon', len(lons))
    nc.createDimension('frac', len(fractions))

    # variables
    lat = nc.createVariable('lat', 'f4', ('lat',))
    lat.units = 'degrees_north'
    lat.long_name = 'latitude'
    lon = nc.createVariable('lon', 'f4', ('lon',))
    lon.units = 'degrees_east'
    lon.long_name = 'longitude'
    f = nc.createVariable('frac', str, ('frac',))
    f.units = '-'
    f.long_name = 'fraction'
    par_vals = nc.createVariable(metadata_var['var_name'], 'f4', ('frac', 'lat', 'lon',), fill_value = metadata_var['missing_value'])
    
    for key in metadata_var.keys():
        if key != 'var_name' and key != 'missing_value':  # @a_medvedev нужны ли эти атрибуты повторно?
            setattr (par_vals, key, metadata_var[key])
    
    lon[:] = lons
    lat[:] = lats
    f[:] = fractions
    par_vals[:, :, :] = data

    nc.close()    