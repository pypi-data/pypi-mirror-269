
import os

import cdsapi
import numpy as np
import pandas as pd
import scipy
import scipy.interpolate
import xarray as xr

import ddeq


g = scipy.constants.g
R = 287.058

# define some variables for the calculation of the weighted wind profile
lower_bounds = np.array([170,  310,  470,  710]) # height bound of GNFR-A weights
upper_bounds = np.array([310,  470,  710,  990]) # height bound of GNFR-A weights
values =       np.array([0.08, 0.46, 0.29, 0.17]) # GNFR-A weights
bounds = np.append(lower_bounds, upper_bounds[-1])
width = np.diff(bounds)


def prepare(time, coords, query, prefix="", timesteps=1, data_path=".",
             overwrite=False):
    """
    Prepare ERA5 wind speed data for a given area. Download ERA5 data if not
    available in data path. Calculate total wind speed and direction.

    Parameters:
    ----------
    time : datetime64 or xarray
        Time for which the wind data should be downloaded
    coords : str or tuple
        Indicate for which coordinates the wind data should be downloaded
        "global" for global coverage or a tuple of coordinates: (lon,lat)
    query : str
        Indicate how the wind should be vertically averaged
            - gnfra: GNFR-A weighted wind on model level wind
            - pbl_mean: Mean wind in pbl
            - pressure_levels: Mean wind of pressure levels 1000 to 700 hPa
    prefix : str
        Prefix of the name of the downloaded data
    timesteps : int
        Number of timesteps before "time" for which the data should be
        downloaded. If 24, a full day will be returned.
    data_path : str
        Path to which the files should be saved
    overwrite : bool
        Indicates if the file should be overwritten if it already exists

    Returns:
    --------
    winds : netCDF
        A file containing the u and v component of the wind, total wind speed
        and direction
    """

    if isinstance(time, xr.DataArray):
        time = pd.Timestamp(time.to_pandas())
    elif isinstance(time, np.datetime64):
        time = pd.Timestamp(time)

    if coords == "global":
        area = [90, -180, -90, 180]

    elif isinstance(coords, tuple):
        lon_o, lat_o = coords
        area = [lat_o - 0.251, lon_o - 0.251, lat_o + 0.251, lon_o + 0.251]

    if query == "gnfra":
        era5_filename_lvl, era5_filename_sfc = download_model_lvl(
            time, area, prefix=prefix, data_path=data_path, overwrite=overwrite,
            timesteps=timesteps
        )

        weighted_wind = calculate_gnfra_weighted_winds(
            era5_filename_lvl, era5_filename_sfc
        )
        weighted_wind = weighted_wind[["u", "v"]]
        weighted_wind = weighted_wind.transpose(*("latitude", "longitude", "time"))

        wind = xr.Dataset(
            data_vars={
                'U': (['lat', 'lon', 'time'], weighted_wind.u.values,
                      {'long_name': 'GNFR-A weighted u-wind', 'units': 'm/s'}),
                'V': (['lat', 'lon', 'time'], weighted_wind.v.values,
                      {'long_name': 'GNFR-A weighted v-wind', 'units': 'm/s'}),
            },
            coords={
                'lat': weighted_wind['latitude'].values.flatten(),
                'lon': weighted_wind['longitude'].values.flatten(),
                'time': weighted_wind['time'],
            }
        )

        description = (
            'U- and V-wind component vertically weighted for GNFR-A emission '
            'profile (Brunner et al. 2019)'
        )

    elif query == "pbl_mean":
        era5_filename_lvl, era5_filename_sfc = download_model_lvl(
            time, area, prefix=prefix, data_path=data_path, overwrite=overwrite,
            timesteps=timesteps
        )

        era5_filename_pbl = download_pbl(time,
                                         area=[90, -180, -90, 180],
                                         prefix="",
                                         data_path=data_path,
                                         overwrite=overwrite,
                                         timesteps=timesteps)

        era5_pbl = xr.open_dataset(era5_filename_pbl)
        wind_height = compute_height_levels(era5_filename_lvl, era5_filename_sfc)

        # interpolate pbl to era5 grid
        pbl_subset = era5_pbl.interp(latitude=wind_height.latitude,
                                     longitude=wind_height.longitude)

        wind = xr.merge([wind_height, pbl_subset[["blh"]]])

        # select data below pbl
        wind_pbl = wind.where(wind.h <= wind.blh)
        wind_pbl["blh"] = wind_pbl.blh.mean(dim="level", keep_attrs=True)

        # only use values where the blh is higher than 400m (based on GNFR-A profile)
        wind_pbl = wind_pbl.mean('level')
        wind_pbl = wind_pbl.where(wind_pbl.blh > 400)

        wind_pbl = wind_pbl[["u", "v", "blh"]]
        wind_pbl = wind_pbl.transpose(*("latitude", "longitude", "time"))

        wind = xr.Dataset(
            data_vars = {
                'U': (['lat', 'lon', 'time'], wind_pbl.u.values,
                      {'long_name': 'mean u-wind in pbl', 'units': 'm/s'}),
                'V': (['lat', 'lon', 'time'], wind_pbl.v.values,
                      {'long_name': 'mean u-wind in pbl', 'units': 'm/s'}),
                'blh': (['lat', 'lon', 'time'], wind_pbl.blh.values,
                        {'long_name': 'boundary layer height', 'units': 'm'}),
            },
            coords = {
                'lat': wind_pbl['latitude'].values.flatten(),
                'lon': wind_pbl['longitude'].values.flatten(),
                'time': wind_pbl['time'],
            }
        )

        description = (
            'Vertical mean of U- and V-wind component inside the planetary '
            'boundary layer'
        )

    elif query == "pressure_levels":
        era5_filename = download_pressure_lvl(time, area, prefix=prefix,
                                              data_path=data_path, overwrite=overwrite,
                                              timesteps=timesteps)

        w = xr.open_dataset(era5_filename)

        w = w.mean('level')
        w =  w[["u", "v"]]
        w = w.transpose("latitude", "longitude", "time")

        wind = xr.Dataset(
            data_vars = {
                'U': (['lat', 'lon', 'time'], w.u.values,
                      {'long_name': 'unweighted u-wind', 'units': 'm/s'}),
                'V': (['lat', 'lon', 'time'], w.v.values,
                      {'long_name': 'unweighted v-wind', 'units': 'm/s'}),
            },
            coords = {
                'lat': w['latitude'].values.flatten(),
                'lon': w['longitude'].values.flatten(),
                'time': w['time'],
            }
        )

        description = (
            'Mean of U- and V-wind component of the pressure levels [700, 750, '
            '775, 800, 825, 850, 875, 900, 925, 950, 975, 1000]'
        )

    attrs = {
        'CREATOR': 'ddeq.era5',
        'DATE_CREATED': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),
        'ORIGIN': 'ERA-5',
        'DESCRIPTION': description
    }

    wind.attrs.update(attrs)

    wind['speed'] = xr.DataArray(
        np.sqrt(wind.U**2 + wind.V**2),
        attrs = {'units': 'm s-1'}
    )
    wind['speed_precision'] = xr.DataArray(
        np.full_like(wind.U, 1.0),
        dims = wind.speed.dims,
        attrs = {'units': 'm s-1'}
    )
    wind['direction'] = xr.DataArray(
        ddeq.wind.calculate_wind_direction(wind.U, wind.V),
        attrs = {'units': '°'}
    )

    if isinstance(coords, tuple):
        wind = wind.sel(lon=lon_o,
                        lat=lat_o,
                        method='nearest')

    return wind





