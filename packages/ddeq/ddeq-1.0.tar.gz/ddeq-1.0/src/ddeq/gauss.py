
import os

import scipy.spatial
import scipy.special
import matplotlib.pyplot as plt
import numpy as np
import lmfit
import xarray as xr
import skimage

import ddeq


# --- These five functions deal with a Bezier-based natural coordinate system
def get_bezier_parameters(X, Y, degree=3):
    """\
    Least square qbezier fit using penrose pseudoinverse.
    From: https://stackoverflow.com/a/69438205/4591046
    Parameters:
    X: array of x data.
    Y: array of y data. Y[0] is the y point for X[0].
    degree: degree of the Bézier curve. 2 for quadratic, 3 for cubic.
    Based on https://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy
    and probably on the 1998 thesis by Tim Andrew Pastva, "Bézier Curve Fitting".
    """
    if degree < 1:
        raise ValueError('degree must be 1 or greater.')

    if len(X) != len(Y):
        raise ValueError('X and Y must be of the same length.')

    if len(X) < degree + 1:
        raise ValueError(
            f'There must be at least {degree + 1} points to '
            f'determine the parameters of a degree {degree} curve. '
            f'Got only {len(X)} points.'
        )

    def bpoly(n, t, k):
        """ Bernstein polynomial when a = 0 and b = 1. """
        return t ** k * (1 - t) ** (n - k) * scipy.special.comb(n, k)

    def bmatrix(T):
        """ Bernstein matrix for Bézier curves. """
        return np.matrix([[bpoly(degree, t, k) for k in range(degree + 1)]
                          for t in T])

    def least_square_fit(points, M):
        M_ = np.linalg.pinv(M)
        return M_ * points

    T = np.linspace(0, 1, len(X))
    M = bmatrix(T)
    points = np.array(list(zip(X, Y)))

    final = least_square_fit(points, M).tolist()
    final[0] = [X[0], Y[0]]
    final[len(final)-1] = [X[len(X)-1], Y[len(Y)-1]]

    return final


def initial_curve_guess(curves, source):
    """\
    Base the curve guess on the fitted 'curves' object.
    IN:
      curves    list      List of ddeq curve objects
      source    string    Source ID (e.g., 'Berlin')
    OUT:
      x0, y0, x1, y1, x2, y2     Nodes for the Bezier curve
    """
    t = np.linspace(curves[source].t_o, curves[source].tmax, 3)
    X, Y = curves[source](t=t)
    nodes = get_bezier_parameters(X, Y, degree=2)
    return (
        nodes[0][0] / 1e6,
        nodes[0][1] / 1e6,
        0.5 * nodes[1][0] / 1e6 + (nodes[0][0] / 1e6 + nodes[2][0] / 1e6) / 4,
        0.5 * nodes[1][1] / 1e6 + (nodes[0][1] / 1e6 + nodes[2][1] / 1e6) / 4,
        nodes[2][0] / 1e6,
        nodes[2][1] / 1e6
    )


def bernstein_poly(i, n, t):
    """\
    The Bernstein polynomial of n, i as a function of t
    """
    return scipy.special.comb(n, i) * ( t**(n-i) ) * (1 - t)**i


def bezier_curve(points, nTimes=50):
    """\
    Given a set of control points, return the bezier curve defined by the
    control points.

    points should be a list of lists, or list of tuples
    such as [ [1,1],
              [2,3],
              [4,5], .. [Xn, Yn] ]
    nTimes is the number of time steps, defaults to 1000

    See http://processingjs.nihongoresources.com/bezierinfo/
    """

    nPoints = len(points)
    xPoints = np.array([p[0] for p in points])
    yPoints = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, nTimes)

    polynomial_array = np.array([ bernstein_poly(i, nPoints-1, t)
                                 for i in range(0, nPoints)])

    xvals = np.dot(xPoints, polynomial_array)
    yvals = np.dot(yPoints, polynomial_array)

    return xvals[::-1], yvals[::-1]


