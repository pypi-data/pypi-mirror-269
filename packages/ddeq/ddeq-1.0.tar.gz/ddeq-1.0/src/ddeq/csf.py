
import numbers
import warnings

import numpy as np
import pandas as pd
import scipy.ndimage
import scipy.optimize
import xarray as xr

import ddeq


def expand_dimension(data, dim, size):
    """\
    Increase `size` of dimension `dim` in `data` (xarray.Dataset).
    """
    coords = {}
    for key in data.dims:
        if key == dim:
            coords[key] = np.arange(size)
        else:
            coords[key] = data[key]

    new = xr.Dataset(coords=coords, attrs=data.attrs)

    for key in data:
        var = data[key]

        if dim in var.dims:
            fill_value = False if var.dtype == bool else np.nan
            values = np.concatenate([
                var.values,
                np.full(size-var[dim].size, fill_value, dtype=var.dtype)
            ])
        else:
            values = data[key].values

        new[key] = xr.DataArray(values, dims=var.dims, attrs=var.attrs)

    return new



def concat_polygons(polygons):
    """\
    Concatenate results from sub-polygons in single xr.Dataset.
    """
    size = max(p['pixels'].size for p in polygons)
    values = [expand_dimension(p, 'pixels', size) for p in polygons]
    return xr.concat(values, dim='along')


def sort_and_remove_nans(y, c, c_std):
    """\
    Sort arrays `c` and `c_std` using `y` and remove non-finite values.
    """
    sort = np.argsort(y)
    y = y[sort]
    c = c[sort]
    c_std = c_std[sort]

    valids = np.isfinite(y) & np.isfinite(c)

    return y[valids], c[valids], c_std[valids]


