
from datetime import timedelta
import os
import netCDF4
import numpy as np
import pandas
import pyproj
import scipy.ndimage
import skimage.draw
import skimage.morphology
import xarray as xr

import f90nml
import cartopy.crs as ccrs
from cartopy.geodesic import Geodesic

# Instance of Geodesic class for working in lon-lat coordinates
EARTH = Geodesic()

import ddeq

class Results(dict):

    def to_file(self, filename):
        for i, (group, data) in enumerate(self.items()):
            mode = 'w' if i == 0 else 'a'
            data.to_netcdf(filename, mode=mode, group=group)

    @classmethod
    def from_file(cls, filename, groups=None):
        """
        Read results from netCDF file.
        """
        if groups is None:
            with netCDF4.Dataset(filename) as nc:
                groups = nc.groups.keys()

        results = dict(
            (group, xr.open_dataset(filename, group=group).load())
            for group in groups
        )
        return cls(results)


def init_results_dataset(source, gases, extra_vars=(), units='kg s-1',
                         method=''):
    """
    Initialize dataset for estimated emissions.
    """
    result = xr.Dataset(source, attrs={'method': method})
    attrs = {'units': units}
    for gas in gases:
        for name, units in extra_vars:
            nan_values = np.full(np.shape(source.source), np.nan)
            result[name.format(gas=gas)] = xr.DataArray(nan_values,
                                                        dims=source.dims,
                                                        attrs={'units': units})
        name = f'{gas}_estimated_emissions'
        name_std = f'{gas}_estimated_emissions_precision'
        result[name] = xr.DataArray(np.full(source['source'].size,np.nan), dims=['source'], attrs=attrs)
        result[name_std] = xr.DataArray(np.full(source['source'].size,np.nan), dims=['source'], attrs=attrs)
    return result


def select_source(data, source):
    """
    Select source in data but also compute new fields for other plumes and multiple sources.
    """
    this = data.sel(source=source).copy()
    this['other_sources'] = data['detected_plume'].any('source') & ~this['detected_plume']
    this['multiple_sources'] = data['detected_plume'].sum('source') > 1
    
    return this



class Domain:
    def __init__(self, name, startlon, startlat, stoplon, stoplat,
                 ie=None, je=None, pollon=None, pollat=None):
        """
        to add: dlon, dlat, ie, je
        """
        self.name = name

        self.startlat = float(startlat)
        self.stoplat = float(stoplat)
        self.startlon = float(startlon)
        self.stoplon = float(stoplon)

        self.ie = ie
        self.je = je

        self.rlon = None
        self.rlat = None
        self.lon = None
        self.lat = None

        self.width = np.abs(self.stoplon - self.startlon)
        self.height = np.abs(self.stoplat - self.startlat)

        self.pollon = pollon
        self.pollat = pollat

        self.is_rotpole =  pollon is not None and pollat is not None
        is_grid = self.ie is not None and self.je is not None

        if is_grid:
            self.dlon = (self.stoplon - self.startlon) / (self.ie - 1)
            self.dlat = (self.stoplat - self.startlat) / (self.je - 1)
        else:
            self.dlon, self.dlat = None, None


        if self.is_rotpole:
            self.proj = ccrs.RotatedPole(pole_latitude=pollat,
                                         pole_longitude=pollon)

            if is_grid:
                self.rlon = np.linspace(self.startlon, self.stoplon, self.ie)
                self.rlat = np.linspace(self.startlat, self.stoplat, self.je)

                rlon, rlat = np.meshgrid(self.rlon, self.rlat)

                self.lon, self.lat = transform_coords(rlon, rlat, self.proj,
                                                      ccrs.PlateCarree(),
                                                      use_xarray=False)
        else:
            self.proj = ccrs.PlateCarree()

            if is_grid:
                self.lon = np.linspace(self.startlon, self.stoplon, self.ie)
                self.lat = np.linspace(self.startlat, self.stoplat, self.je)


    @property
    def shape(self):
        return self.je, self.ie


    @classmethod
    def from_nml(cls, filename):
        with open(filename) as nml_file:
            nml = f90nml.read(nml_file)

        pollon = nml['lmgrid']['pollon']
        pollat = nml['lmgrid']['pollat']
        startlon = nml['lmgrid']['startlon_tot']
        startlat = nml['lmgrid']['startlat_tot']
        dlon = nml['lmgrid']['dlon']
        dlat = nml['lmgrid']['dlat']
        ie = nml['lmgrid']['ie_tot']
        je = nml['lmgrid']['je_tot']

        stoplat = startlat + (je-1) * dlat
        stoplon = startlon + (ie-1) * dlon

        return cls(filename, startlon, startlat, stoplon, stoplat,
                   ie, je, pollon, pollat)
    
    
    def get_transform(self):
        import rasterio.transform
        
        return rasterio.transform.from_bounds(
            self.startlon, self.startlat,
            self.stoplon, self.stoplat,
            self.ie, self.je
        )



    
    