def natural_coords(x_nodes, y_nodes, lon, lat):
    """\
    Create a quick 'natural coordinate' system w.r.t. a curve,

    IN:
      x_nodes   list of node points (in meters)
      y_nodes   list of node points (in meters)
      lon       2D array of longitude coordinates (in meters)
      lat       2D array of latitude coordinates (in meters)

    OUT:
      x_min     2D array of TANGENTIAL distance to the curve
      y_min     2D array of NORMAL distance to the curve
      curve     bezier.Curve object (allows for simple plotting, e.g., curve.plot())
    """
    # Generate the Bezier curve from its nodes
    points = np.stack( (x_nodes,y_nodes) ).T

    # Evaluate points along the parametric curve
    npts = 100 # higher is more accurate, but will take more time.
    xp, yp = bezier_curve(points, nTimes=npts)

    # Establish shortest Euclidean distance (automatically corresponds to
    # shortest perpendicular distance between any point vs. the curve!)
    grid_coords = np.nan_to_num(np.vstack( (lon.ravel(), lat.ravel()) ).T)
    curve_coords = np.vstack( (xp.ravel(), yp.ravel()) ).T
    kdtree = scipy.spatial.KDTree(curve_coords)
    neighbours, idx = kdtree.query(grid_coords)

    # ... so, establish the normal distance to the line
    y_min = neighbours.reshape(lon.shape)
    y_min = np.where( ~np.isnan(lat), y_min, np.nan)

    # ---> Establish the corresponding length along the line
    offsets = np.sqrt( np.gradient( xp )**2 + np.gradient( yp )**2 )
    x_length = np.cumsum( offsets )
    x_min = x_length[idx].reshape(lon.shape)
    x_min = np.where( ~np.isnan(lon), x_min, np.nan)

    return x_min, y_min, curve_coords


# --- This functions deals with generating a Gaussian plume model
def Gaussian_plume_model(K, u, Q, xn, yn, BG=0.0, x0=0, y0=0, tau=14400, b=1,
                         sigmaG=1, plumetype='city'):
    """\
    Returns vertically integrated Gaussian plume image
    IN:
      K         scalar    Eddy diffusivity coefficient (m^2/s)
      u         scalar    Wind speed (m/s)
      Q         scalar    Emission rate (kg/s)
      xn        2D array  Natural coordinates (tangential direction)
      yn        2D array  Natural coordinates (normal direction)
      BG        scalar    Background constant (kg)
      x0        scalar    Source position in tangential direction
      y0        scalar    Source position in normal direction
      tau       scalar    Decay time (s)
      b         scalar    Exponential function applied to plume spread
      sigmaG    float     Defines the exponentially modified Gaussian spread
      plumetype string    If 'city', the plume gets a 10 km initial width
                          instead of a point source

    OUT:
      plume     2D array of the vertically integrated plume
    """
    down = xn > x0
    if plumetype=='city':
        x_offset = ( 10000**2 * u / (2*K) )**(1/b) 
    else:
        x_offset = 0
    ynp = np.where(xn<=x0, 0, yn-y0)[down]
    xnp = np.where(xn<=x0, 0, xn-x0)[down]
    sigma = np.sqrt(2.0 * K * (xnp+x_offset)**b / u)
    c = Q / (np.sqrt(2*np.pi) * sigma * u) * np.exp(-0.5 * ynp**2 / sigma**2)

    # --- Function one: exponential decay
    decay = ddeq.functions.decay_function(xn, x0, tau*u)

    # --- Function two: 
    gauss = ddeq.functions.gauss(np.linspace(-5,5), E0=1.0, sigma=sigmaG,
                                 shift=0.0)

    # --- Convolve the two functions to get exponentially modified Gaussian
    decay = np.apply_along_axis(lambda m: np.convolve(m, gauss, mode='same'),
                                axis=1, arr=decay)
    c *= (decay[down] / decay.max())
    plume = np.full(xn.shape, float(BG))
    plume[down] += c

    return plume


# --- These two functions deal with lmfit in- and output
def generate_params(curves, params, source, num, wind_speed,
                    Q_prior, tau_prior=4.0*3600):
    """\
    Generate LMFit params structure for the initial guess,
    which will be refined later. This initial guess is for
    an NO2 source.
    """
    x0, y0, x1, y1, x2, y2 = initial_curve_guess(curves, source)
    params.add(f'x0_{num}', x0, vary=False)
    params.add(f'x1_{num}', x1, min=x1-0.02, max=x1+0.02, vary=True)
    params.add(f'x2_{num}', x2, min=x2-0.02, max=x2+0.02, vary=True)
    params.add(f'y0_{num}', y0, vary=False)
    params.add(f'y1_{num}', y1, min=y1-0.02, max=y1+0.02, vary=True)
    params.add(f'y2_{num}', y2, min=y2-0.02, max=y2+0.02, vary=True)
    params.add(f'Q_{num}', Q_prior, min=0.1*Q_prior, max=1.9*Q_prior, vary=True)
    params.add(f'u_{num}', float(wind_speed), vary=False)
    params.add(f'K_{num}', 400, min=200, max=2000, vary=False)
    params.add(f'tau_{num}', tau_prior, min=1*3600, max=200*3600, vary=False) # in seconds (1-200 hours)
    params.add(f'b_{num}', 0.9, min=0.7, max=1.8, vary=True)
    params.add(f'sigmaG_{num}', 0.01, min=0.01, max=4, vary=False)
    params.add(f'BG', 0, vary=True)
    return params