def prepare_gauss_models(gases, pixel_size, share_mu=True, share_sigma=True,
                         background=None):
    """\
    Prepare functions for main and aux Gaussian curve for given gases. In
    addition, also provide starting vector p0 and bounds for the models.
    """
    # start values
    line_density_0 = {
        'CO2': 100.0,
        'NO2': 0.1,
    }
    line_density_bounds = [0, np.inf]

    sigma_0 = 5 * pixel_size
    sigma_bounds = [0.5 * pixel_size, 50 * pixel_size]

    mu_0 = 0.0
    mu_bounds = [-10 * pixel_size, +10 * pixel_size]

    slope_0 = 0.0
    slope_bounds = [-np.inf, +np.inf]

    intercept_0 = 0.0
    intercept_bounds = [-np.inf, +np.inf]

    # define main and aux Gaussian curve with/without linear background
    # and sharing mu and sigma between curves
    p0 = [line_density_0.get(gases[0], 1.0), sigma_0, mu_0]
    bounds = [line_density_bounds, sigma_bounds, mu_bounds]

    # build mapping to parameter vector from line density (ld),
    # standard witdh (sd), center shift (mu), slope (m) and intercept (b)
    # for each gas
    mapping = dict((gas, {}) for gas in gases)
    mapping[gases[0]]['ld'] = 0
    mapping[gases[0]]['sd'] = 1
    mapping[gases[0]]['mu'] = 2

    if background is None:
        # x, q, sigma, shift, slope, offset
        curve = lambda x, *p: ddeq.functions.gauss(
            x, p[0], p[1], p[2]
        )
    else:
        curve = lambda x, *p: ddeq.functions.gauss(
            x, p[0], p[1], p[2], p[3], p[4]
        )
        p0 += [slope_0, intercept_0]
        bounds += [slope_bounds, intercept_bounds]

        mapping[gases[0]]['m'] = 3
        mapping[gases[0]]['b'] = 4

    if len(gases) == 2:
        p0 += [line_density_0.get(gases[1], 1.0)]
        bounds += [line_density_bounds]

        if background is None:
            if share_sigma and share_mu:
                aux_curve = lambda x, *p: ddeq.functions.gauss(
                    x, p[3], p[1], p[2]
                )
                mapping[gases[1]]['ld'] = 3
                mapping[gases[1]]['sd'] = 1
                mapping[gases[1]]['mu'] = 2
                mapping[gases[1]]['m'] = None
                mapping[gases[1]]['b'] = None

            elif share_sigma:
                aux_curve = lambda x, *p: ddeq.functions.gauss(
                    x, p[3], p[1], p[4]
                )
                p0 += [mu_0]
                bounds += [mu_bounds]

                mapping[gases[1]]['ld'] = 3
                mapping[gases[1]]['sd'] = 1
                mapping[gases[1]]['mu'] = 4

            elif share_mu:
                aux_curve = lambda x, *p: ddeq.functions.gauss(
                    x, p[3], p[4], p[2]
                )
                p0 += [sigma_0]
                bounds += [sigma_bounds]

                mapping[gases[1]]['ld'] = 3
                mapping[gases[1]]['sd'] = 4
                mapping[gases[1]]['mu'] = 2
            else:
                aux_curve = lambda x, *p: ddeq.functions.gauss(
                    x, p[3], p[4], p[5]
                )
                p0 += [sigma_0, mu_0]
                bounds += [sigma_bounds, mu_bounds]

                mapping[gases[1]]['ld'] = 3
                mapping[gases[1]]['sd'] = 4
                mapping[gases[1]]['mu'] = 5
        else:
            if share_sigma and share_mu:
                aux_curve = lambda x, *p: ddeq.functions.gauss(
                    x, p[3], p[1], p[2], p[4], p[5]
                )
                mapping[gases[1]]['ld'] = 3
                mapping[gases[1]]['sd'] = 1
                mapping[gases[1]]['mu'] = 2
                mapping[gases[1]]['m'] = 4
                mapping[gases[1]]['b'] = 5

            elif share_sigma:
                aux_curve = lambda x, *p: ddeq.functions.gauss(
                    x, p[3], p[1], p[4], p[5], p[6]
                )
                p0 += [mu_0]
                bounds += [mu_bounds]

                mapping[gases[1]]['ld'] = 3
                mapping[gases[1]]['sd'] = 1
                mapping[gases[1]]['mu'] = 4
                mapping[gases[1]]['m'] = 5
                mapping[gases[1]]['b'] = 6

            elif share_mu:
                aux_curve = lambda x, *p: ddeq.functions.gauss(
                    x, p[3], p[4], p[2], p[5], p[6]
                )
                p0 += [sigma_0]
                bounds += [sigma_bounds]

                mapping[gases[1]]['ld'] = 3
                mapping[gases[1]]['sd'] = 4
                mapping[gases[1]]['mu'] = 2
                mapping[gases[1]]['m'] = 5
                mapping[gases[1]]['b'] = 6

            else:
                aux_curve = lambda x, *p: ddeq.functions.gauss(
                    x, p[3], p[4], p[5], p[6], p[7]
                )
                p0 += [sigma_0, mu_0]
                bounds += [sigma_bounds, mu_bounds]

                mapping[gases[1]]['ld'] = 3
                mapping[gases[1]]['sd'] = 4
                mapping[gases[1]]['mu'] = 5
                mapping[gases[1]]['m'] = 6
                mapping[gases[1]]['b'] = 7

            # add background
            p0 += [slope_0, intercept_0]
            bounds += [slope_bounds, intercept_bounds]

    else:
        aux_curve = None


    return curve, aux_curve, np.array(p0), list(zip(*bounds)), mapping