def kgs_to_Mtyr(x, inverse=False):
    """ Convert kg/s to Mt/yr. """
    SECONDS_PER_YEAR = 31557600.0 # with 365.25 days
    factor = 1e9 / SECONDS_PER_YEAR
    if inverse:
        return x * factor
    else:
        return x / factor




def read_point_sources(filename=None):
    """\
    Read list of point sources and converts them to format used by the
    plume detection algorithm.

    Parameters
    ----------
    filename : str, default: None
        Name of CSV file with point source information (see "sources.csv"
        in ddeq.DATA_PATH for an example).

    Returns
    -------
    xr.Dataset
        xarray dataset containing point source locations
    """
    if filename is None:
        filename = os.path.join(os.path.dirname(__file__), 'data',
                                'sources.csv')

    point_sources = pandas.read_csv(filename, index_col=0,
                              names=['label', 'longitude', 'latitude', 'type'],
                              header=0)

    sources = xr.Dataset(coords={'source': point_sources.index})
    sources['lon_o'] = xr.DataArray(point_sources['longitude'], dims='source',
                                        attrs={'name': 'longitude of point source'})
    sources['lat_o'] = xr.DataArray(point_sources['latitude'], dims='source',
                                        attrs={'name': 'latitude of point source'})
    sources['type'] = xr.DataArray(point_sources['type'], dims='source',
                                       attrs={'name': 'type of point source'})

    sources['label'] = xr.DataArray(point_sources['label'], dims='source')

    # size of point sources (used for finding overlap of detected plumes)
    sources['radius'] = xr.DataArray(
        np.where(point_sources['type'] == 'city', 15.0, 5.0),
        attrs={'name': 'Radius of point source around location', 'units': 'km'},
        dims='source')

    return sources


def get_source_location(source):
    """ Returns (lon, lat) tuple of source location """
    return float(source.lon_o), float(source.lat_o)



def transform_coords(x, y, input_crs, output_crs, use_xarray=True, names=('x', 'y')):
    """
    Convert easting and northing in EPSG to WGS84.
    """
    if use_xarray:
        dims = x.dims
        
    x = np.asarray(x)
    y = np.asarray(y)
    shape = x.shape
        
    res = output_crs.transform_points(input_crs, x.flatten(), y.flatten())
    xnew, ynew = res[:,0].reshape(shape), res[:,1].reshape(shape)
    
    if use_xarray:
        xnew = xr.DataArray(xnew, name=names[0], dims=dims)
        ynew = xr.DataArray(ynew, name=names[1], dims=dims)
        
    return xnew, ynew
    

    if np.ndim(x) == 0:
        res = output_crs.transform_point(lon, lat, input_crs)
        xnew, ynew = res[0], res[1]
        
    elif np.ndim(x) in [1,2]:
        res = out.transform_points(in_, lon, lat)
        xnew, ynew = res[...,0], res[...,1]
        
    else:
        shape = x.shape
        res = output_crs.transform_points(input_crs, x.flatten(), y.flatten())
        x, y = x[:,0].reshape(shape), y[:,1].reshape(shape)
        
        
        


def wgs2epsg(lon, lat, epsg, inverse=False):
    """
    Transforms lon/lat to EPSG.
    """
    if inverse:
        out = ccrs.PlateCarree()
        in_ = ccrs.epsg(epsg)
    else:
        out = ccrs.epsg(epsg)
        in_ = ccrs.PlateCarree()

    if np.ndim(lon) == 0:
        res = out.transform_point(lon, lat, in_)
        return res[0], res[1]
    elif np.ndim(lon) in [1,2]:
        res = out.transform_points(in_, lon, lat)
        return res[...,0], res[...,1]
    else:
        shape = lon.shape
        res = out.transform_points(in_, lon.flatten(), lat.flatten())
        return res[:,0].reshape(shape), res[:,1].reshape(shape)
    
    
def has_multiple_sources(data, source):
    """
    Returns if the plume detected for "source" has also added to other
    sources in the dataset.
    """
    return bool(np.any(data['detected_plume'].sel(source=source) &
                       (data['detected_plume'].sum('source') > 1)))