def download_pressure_lvl(time, area, prefix="", data_path='.', overwrite=False,
                          timesteps=1):
    """
    Download ERA-5 data on pressure levels of a given time step.
    Documentation: https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation

    timesteps :: number of hours to download on the given day.
        If 24, a full day will be returned.
    """

    if prefix != "":
        prefix = prefix + "_"

    if timesteps == 24:
        era5_filename = os.path.join(
            data_path,
            time.strftime(f'{prefix}ERA5-wind-%Y%m%d.nc')
        )
    else:
        era5_filename = os.path.join(
            data_path,
            time.strftime(f'{prefix}ERA5-wind-%Y%m%dt%H00.nc')
        )

    if os.path.exists(era5_filename) and not overwrite:
        return era5_filename

    if timesteps == 1:
        t = time.round('H').strftime('%H:00')
    elif timesteps == 24:
        t = [f"{hour:02d}:00" for hour in range(0, timesteps, 1)]
    else:
        t = [f"{hour:02d}:00" for hour in range(
            max(0,time.round('H').hour+1-timesteps),
            time.round('H').hour+1,
            1)]

    cds = cdsapi.Client()

    query = {
        'product_type'     : 'reanalysis',
        'date'             : time.strftime('%Y-%m-%d'),
        'time'             : t,
        'format'           : 'netcdf',
        'variable'         : ['geopotential', 'temperature',
                              'u_component_of_wind',
                              'v_component_of_wind'],
        'pressure_level'   : ['700', '750', '775', '800', '825', '850', '875',
                              '900', '925', '950', '975', '1000'],
        'area'             : area, # north, east, south, west
    }

    r = cds.retrieve('reanalysis-era5-pressure-levels', query, era5_filename)

    return era5_filename