def fit_gauss_curve(polygon, gases, pixel_size, share_mu=True, share_sigma=True,
                    background=None):
    """\
    Fit one/two Gaussian curves to gas columns in a polygon.


    Parameter
    =========
    polygon (xr.Dataset)
        dataset created by `ddeq.csf.extract_pixels function` containing all
        relevant values within a polygon given by along- and across-plume
        intervals.

    gases (list of strings)
        A list of one or two strings naming the gas columns in the polygon.

    share_mu (default: True)
        If true Gaussian curves share center positions.

    share_sigma (default: True)
        If true Gaussian curves share standard width.

    background (default: None)
        If "linear" fit linear background (i.e. mx + b).

    pixel_size (default: 1e3)
        Pixel size of the image determines suitable starting vector assume
        that the plume is resolved by the imager.
    """
    func, aux_func, p0, bounds, mapping = prepare_gauss_models(
        gases,
        pixel_size=pixel_size,
        share_mu=share_mu,
        share_sigma=share_sigma,
        background=background,
    )

    # data for fitting
    values = [
        sort_and_remove_nans(polygon['y'], polygon[gas], polygon[f'{gas}_std'])
        for gas in gases
    ]
    y, c, c_std = np.concatenate(values, axis=1)

    # combine func and aux_func
    if aux_func is not None:
        y1 = values[0][0]
        y2 = values[1][0]
        function = lambda x, *p: np.concatenate([func(y1, *p), aux_func(y2, *p)])
    else:
        function = func

    if y.size < p0.size:
        p = np.full_like(p0, np.nan)
        cov_p = np.full((p0.size, p0.size), np.nan)
        sigma = None

    else:
        if np.all(np.isnan(c_std)):
            sigma = None
        elif np.any(np.isnan(c_std)):
            raise ValueError
        else:
            sigma = c_std

        warnings.simplefilter("error", scipy.optimize.OptimizeWarning)
        try:
            p, cov_p = scipy.optimize.curve_fit(
                function, y, c, p0, sigma=sigma, bounds=bounds,
                absolute_sigma=sigma is not None)

        except (scipy.optimize.OptimizeWarning, RuntimeError):
            p = np.full_like(p0, np.nan)
            cov_p = np.full((p0.size, p0.size), np.nan)

    p_std = np.sqrt(cov_p.diagonal())

    short2long_name = {
        'ld': 'line_density',
        'sd': 'standard_width',
        'mu': 'shift',
        'm': 'slope',
        'b': 'intercept'
    }
    short2units = {
        'ld': 'kg m-1',
        'sd': 'm',
        'mu': 'm',
        'm': 'kg m-3',
        'b': 'kg m-2'
    }
    for i, gas in enumerate(gases):

        for parameter in ['ld', 'sd', 'mu', 'm', 'b']:

            index = mapping[gas].get(parameter)

            if index is None:
                value = np.nan
                value_std = np.nan
            else:
                value = p[index]
                value_std = np.nan if sigma is None else p_std[index]

            name = short2long_name[parameter]
            units = short2units[parameter]
            polygon[f'{gas}_{name}'] = value
            polygon[f'{gas}_{name}'].attrs['units'] = units
            polygon[f'{gas}_{name}_precision'] = value_std
            polygon[f'{gas}_{name}_precision'].attrs['units'] = units

    return polygon


def get_values_from_areas(values, sub_areas):
    """\
    Get items in `values' for each boolean mask given by `sub_areas`.
    """
    return np.array(
        [values[a.values] if np.any(a) else np.array([]) for a in sub_areas],
        dtype='object'
    )