def get_source_clusters(data, sources):
    """\
    Return a list of list source names that have overlapping plumes.
    """ 
    plumes = data['detected_plume']

    sources_names = plumes.source.values
    names = []
    cluster = []

    for name in sources_names:
        current = plumes.sel(source=name)
        twins = []

        if name in names:
            continue

        for name in sources_names:
            if np.all(current == plumes.sel(source=name)):
                names.append(name)
                twins.append(name)

        cluster.append(twins)

    return cluster


def compute_plume_area(data, crs, radius=25e3, pixel_size=2e3):
    """
    distance in meters, source used to draw circle around
    """
    n = int(radius // (0.5 * pixel_size) + 1)
    r = int(radius // pixel_size + 1) 
    
    shape = (n, n)
    kernel = np.zeros(shape, dtype=bool)

    rr,cc = skimage.draw.disk((r-1,r-1),r)
    kernel[rr,cc] = True

    # set pixels within distance from detected pixels to True
    detected_plume = np.array(data['detected_plume'])
    area = skimage.morphology.dilation(detected_plume, kernel)

    # set area 50 km around source to True
    x_o = float(data['x_o'])
    y_o = float(data['y_o'])

    area[ np.sqrt((data.x - x_o)**2 + (data.y - y_o)**2) < radius] = True
    
    return area


def cubic_equation(a,b,c,d):
    """
    Find roots of cubic polynomial:
        a * x**3 + b * x**2 + c * x + d = 0
    """
    try:
        dtype = np.complex256
    except AttributeError:
        dtype = np.complex128
    a = np.asarray(a).astype(dtype)
    b = np.asarray(b).astype(dtype)
    c = np.asarray(c).astype(dtype)
    d = np.asarray(d).astype(dtype)

    d0 = b**2 - 3 * a * c
    d1 = 2 * b**3 - 9 * a * b * c + 27 * a**2 * d

    C = ((d1 + np.sqrt(d1**2 - 4 * d0**3)) / 2.0)**(1/3)

    xi = (-1.0 + np.sqrt(-3.0 + 0j)) / 2.0
    s = lambda k: xi**k * C

    roots = [-1.0/ (3.0 * a) * (b + s(k) + d0 / s(k)) for k in range(3)]

    return np.array(roots)


def get_plume_width(data, dy=5e3, area='detected_plume'):

    # distance from center line
    if isinstance(area, str):
        yp = data['yp'].values[data[area]]
    else:
        yp = data['yp'].values[area]

    ymin = np.floor((yp.min() - 2 * dy) / dy) * dy
    ymax = np.ceil((yp.max() + 2 * dy) / dy) * dy

    return ymin, ymax


def compute_polygons(data, source_type='point', dmin=None, dmax=np.inf, delta=None,
                     add_upstream_box=None, extra_width=1, pixel_size=None):
    """
    Compute [xa,xb] and [ya,yb] intervals for polygons.
    """
    if pixel_size is None:
        raise ValueError('Pixel size is None.')

    if source_type in ['point', 'power plant', 'steel plant']:
        dmin = 0.0 if dmin is None else dmin
        delta = 2.5 * pixel_size if delta is None else delta
        add_upstream_box = True if add_upstream_box is None else add_upstream_box

    elif source_type == 'city':
        dmin = -25e3 if dmin is None else dmin
        delta = 5.0 * pixel_size if delta is None else delta
        add_upstream_box = False if add_upstream_box else add_upstream_box

    else:
        raise ValueError(f'Source type {source_type} not in [point, power plant, city].')

    dmax = min(dmax, np.nanmax(data.xp.values[data.detected_plume]))
    distances = np.arange(dmin, dmax+delta, delta)

    if add_upstream_box: # FIXME
        xa_values = np.concatenate([[-12e3], distances[:-1]])
        xb_values = np.concatenate([[-2e3], distances[1:]])
    else:
        xa_values = distances[:-1]
        xb_values = distances[1:]

    ya, yb = get_plume_width(data, dy=extra_width * pixel_size)

    return xa_values, xb_values, np.full_like(xa_values, ya), \
           np.full_like(xb_values, yb)



def normalized_convolution(values, kernel, mask=None):

    if mask is None:
        mask = ~np.isfinite(values)

    values = values.copy()
    certainty = 1.0 - mask

    values[certainty == 0.0] = 0.0

    return scipy.ndimage.convolve(values, kernel) / scipy.ndimage.convolve(certainty, kernel)



def compute_plume_age_and_length(ld):
    """
    Estimate plume age and length based on wind speed and arc length of
    detected pixels.
    """
    values = ld.x.values[ld.is_plume.values]

    if np.size(values) > 0:
        plume_length = ld.x.values[ld.is_plume.values].max() / 1e3
    else:
        plume_length = 0.0

    plume_age = plume_length / np.mean(ld['wind_speed'] * 3600 / 1000)

    return plume_age, plume_length



def compute_angle_between_curve_and_wind(curve, wind_direction, crs=None):
    """
    Compute the angle between wind vector and curve tangent, which can be
    used as a warning flag for large misfits.

    Parameter: 
    - source: name of point source
    - curves: dict with curves
    """
    if crs is None:
        crs = curve.crs

    # compute curve angle (lon-lat angle)
    u, v = curve.compute_tangent(curve.t_o)

    u, v = transform_coords(
        np.array([curve.x_o, curve.x_o - u]),
        np.array([curve.y_o, curve.y_o - v]),
        crs, ccrs.PlateCarree(), use_xarray=False
    )
    u = np.diff(u)
    v = np.diff(v)

    curve_angle = float( np.rad2deg(np.arctan2(u,v)) )

    return smallest_angle(wind_direction, curve_angle)


def smallest_angle(x,y):
    return min(abs(x - y), 360 - abs(x - y))


def generate_grids(center_lon, center_lat, lon_km, lat_km, grid_reso):
    """
    Generate the km and degree grids corresponding resolution grid_reso in km.
    """
    longrid_km = np.arange(-lon_km, lon_km+grid_reso, grid_reso)
    latgrid_km = np.arange(-lat_km, lat_km+grid_reso, grid_reso)[::-1]

    shape = latgrid_km.size, longrid_km.size

    lat_arr = np.asarray(EARTH.direct(
        np.repeat([(center_lon, center_lat)], shape[0], axis=0),
        np.zeros(shape[0]),1000*latgrid_km)
    )[:,1]

    latgrid = np.repeat(np.reshape(lat_arr, (-1, 1)), shape[1], axis=1)
    longrid = np.full(shape, np.nan)

    for r in range(shape[0]):
        longrid[r,:] = np.asarray(EARTH.direct(
            np.repeat([(center_lon,lat_arr[r])],shape[0],axis=0),
            90*np.ones(shape[0]),1000*longrid_km)
        )[:,0]

    return longrid, latgrid, longrid_km, latgrid_km


def calculate_gaussian_curve(gas, polygon):
    """
    Calculate Gaussian curve from fit parameters for Gaussian curve in
    cross-sectional flux method.
    """
    s = np.linspace(polygon['ya'], polygon['yb'], 501)
    p = [
        float(polygon[name]) for name in  [f'{gas}_line_density',
                                           f'{gas}_standard_width',
                                           f'{gas}_shift',
                                           f'{gas}_slope',
                                           f'{gas}_intercept']
    ]
    return s, ddeq.functions.gauss(s, *p)


def find_closest(data, fld, poi):
    """
    Get the index of the pixel closest to the point of interest.

    Parameters:
    ----------
    data: netCDF
        File with the coordinates to find
    fld: (str, str)
        Tuple of strings with the names of the coordinates in data (i.e 'lon', 'lat')
    poi: (float, float)
        Tuple of floats with the coordinates of the point of interest

    Returns:
    --------
    ind: (int, int)
        Indexes of the pixel closest to the point of interest.
    dist: float
        Distance of the closest pixel to the point of interest.
        In the units of the input data.
    """
    xf, yf = fld
    x, y = poi
    diff = np.sqrt((data[xf].values - x)**2 + \
                   (data[yf].values - y)**2)

    return (*np.unravel_index(np.nanargmin(diff), diff.shape), np.nanmin(diff))



def cluster_sources(sources, distance):
    """
    Cluster sources based on `distance` in meters following the example at [1].


    [1] https://geoffboeing.com/2014/08/clustering-to-reduce-spatial-data-set-size/
    """
    # TODO
    pass


def get_opt_crs(domain):
    """
    Get a coordinate reference system (crs) based on the extent of the domain.

    Parameters
    ----------
    domain : ddeq.misc.Domain
        Domain class used to define plotting area.

    Returns
    -------
    cartopy.crs.CRS
    """
    # Define the area of interest
    area_of_interest = pyproj.aoi.AreaOfInterest(
        west_lon_degree = domain.startlon,
        south_lat_degree = domain.startlat,
        east_lon_degree = domain.stoplon,
        north_lat_degree = domain.stoplat)

    # query all crs which intersect with the domain
    utm_crs_list = pyproj.database.query_utm_crs_info(
        datum_name = "WGS 84",
        area_of_interest = area_of_interest)

    df = pandas.DataFrame(utm_crs_list)

    return ccrs.epsg(int(df.iloc[0]["code"]))