def download_model_lvl(time, area, prefix="", data_path='.', overwrite=False,
                       timesteps=1): 
    """
    Download ERA-5 data on model levels of a given time step.

    timesteps :: number of hours to download on the given day.
        If 24, a full day will be returned.
    """

    if prefix != "":
        prefix = prefix + "_"

    if timesteps == 24:
        era5_filename_lvl = os.path.join(
            data_path,
            time.strftime(f'{prefix}ERA5-lvl-%Y%m%d.nc')
        )
    else:
        era5_filename_lvl = os.path.join(
            data_path,
            time.strftime(f'{prefix}ERA5-lvl-%Y%m%dt%H00.nc')
        )

    if os.path.exists(era5_filename_lvl) and not overwrite:
        return era5_filename_lvl, era5_filename_lvl.replace("lvl", "sfc")

    cds = cdsapi.Client()

    # data download specifications:
    cls     = "ea"
    expver  = "1"
    levtype = "ml"
    stream  = "oper"
    tp      = "an"
    date    = time.strftime("%Y-%m-%d")
    grid    = [0.25, 0.25]
    area    = area # north, east, south, west

    if timesteps == 1:
        time = time.round('H').strftime('%H:00')
    elif timesteps == 24:
        time = [f"{hour:02d}:00" for hour in range(0, timesteps, 1)]
    else:
        time = [f"{hour:02d}:00" for hour in range(
            max(0,time.round('H').hour+1-timesteps),
            time.round('H').hour+1,
            1)]

    # model levels
    query_lvl = {
        'class'   : cls,
        'date'    : date,
        'expver'  : expver,
        # 1 is top level, 137 the lowest model level in ERA5
        'levelist': '100/to/137/by/1',
        'levtype' : levtype,
        # temperature (t), u- and v-wind, and specific humidity (q)
        'param'   : '130/131/132/133',
        'stream'  : stream,
        'time'    : time,
        'type'    : tp,
        # Latitude/longitude grid: east-west (longitude) and north-south
        # resolution (latitude). Default: 0.25 x 0.25°
        'grid'    : grid,
        'area'    : area, # North, West, South, East. Default: global
        'format'  : 'netcdf'
    }

    cds.retrieve('reanalysis-era5-complete', query_lvl, era5_filename_lvl)

    query_sfc = {
            'class'   : cls,
            'date'    : date,
            'expver'  : expver,
            # Geopotential (z) and Logarithm of surface pressure (lnsp)
            # are 2D fields, archived as model level 1
            'levelist': '1',
            'levtype' : levtype,
            # Geopotential (z) and Logarithm of surface pressure (lnsp)
            'param'   : '129/152',
            'stream'  : stream,
            'time'    : time,
            'type'    : tp,
            # Latitude/longitude grid: east-west (longitude) and north-south
            # resolution (latitude). Default: 0.25 x 0.25°
            'grid'    : grid,
            'area'    : area, 
            'format'  : 'netcdf'
        }

    cds.retrieve('reanalysis-era5-complete', query_sfc,
                 era5_filename_lvl.replace("lvl", "sfc"))

    return era5_filename_lvl, era5_filename_lvl.replace("lvl", "sfc")