def extract_pixels(data, gas, variable, xa, xb, ya, yb, dy=None):
    """
    Extract pixels within a polygon given by plume coords for along-plume
    direction [xa,xb] and across-plume direction [ya,yb] (units: meters).

    Parameter
    =========
    data (xr.Dataset)
        Dataset of remote sensing data.

    gas (string)
        Name of gas in `data` (e.g., CO2 or NO2).

    variable (string)
        Name of varible with the gas columns. The random uncertainty of the
        variable is taken from data[varible].attrs['noise_level'].

    xa, xb (number)
        Interval for along-plume distance [xa,xb] in meters.

    ya, yb (number)
        Interval for across-plume distance [xa,xb] in meters.

    dy (number in meters)
        distance to additional divide polygon in sub-polygons in across-plume
        direction (used by sub-area method).

    """
    polygon = xr.Dataset()

    # only use pixels that are valid observations
    xp = data['xp'].values
    yp = data['yp'].values

    area = (xa <= xp) & (xp < xb) & (ya <= yp) & (yp <= yb)

    polygon['polygon_mask'] = xr.DataArray(area, dims=data.xp.dims)
    polygon['xa'] = xa
    polygon['xb'] = xb
    polygon['ya'] = ya
    polygon['yb'] = yb

    isfinite = data[f'{gas}_isfinite'].values[area]

    if 'other_sources' in data and np.any(data['other_sources'].values[area]):
        isfinite[data['other_sources'].values[area]] = False

    # pixel in area
    polygon['x'] = xr.DataArray(data.xp.values[area], name='x',
                                    dims='pixels')
    polygon['y'] = xr.DataArray(data.yp.values[area], name='y',
                                    dims='pixels')

    c = data[variable].values[area]
    c[~isfinite] = np.nan
    p = data['detected_plume'].values[area]

    polygon[gas] = xr.DataArray(c, dims='pixels')
    polygon['is_plume'] = xr.DataArray(p, dims='pixels')

    # estimate noise
    noise_level = data[variable].attrs['noise_level']

    c_std = np.full(np.shape(c), noise_level)
    polygon[f'{gas}_std'] = xr.DataArray(c_std, dims='pixels')

    polygon['subpolygons'] = xr.DataArray(
        np.arange(ya + 0.5 * dy, yb, dy), dims='subpolygons'
    )

    sub_areas = [(y0 - 0.5 * dy <= polygon['y']) &
                 (polygon['y'] < y0 + 0.5 * dy)
                 for y0 in polygon['subpolygons']]

    xx = get_values_from_areas(polygon['x'], sub_areas)
    yy = get_values_from_areas(polygon['y'], sub_areas)

    c = get_values_from_areas(polygon[gas], sub_areas)
    c_std = get_values_from_areas(polygon[f'{gas}_std'], sub_areas)

    for name in ['x', 'y', gas, f'{gas}_std', 'is_plume']:

        if name == 'is_plume':
            function = np.sum
        elif name == '%s_std' % name:
            function = standard_error_of_the_mean
        else:
            function = np.nanmean

        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', r'Mean of empty slice')
            values = [function(v) for v in
                      get_values_from_areas(polygon[name].values, sub_areas)]

        polygon[f'{name}_sub'] = xr.DataArray(values, dims='subpolygons')

    return polygon