def parse_lmfit_params(params, plumeNum):
    """\
    Parse the lm fit parameters to select the values
    relevant to describe one single plume
    params = lmfit Parameters class
    plumeNum = number for which you want to return the properties
    """
    lmfit_dict = params.valuesdict()

    # Extract features that describe this plume
    x_nodes = [lmfit_dict[f'x0_{plumeNum}'],
               lmfit_dict[f'x1_{plumeNum}'],
               lmfit_dict[f'x2_{plumeNum}']]
    y_nodes = [lmfit_dict[f'y0_{plumeNum}'],
               lmfit_dict[f'y1_{plumeNum}'],
               lmfit_dict[f'y2_{plumeNum}']]
    Q = lmfit_dict[f'Q_{plumeNum}']
    K = lmfit_dict[f'K_{plumeNum}']
    u = lmfit_dict[f'u_{plumeNum}']
    tau = lmfit_dict[f'tau_{plumeNum}']
    b = lmfit_dict[f'b_{plumeNum}']
    sigmaG = lmfit_dict[f'sigmaG_{plumeNum}']
    BG = BG = lmfit_dict["BG"]

    return x_nodes, y_nodes, Q, K, u, tau, b, BG, sigmaG


# --- These three functions deal with overlapping plumes
def ini_Gaussian_plumes(curves, overlapping_sources, wind_speed, Q_priors,
                        tau_priors):
    """\
    Initialize the plume guess for ALL overlapping plumes
    """
    params = lmfit.Parameters()
    for i, sourcename in enumerate(overlapping_sources):
        params = generate_params(curves, params, sourcename, i+1,
                                 wind_speed[i] if isinstance(wind_speed,list) else wind_speed,
                                 Q_priors[i], tau_priors[i])
    num_plumes = len(overlapping_sources)
    return params, num_plumes


def total_plume_model(params, lon, lat, numplumes, plumetypes):
    """\
    Return a (sum of) Gaussian plume(s) based on lm-fit input parameters.

    params = from lmfit Parameters class
    lon = 2D array of longitude coordinates (in meters)
    lat = 2D array of latitude coordinates (in meters)
    """
    # Loop over number of plumes requested...
    for plumeNum in range(1,numplumes+1):

        # Extract info from the parameters dictionary for this plume
        x_nodes, y_nodes, Q, K, u, tau, b, BG, sigmaG = parse_lmfit_params(
            params, plumeNum
        )

        # Generate the natural coordinate system (x=tangential, y=normal)
        xn, yn, curve = natural_coords(np.asarray(x_nodes)*1e6,
                                       np.asarray(y_nodes)*1e6, lon, lat)

        # Generate the Gaussian plume given the input parameters
        model_tmp = Gaussian_plume_model(K, u, Q, xn, yn, tau=tau, BG=BG, b=b,
                                         sigmaG=sigmaG,
                                         plumetype=plumetypes[plumeNum-1])
        # Add plume(s) to the modeled data
        if plumeNum == 1:
            model = model_tmp
            curves = [curve]
        else:
            model += model_tmp
            curves.append(curve)

    return model, curves


# --- The objective function that we fit towards
def residual(params, lon, lat, data, numplumes=1, eps=1, plumetypes=['city',],
             mask=None):
    """\
    Residual between input data and Gaussian plume(s)
    IN:
      params     params    lmfit params file for all sources
      lon        2D array  Longitude coordinates (in meters)
      lat        2D array  Latitude coordinates (in meters)
      numplumes  scalar    Number of plumes in the params file
      eps        scalar    Data uncertainty (for the objective function)
      plumetypes list      List of plume types

    OUT:
      residual   scalar    The residual between input data and Gaussian plumes
    """
    model, _ = total_plume_model(params, lon, lat, numplumes=numplumes,
                                 plumetypes=plumetypes)
    # --- Basic residual
    res = (data-model)

    # --- Prevent nans in the final result
    res = np.where(np.isnan(res), 0, res)
    if mask is not None:
        res = res[mask]

    return res / eps