def download_pbl(time, area, prefix="", data_path='.', overwrite=False, 
                 timesteps=1):
    """
    Download ERA-5 pbl data of a given time step.

    time : datetime
        Time for which the pbl should be downloaded
    area : array
        North, West, South, East coordinates of area of interest,
        e.g [60, -10, 50, 2]
    prefix : str
        Prefix for the downloaded data
    data_path : str
        Path where to store the data
    overwrite : bool
        Indicates if the file should be overwritten if it already exists
    timesteps : int
        number of hours to download on the given day.
        If 24, a full day will be returned.

    Returns
    -------
    era5_filename_pbl : str
        Path to the downloaded ERA5 data
    """
    if prefix != "":
        prefix = prefix + "_"

    if timesteps == 24:
        era5_filename_pbl = os.path.join(
            data_path,
            time.strftime(f'{prefix}ERA5-pbl-%Y%m%d.nc')
        )
    else:
        era5_filename_pbl = os.path.join(
            data_path,
            time.strftime(f'{prefix}ERA5-pbl-%Y%m%dt%H00.nc')
        )

    if os.path.exists(era5_filename_pbl) and not overwrite:
        return era5_filename_pbl

    cds = cdsapi.Client()

    # data download specifications:
    date    = time.strftime("%Y-%m-%d")
    grid    = [0.25, 0.25]

    if timesteps == 1:
        t = time.round('H').strftime('%H:00')
    elif timesteps == 24:
        t = [f"{hour:02d}:00" for hour in range(0, timesteps, 1)]
    else:
        t = [f"{hour:02d}:00" for hour in range(
            max(0,time.round('H').hour+1-timesteps),
            time.round('H').hour+1,
            1)]

    # model levels
    query_lvl = {
        'product_type' : 'reanalysis',
        'date'         : date,
        'variable'     : 'boundary_layer_height',
        'time'         : t,
        'grid'         : grid,
        'area'         : area,
        'format'       : 'netcdf'
    }

    cds.retrieve('reanalysis-era5-single-levels', query_lvl, era5_filename_pbl)

    return era5_filename_pbl








def calculate_gnfra_weighted_winds(filename_lvl, filename_sfc):
    """
    Compute a vertically averaged wind speed based on a GNFR-A weighted wind.

    Note that the current implementation is quite slow and thus only recommended
    for small regions.
    """
    def func(s):
        # get values on model level boundaries
        if bounds[0] <= s < bounds[-1]:
            i = np.searchsorted(bounds, s, side='right')
            return values[i-1]
        else:
            return 0.0

    # compute heights
    wind = compute_height_levels(filename_lvl, filename_sfc)

    # compute weights (by quick interpolation)
    z2 = np.linspace(0,1000, 501)
    func_vec = np.vectorize(func)
    w2 = func_vec(z2)
    ifunc = scipy.interpolate.interp1d(z2, w2, bounds_error=False, fill_value=0.0)

    w2 = ifunc(wind.h.values)
    wind["weights"] = ((wind.h.dims), w2)
    wind["weights"] = wind.weights / wind.weights.sum(dim="level")

    # computed vertically-weighted winds
    wind["u"] = (wind.u * wind.weights).sum(dim="level") / wind.weights.sum(dim="level")
    wind["v"] = (wind.v * wind.weights).sum(dim="level") / wind.weights.sum(dim="level")
    wind["u"].attrs = {"units":"m/s", "long_name": "GNFR-A weighted u-wind"}
    wind["v"].attrs = {"units":"m/s", "long_name": "GNFR-A weighted v-wind"}

    return wind