def compute_line_density(data, gases, variable, xa, xb, ya=None, yb=None,
                         dy=5e3, method='gauss', pixel_size=None, share_mu=True,
                         share_sigma=True, background=None, extra_width=5e3):
    """\ TODO
    Compute the line densitiy of trace gases in data within polygon given by
    along-plume interval [xa, xb] and across-plume interval [ya, yb]. If ya or
    yb is None estimate plume width from detected pixels. The plume center line
    is described by the `curve`.

    The function uses two methods:
    - gauss: fitting a Gaussian curve
    - sub-areas: sum mean values in sub-areas in across-plume direction using
                 sub-areas with width `dy`

    Parameter
    =========
    data
    
    gases
    
    variable
    
    xa, xb
    
    ya, yb
    
    dy
    
    method ('gauss' or 'sub-areas') (default: 'gauss')
        Method used for computing line densities:
        - 'gauss': fit one or two Gaussian curves to gas columns in polygon.
        - 'sub-areas': divide polygon in sub-areas in across-plume direction,
          compute the mean value in each sub-polygon and sum all mean values to
          obtain line density.
    
    share_mu, share_sigma
        If two gases, share center position (mu) and standard width (sigma)
        
    background
    
    extra_width
    """
    if ya is None or yb is None:
        ya, yb = ddeq.misc.get_plume_width(data, dy=extra_width)
    else:
        ya = ya[0]
        yb = yb[0]

    # extract pixels in area
    polygon = xr.Dataset()
    polygon['method'] = method
    polygon['along'] = xr.DataArray(0.5 * (xa + xb))

    for gas in gases:
        polygon.update(
            extract_pixels(data, gas, variable.format(gas=gas),
                           xa, xb, ya, yb, dy=dy)
        )

        # add nans for results
        for name in ['line_density', 'standard_width', 'shift', 'slope',
                     'intercept']:
            polygon[f'{gas}_{name}'] = np.nan
            polygon[f'{gas}_{name}_precision'] = np.nan

    if method == 'gauss':
        # Only fit line density if valid observation for detected plume, e.g.,
        # if NO2 is used for plume detection, CO2 might not have valid values.
        if np.any((polygon['is_plume_sub'] > 0)
                  & np.isnan(polygon[f'{gas}_sub'])):

            polygon[f'{gas}_line_density'] = np.nan
        else:
            polygon = fit_gauss_curve(polygon, gases,
                                      pixel_size=pixel_size,
                                      share_mu=share_mu,
                                      share_sigma=share_sigma,
                                      background=background,
                                     )
    elif method in ['sub-areas']:
        for gas in gases:

            if not (np.any((polygon['is_plume_sub'] > 0) \
                      & np.isnan(polygon[f'{gas}_sub']))):

                valids = np.isfinite(polygon[f'{gas}_sub'].values)

                ss = polygon['subpolygons'].values
                area_means = polygon[f'{gas}_sub'].values
                area_means_std = polygon[f'{gas}_std_sub'].values

                if np.all(~valids):
                    area_means[:] = np.nan
                else:
                    area_means = np.interp(ss, ss[valids], area_means[valids],
                                           left=0.0, right=0.0)

                polygon[f'{gas}_line_density'] = np.sum(area_means * dy)

                # FIXME
                n = np.sum(valids)
                polygon[f'{gas}_line_density_precision'] = np.sqrt(
                    np.nansum(area_means_std**2 * dy**2)
                ) / np.sqrt(n)

    else:
        raise ValueError


    return polygon


    # TODO/FIXME: should still do some filtering here, but need smarter
    # default values

    # x_sub and y_sub have only nans if no pixels are inside subpolygon,
    # i.e. sub-polygon is not in swath
    not_fully_in_swath = np.any(np.isnan(polygon['x_sub']))

    # only use fits with at least one observation per sub-polygon, 
    # if pixels have been detected
    for gas in gases:
        if not_fully_in_swath or (np.any((polygon['is_plume_sub'] > 0)
                                  & np.isnan(polygon[f'{gas}_sub']))):

            polygon[f'{gas}_line_density'] = np.nan
            polygon[f'{gas}_line_density_precision'] = np.nan

        # set unrealistic low/high values to nan / TODO: dehardcode
        if (
            polygon[f'{gas}_line_density'] < -1000.0
            or polygon[f'{gas}_line_density'] > 1000.0
            or polygon[f'{gas}_line_density_precision'] > 1000.0
        ):
            polygon[f'{gas}_line_density'] = np.nan
            polygon[f'{gas}_line_density_precision'] = np.nan

    return polygon