# --- Fitting of one (or more) sources
def gaussian_plume_estimates(this, overlapping_sources, curves, priors, wind_speed,
                             variable='{gas}_minus_estimated_background_mass',
                             trace_gases=['NO2', 'CO2'],
                             fit_decay_times=[True, False],
                             sources=None, results=None, verbose=False):
    """\
    Do the Gaussian plume estimation procedure.
    IN:
      this                 xarray Dataset       Containing the data for (overlapping) sources
      variable             string               Name of varaible used for observations.
      overlapping_sources  list of strings      Source name(s) for this (and other) sources
      curves               list of ddeq curves  List of ddeq curve objects
      priors               dict. of scalars     Dictionary of priors for this (and other) sources
      wind_speed           list of scalars      List of wind speeds for this (and other) sources
      trace_gases          list of strings      List of trace gases considered
      fit_decay_times      list of bools        List if decay times are fitted
      sources              ddeq. source obj.    ddeq source object file with locations of all sources
      verbose              Boolean              Print more data regarding the fitting process if true

    OUT:
      this                 xarray Dataset       Same DataArray as input, but with added estimated fields
      out_curves           dict of curves       Contains the fitted Bezier curves which may be plotted
                                                as simply as curve.plot(100)
    """
    # Initialize space and time coordinates
    area = np.isfinite(this['xp']).any('source')

    x = np.where(area, this['x'].values, np.nan)
    y = np.where(area, this['y'].values, np.nan)

    out_fields = {}
    out_curves = {}

    # Do the Gaussian fit in order of provided gases
    for num_gas, (gas, fit_decay) in enumerate(zip(trace_gases, fit_decay_times)):

        if verbose:
            print(f'Fitting a Gaussian plume model for {gas}')

        # Initialize guess
        Q_prior = [priors[s][gas]["Q"] for s in overlapping_sources]
        tau_prior = [priors[s][gas]["tau"] for s in overlapping_sources]
        if num_gas == 0:
            params, num_plumes = ini_Gaussian_plumes(curves, overlapping_sources,
                                                     wind_speed, Q_prior, tau_prior)
        else:
            # Use optimized parameters from previous gas
            params = tau_fit.params
            for name in params:
                if "Q" in name:
                    source_num = int(name.split('_')[-1]) - 1 # -> (0, 1, 2, ...)
                    Q0 = Q_prior[source_num]
                    params[name].set(min=0.1*Q0, max=1.9*Q0, value=Q0, vary=True)
                if "BG" in name:
                    params[name].set(value=0, vary=True)
                if ("K" in name) or ("b" in name):
                    params[name].set(min=0.99*params[name], max=1.01*params[name],
                                     vary=True)
                if ("x" in name) or ("y" in name):
                    params[name].set(vary=False)

        # fix decay time
        if not fit_decay:
            for name in params:
                if "tau" in name:
                    params[name].set(vary=False)
        if verbose:
            params.pretty_print()

        # Fit the data
        observations = this[variable.format(gas=gas)].values
        mask = this.detected_plume.any('source')
        mask = skimage.morphology.dilation(mask, skimage.morphology.square(5))
        observations = np.where( mask, observations, np.nan )
        noise_level  = this[variable.format(gas=gas)].attrs.get('noise_level', np.nan)

        # FIT 1 (location, Q, b)
        mini = lmfit.Minimizer(residual, params,
                               fcn_args=(x, y, observations, num_plumes, noise_level,
                                         np.atleast_1d(sources.sel(source=overlapping_sources).type.data), mask),
                               nan_policy='propagate',
                               max_nfev=400)

        # ini_fit = mini.minimize(method='leastsq')
        ini_fit = mini.minimize(method='leastsq')

        if verbose:
            ini_fit.params.pretty_print()
            print("no. of evaluations:", ini_fit.nfev)
            print("Reduced chi-square:", ini_fit.redchi)
            print("Akaike Information:", ini_fit.aic)

        # FIT 2 (include K and decay, exclude location)
        for name in ini_fit.params:
            if ("K" in name) or ("tau" in name):
                ini_fit.params[name].set(vary=True)
            elif ("x" in name) or ("y" in name):
                ini_fit.params[name].set(vary=False)

        mini = lmfit.Minimizer(residual, ini_fit.params,
                               fcn_args=(x, y, observations, num_plumes, noise_level,
                                         np.atleast_1d(sources.sel(source=overlapping_sources).type.data), mask),
                               nan_policy='propagate',
                               max_nfev=200)
        iniU_fit = mini.minimize(method='leastsq')

        if verbose:
            iniU_fit.params.pretty_print()
            print("no. of evaluations:", iniU_fit.nfev)
            print("Reduced chi-square:", iniU_fit.redchi)
            print("Akaike Information:", iniU_fit.aic)

        # FIT 3 (fit Q only)
        for name in iniU_fit.params:
                if "Q" in name:
                    iniU_fit.params[name].set(vary=True)
                else:
                    iniU_fit.params[name].set(vary=False)

        mini = lmfit.Minimizer(residual, iniU_fit.params,
                               fcn_args=(x, y, observations, num_plumes, noise_level,
                                         np.atleast_1d(sources.sel(source=overlapping_sources).type.data), mask),
                               nan_policy='propagate',
                               max_nfev=20)
        Q_fit = mini.minimize(method='leastsq')

        if verbose:
            Q_fit.params.pretty_print()
            print("no. of evaluations:", Q_fit.nfev)
            print("Reduced chi-square:", Q_fit.redchi)
            print("Akaike Information:", Q_fit.aic)

        # FIT 4 (fit TAU only)
        for name in Q_fit.params:
            if "Q" in name:
                Q_fit.params[name].set(vary=False)
            elif 'tau' in name:
                Q_fit.params[name].set(vary=True)

        mini = lmfit.Minimizer(residual, Q_fit.params,
                               fcn_args=(x, y, observations, num_plumes, noise_level,
                                         np.atleast_1d(sources.sel(source=overlapping_sources).type.data), mask),
                               nan_policy='propagate',
                               max_nfev=20)

        tau_fit = mini.minimize(method='leastsq')

        if verbose:
            tau_fit.params.pretty_print()
            print("no. of evaluations:", tau_fit.nfev)
            print("Reduced chi-square:", tau_fit.redchi)
            print("Akaike Information:", tau_fit.aic)

        # Save the data
        for number, name in enumerate(overlapping_sources, 1):

            Q_est = Q_fit.params[f'Q_{number}'].value
            Q_std = Q_fit.params[f'Q_{number}'].stderr


            # if no successful estimate took place
            if Q_std is None or not (0.1 * Q_prior[number-1] <= Q_est <= 1.9 * Q_prior[number-1]):
                if verbose:
                    print('No reliable estimate found.')
                continue

            Q_std = np.sqrt(Q_std**2 + (Q_est / Q_fit.params[f"u_{number}"]**2 * 0.5**2))

            results[f'{gas}_estimated_emissions'].loc[dict(source=name)] = Q_est
            results[f'{gas}_estimated_emissions_precision'].loc[dict(source=name)] = Q_std

            for new, old in [
                ('wind_speed', f'u_{number}'),
                (f'{gas}_eddy_diffusivity_coefficient', f'K_{number}'),
                (f'{gas}_background', 'BG'),
                (f'{gas}_decay_time', f'tau_{number}')
            ]:
                if new in results:
                    results[new].loc[dict(source=name)] = tau_fit.params[old].value
                    results[f'{new}_precision'].loc[dict(source=name)] = tau_fit.params[old].stderr

        mod, curves = total_plume_model(
            tau_fit.params, x, y, numplumes=num_plumes,
            plumetypes=np.atleast_1d(sources.sel(source=overlapping_sources).type.data)
        )
        out_fields[gas] = mod
        out_curves[gas] = curves

    return results, out_fields, out_curves