def compute_height_levels(filename_lvl, filename_sfc):
    """
    Compute the geometric height of the ERA5 model levels using the hypsometric equation

    filename_lvl : str
        File name of the file containing the ERA5 data on model levels
    filename_sfc : str
        File name of the file containing the ERA5 data on the surface
    """

    lvl = xr.open_dataset(filename_lvl)
    sfc = xr.open_dataset(filename_sfc)

    era5 = xr.merge([lvl, sfc])
    era5["ps"] = np.exp(sfc['lnsp'])

    a, b = read_l137_a_and_b_parameter()
    lower_value = np.nanmin(era5.level.values.astype(int))-1
    era5["a"] = (("level_bound"), a[np.insert(era5.level.values.astype(int), 0,
                                              lower_value)],
                 {"units": "Pa"})
    era5["b"] = (("level_bound"), b[np.insert(era5.level.values.astype(int), 0,
                                              lower_value)],
                 {"units": 1})

    # calculate pressure
    era5["p_bound"] = era5.a + era5.b * era5.ps
    era5["p_bound"] = era5["p_bound"].transpose('time', 'level_bound',
                                                'latitude', 'longitude')
    era5["p_mid"] = (era5.t.dims, 0.5 * (era5.p_bound.values[:,1:,:,:]
                                         + era5.p_bound.values[:,:-1,:,:]),
                     {"units": "Pa"})

    # calculate virtual temperature
    era5["t_v"] = era5.t * (1. + 0.609133 * era5.q)
    era5["t_v"].attrs = {"units": "K",
                         "long_name": "virtual_temperature"}

    # calculate thickness of layer with hypsometric equation
    era5["dh"] = R * era5.t_v / g * np.log(era5.p_bound.values[:,1:,:,:]
                                           / era5.p_bound.values[:,:-1,:,:])
    era5["dh"].attrs = {"units": "m", "long_name": "thickness_of_model_level"}

    # height at upper boundary of level
    era5["h"] = era5["dh"][:,::-1,:,:].cumsum(dim='level')
    era5["h"] = era5.h-era5.dh/2 # height at the middle of the level
    era5["h"].attrs = {"units": "m", "long_name": "height_of_model_level"}

    return era5


def read_l137_a_and_b_parameter(filename=None):
    """
    Returns a and b paramaters for computing vertical levels of ERA5 model:
        ph = a + b * surface_pressure
    """
    if filename is None:
        filename = os.path.join(
            ddeq.DATA_PATH,
            'ERA5_L137_model_level_definitions.csv'
        )
    level_definitions = pd.read_csv(filename, index_col=0)
    a = np.array(level_definitions['a [Pa]'])
    b = np.array(level_definitions['b'])
    return a, b


def calculate_level_heights(temperature, pressure, which='middle'):
    """
    temperature at middle of layers
    pressure at boundary of layers
    """
    g = 9.80665
    R = 287.06

    p1 = pressure[1:]
    p2 = pressure[:-1]

    dh = R * temperature / g * np.log(p1 / p2)

    hh = np.concatenate([[0.0], dh[::-1].cumsum()])
    hh = hh[::-1]

    hf = 0.5 * (hh[1:] + hh[:-1])

    if which == 'middle':
        return hf
    elif which == 'boundary':
        return hh
    else:
        raise ValueError