def fit_emissions(xvalues, flux, flux_std=None,
                  model='point_source', decay_term='none',
                  dmin_fit=10e3, dmax_fit=np.inf, absolute_sigma=True):
    """
    Estimate `gas` emissions from fluxes by fitting an exponential decay
    function.
    """
    parameter = ['Q']

    # check valid values
    valids = np.isfinite(flux) & (xvalues < dmax_fit) & (xvalues > dmin_fit)

    if flux_std is None or np.all(np.isnan(flux_std)) \
       or np.all(flux_std == 0.0):
        sigma = None
    else:
        valids = valids & (flux_std > 0)
        sigma = flux_std[valids]

    if sigma is not None and np.any(np.isnan(sigma)):
        sigma = None

    # starting vector
    if model == 'point_source':
        model_function = ddeq.functions.point_plume_model
        p0 = [max(0.0, np.nanmedian(flux))]
        bounds = [(0, np.inf)]

    elif model == 'area_source':
        model_function = ddeq.functions.city_plume_model
        p0 = [
            max(0.0, np.nanmedian(flux)),  # flux (in kg/s)
            10e3,                          # standard width of city (in m)
        ]
        bounds = [
            (0.0, np.inf), # flux bounds (no negative emissions)
            (0.0, np.inf), # width bounds
        ]
        parameter.append('W')

    if decay_term == 'exp':
        p0 += [100e3] # decay distance: x0 = wind_speed * decay_time
        bounds += [(0.0, 432e3)] # 24 hours (TODO)
        parameter.append('D')

    # TODO: add logging message
    if np.sum(valids) < len(p0):
        p = np.full_like(p0, np.nan)
        p_std = np.full_like(p0, np.nan)
    else:
        try:
            p, cov_p = scipy.optimize.curve_fit(model_function, xvalues[valids],
                                                flux[valids], p0=p0,
                                                bounds=np.transpose(bounds),
                                                sigma=sigma,
                                                absolute_sigma=absolute_sigma
                                               )
            # estimate uncertainty assuming a good fit
            p_std = np.sqrt(np.diag(cov_p))

        except RuntimeError as e:
            p = np.full_like(p0, np.nan)
            p_std = np.full_like(p0, np.nan)

        except scipy.optimize.OptimizeWarning as e:
            p = np.full_like(p0, np.nan)
            p_std = np.full_like(p0, np.nan)

    x = np.linspace(xvalues[0], xvalues[-1], 100)

    return p, p_std, parameter, x, model_function(x, *p)




def fit_along_plume_fluxes(gas, line_densities, model='point_source', 
                           decay_term='none'):
    """\
    Fit a model that describes the gas flux in along-plume direction.

    Compute emissions (q in kg/s) and for NO2 decay times (tau in hours) as
    well as their uncertainties.

    gas                CO2 or NO2
    line_densities     line densities
    model              "point_source" or "area_source" for sources small or
                       larger than a satellite pixel (e.g. power plants and
                       cities)
    decay_term         adds a decay term if "exp" (otherwise flux should be
                       constant in along-plume direction)
    """
    # compute flux and uncertainty (not including wind_std yet)
    wind = line_densities['wind_speed'].values
    wind_std = line_densities['wind_speed_precision'].values

    flux = wind * line_densities[f'{gas}_line_density']
    flux_std = wind * line_densities[f'{gas}_line_density_precision']

    # along plume distance
    along = line_densities['along']
    seconds = line_densities['seconds_since_emission']

    if model == 'point_source':
        dmin_fit = 0.0
    else:
        if decay_term == 'exp':
            dmin_fit = -25e3
        else:
            dmin_fit = 15e3

    p, p_std, parameters, x, fitted_fluxes = fit_emissions(
            along, flux, flux_std, dmin_fit=0.0, dmax_fit=np.inf,
            model=model, decay_term=decay_term,
    )

    # use wind at source from here
    wind = wind[0] if wind.size > 1 else float(wind)
    wind_std = wind_std[0] if wind_std.size > 1 else float(wind_std)

    fit = xr.Dataset()
    fit['along'] = xr.DataArray(along, dims='along', attrs={'units': 'm'})

    fit[f'along_hr'] = xr.DataArray(x, dims='along_hr',
                                          attrs={'units': 'kg s-1'})
    fit[f'{gas}_flux_fit'] = xr.DataArray(fitted_fluxes, dims='along_hr',
                                          attrs={'units': 'kg s-1'})

    fit[f'{gas}_emissions'] = xr.DataArray(p[0], attrs={'units': 'kg s-1'})
    fit[f'{gas}_emissions_precision'] = xr.DataArray(
        np.sqrt(p_std[0]**2 + (p[0] / wind)**2 * wind_std**2),
        attrs={'units': 'kg s-1'}
    )

    if 'D' in parameters:
        i = parameters.index('D')
        fit[f'{gas}_decay_time'] = xr.DataArray(p[i] / wind,
                                                attrs={'units': 's'})

        fit[f'{gas}_decay_time_precision'] = xr.DataArray(
            np.sqrt(p_std[i]**2 / wind**2 + p[i]**2 / wind**4 * wind_std**2),
            attrs={'units': 's'}
        )
    if 'W' in parameters:
        i = parameters.index('W')
        fit[f'{gas}_source_width'] = xr.DataArray(p[i], attrs={'units': 'm'})
        fit[f'{gas}_source_width_precision'] = xr.DataArray(
            p_std[i], attrs={'units': 'm'}
        )

    return fit