def estimate_emissions(data, winds, sources, curves, gases, priors=None,
                       variable='{gas}_minus_estimated_background_mass',
                       fit_decay_times=False, skip_overlapping_plumes=True,
                       verbose=False):
    """
    Estimate emissions using Gaussian plume (GP) inversion.

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

    priors : dict, optional
        A dictionary with prior informatio for each source with source strength
        and decay time. For example:

        >>> priors = {'Matimba': {
        >>>    'NO2': {
        >>>        'Q': 3.0,       # in kg/s
        >>>        'tau': 4*60**2  # in seconds
        >>>   }
        >>> }}

    variable : str, optional
        Name of variable in `data` with gas enhancement above background in mass
        columns (units: kg m-2).

    fit_decay_times: boolean or list of booleans, optional
        If True, the decay time will be included and fitted in the Gaussian
        plume model.

    skip_overlapping_plumes : boolean
        If True, do not process overlapping plumes.

    verbose : boolean
        If True, provide more information.

    Returns
    -------
    xr.Dataset
        The remote sensing dataset with added data arrays with Gaussian plume
        models for each trace gas and source.

    xr.Dataset
        The results dataset with estimated emissions and other parameters.

    """
    if not skip_overlapping_plumes:
        print(
            'Fitting multiple Gaussian plumes simultaneously is an experimental'
            ' feature that might fail without warning. It is recommended to set '
            '`skip_overlapping_plumes` to True.'
        )

    # at least 1D for iterating
    gases = np.atleast_1d(gases)
    fit_decay_times = np.atleast_1d(fit_decay_times)

    if fit_decay_times.size == 1:
        fit_decay_times = fit_decay_times.repeat(gases.size)

    # init results dataset
    extra_variables = [
        ('wind_speed', 'm s-1'),
        ('wind_speed_precision', 'm s-1'),
        ('wind_direction', '°'),
        ('{gas}_eddy_diffusivity_coefficient', 'm2 s-1'),
        ('{gas}_eddy_diffusivity_coefficient_precision', 'm2 s-1'), 
        ('{gas}_background', 'kg m-2'),
        ('{gas}_background_precision', 'kg m-2'),
    ]

    for gas, do_fit in zip(gases, fit_decay_times):
        if do_fit:
            extra_variables += [
                (f'{gas}_decay_time', 's'),
                (f'{gas}_decay_time_precision', 's')
            ]

    results = ddeq.misc.init_results_dataset(
        sources, gases, extra_vars=extra_variables,
        method=f'gaussian plume inversion'
    )

    for gas in gases:
        shape = (100, 2, results.source.size)
        dims = ('t', 'xy', 'source')
        nans = np.full(shape, np.nan)
        results[f'{gas}_curve'] = xr.DataArray(nans, dims=dims)

    # add array for model fits
    shape = data['detected_plume'].shape
    for gas in gases:
        data[f'{gas}_plume_model_mass'] = xr.DataArray(
            np.full(shape, np.nan),
            dims=data['detected_plume'].dims
        )

    for overlapping_sources in ddeq.misc.get_source_clusters(data, sources):

        if len(overlapping_sources) > 1 and skip_overlapping_plumes:
            continue

        this = data.sel(source=overlapping_sources)
        wind_speeds = list(winds['speed'].sel(source=overlapping_sources).values)

        results, fields, CR = gaussian_plume_estimates(this, overlapping_sources,
                                                       curves, priors, wind_speeds,
                                                       variable, trace_gases=gases,
                                                       fit_decay_times=fit_decay_times,
                                                       sources=sources,
                                                       results=results,
                                                       verbose=verbose)

        for gas in gases:
            for i, name in enumerate(overlapping_sources):
                data[f'{gas}_plume_model_mass'].loc[dict(source=name)][:] = fields[gas]
                results[f'{gas}_curve'].loc[dict(source=name)][:] = CR[gas][i]

    return data, results



class PlumeModel:
    def __init__(self, x, y, u, x0=0.0, y0=0.0):
        """\
        Computes Gaussian plume (units: kg/m2).
        x: distance from origin in m
        y: distance from center line in m
        u: wind speed in m/s
        x0: x-coordinate of origin
        y0: y-coordinate of origin
        TODO:
        - decay time
        """
        self.x = x
        self.y = y
        self.u = u

        # location of origin
        self.x0 = x0
        self.y0 = y0

    def __call__(self, foo, Q, K, BG=0.0, tau=None):
        """
        Q: emission strength in kg/s
        K: eddy diffusion coefficient in m²/s
        BG: background in kg/m²
        """
        # dispersion along the plume
        down = self.x > self.x0
        sigma = np.sqrt(2.0 * K * (self.x[down] - self.x0) / self.u)

        # compute Gaussian plume
        c = Q / (np.sqrt(2.0 * np.pi) * sigma * self.u) * np.exp(-0.5 * (self.y[down] - self.y0)**2 / sigma**2)

        if tau is not None:
            c = c * ddeq.functions.decay_function(self.x, self.x0, tau)[down]

        plume = np.full(self.x.shape, BG)
        plume[down] += c

        return plume