def estimate_emissions(data, winds, sources, curves, gases, t_max=None,
                       method='gauss',
                       variable='{gas}_minus_estimated_background_mass',
                       crs=None, pixel_size=None,
                       f_model=None, use_wind_timeseries=False):
    """
    Estimate emissions using the cross sectional flux (CSF) method.

    Parameters
    ----------
    data : xr.Dataset
        Remote sensing data from pre-processing.

    winds : xr.Dataset
        Wind for each source.

    sources : xr.Dataset
        Source dataset for which emissions will be estimated.

    curves : dict
        Dictionary with center curves.

    gases : str or list of strings
        Gases for which emissions will be estimated.

    t_max : float, optional
        Maximum along-plume distance (in seconds) that will be used for
        computing line densities (currently not implemented!)

    method : str, optional
        Method used for computing the line density with "gauss" fitting Gaussian
        curve and "sub-area" summing mass in sub-polygons. In the upstream
        polygon "sub-area" is always used.

    variable : str, optional
        Name of variable in `data` with gas enhancement above background in mass
        columns (units: kg m-2).

    crs : cartopy.crs, optional
        The coordinate reference system used for the center curves.

    pixel_size : float, optional
        Size of the ground pixel (in meters). If None, pixel size is computed
        from the mean "plume_area" variable in `data`.

    f_model : float or callable, optional
        A number or a a function to convert NO2 to NOx line densites as a
        function of time since emissions. Will only be used uf NO2 in gases to
        convert line densities from NO2 to NOx.

    use_wind_timeseries : bool (default: False)
        Wind speed at each polygon is computed by integrating backwards in time
        (experimental).
    """
    if isinstance(gases, str):
        gases = [gases]

    time = pd.Timestamp(data.time.values)
    results = {}

    extra_variables = [
        ('wind_speed', 'm s-1'),
        ('wind_speed_precision', 'm s-1'),
        ('wind_direction', '°'),
    ]


    if pixel_size is None:
        pixel_size = np.sqrt(np.mean(data['pixel_area']))
        # round to next 100m to prevent irregular spacing when plotting along plume
        pixel_size = int(round(float(pixel_size), -2)) 

    for name, source in sources.groupby('source', squeeze=False):

        if name not in data.source:
            continue

        # no multiple sources
        if ddeq.misc.has_multiple_sources(data, name):
            continue

        # select source data
        this = ddeq.misc.select_source(data, source=name)

        if np.sum(this['detected_plume']) == 0:
            continue

        results[name] = ddeq.misc.init_results_dataset(
            source, gases, extra_vars=extra_variables,
            method=f'cross sectional flux ({method})')


        # compute polygons
        source_type = str(source['type'].values[0])
        xa_values, xb_values, ya, yb = ddeq.misc.compute_polygons(
            this, source_type=source_type,
            pixel_size=pixel_size,
            dmax=np.inf
        )

        # center distance for each polygon
        along = 0.5 * (xa_values + xb_values)

        # get wind for source
        wind = winds.sel(source=name)

        if use_wind_timeseries:
            wind = ddeq.wind.integrate_along_curve(this, wind, curves[name],
                                                   crs=crs)
            wind = ddeq.wind.interpolate_to_polygons(along, wind)
        else:
            wind = wind.squeeze()
            
            if 'time' in wind.dims:
                wind = wind.sel(time=data.time, method="nearest")
                
            wind['seconds_since_emission'] = xr.DataArray(along / float(wind.speed), dims='along')

        # compute angle between curve and wind direction
        if 'angle_between_curve_and_wind' not in wind:
            angle = ddeq.misc.compute_angle_between_curve_and_wind(
                curves[name], wind.direction.values, crs
            )
            wind['angle_between_curve_and_wind'] = xr.DataArray(
                angle, attrs={'units': 'degrees'}
            )

        # TODO/FIXME: limit polygons to t_max
        if t_max is not None:
            raise NotImplementedError("Limiting plume length/time currently not supported.")

        # compute line densities
        polygons = []

        for xa, xb in zip(xa_values, xb_values):

            if method == 'gauss' and xa < 0.0:
                current_method = 'sub-areas'
            else:
                current_method = 'gauss'

            ld = compute_line_density(
                this, gases, variable, 
                pixel_size=pixel_size,
                method=current_method,
                xa=xa, xb=xb, ya=ya, yb=yb,
                share_mu=True, share_sigma=True,
            )
            polygons.append(ld)

        if len(polygons) == 0:
            continue

        polygons = concat_polygons(polygons)
        results[name] = polygons


        # add wind to the results dataset
        wind = wind.rename({
            "speed": "wind_speed",
            "speed_precision": "wind_speed_precision",
            "direction": "wind_direction"
        })

        wind_vars = ["wind_speed", "wind_speed_precision", "wind_direction",
                     "angle_between_curve_and_wind", "seconds_since_emission"]

        results[name] = xr.merge([results[name], wind[wind_vars]])

        # convert NO2 to NOx line densities
        no2_to_nox_conversion = (f_model is not None and 'NO2' in gases)

        if no2_to_nox_conversion:

            # calculate NO2 to NOx conversion factor as function of time
            if isinstance(f_model, numbers.Number):
                f = np.full(results[name].along.size, f_model)
                f_precision = np.zeros_like(f)
            else:
                f, f_precision = f_model(results[name]['seconds_since_emission'])

            results[name]["f"] = ("along", np.array(f))
            results[name]["f_precision"] = ("along", np.array(f_precision))

            # convert NO2 to NOx line densities
            results[name][f"NOx_line_density"] = xr.DataArray(
                    f * results[name]['NO2_line_density'],
                    attrs={'units': 'kg m-1'}
                )
            results[name][f"NOx_line_density_precision"] = xr.DataArray(
                np.sqrt(
                    f**2 * results[name]['NO2_line_density_precision']**2
                    + f_precision**2 * results[name]['NO2_line_density']**2
                ),
                attrs={'units': 'kg m-1'}
            )

        for gas in gases:

            if no2_to_nox_conversion and gas == 'NO2':
                gas = 'NOx'

            if f'{gas}_line_density' not in results[name]:
                continue

            model = 'area_source' if source_type == 'city' else 'point_source'
            decay_term = 'exp' if gas in ['NOx', 'NO2'] else 'none'

            fit = fit_along_plume_fluxes(gas, results[name], model=model,
                                         decay_term=decay_term)
            results[name].update(fit)


            # compute flux and its precision adding wind speed std
            results[name][f'{gas}_flux'] = xr.DataArray(
                results[name]['wind_speed'] * results[name][f'{gas}_line_density'],
                attrs={'units': 'kg s-1'}
            )
            results[name][f'{gas}_flux_precision'] = xr.DataArray(
                np.sqrt(
                      results[name]['wind_speed']**2 * results[name][f'{gas}_line_density_precision']**2
                    + results[name]['wind_speed_precision']**2 * results[name][f'{gas}_line_density']**2
                ),
                attrs={'units': 'kg s-1'}
            )

    return ddeq.misc.Results(results)

