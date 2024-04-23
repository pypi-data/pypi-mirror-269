

import warnings

import numpy as np
import scipy.ndimage
import scipy.stats
import shapely
import skimage.measure
import xarray
import sys
import os
import pandas
import ddeq
# --- Load diplib quietly, so as to not crowd the std out
import contextlib
with contextlib.redirect_stdout(None):
    import diplib as dip

# ignore warnings
warnings.filterwarnings('ignore', r'All-NaN (slice|axis) encountered')
np.seterr(divide='ignore', invalid='ignore')


def find_plume_by_labels(lon, lat, labels, lon_o, lat_o, radius):
    """\
    Find plume by using `labels` that are within `radius` (in km)  around
    (`lon_o`, `lat_o`).
    """
    lon = np.array(lon)
    lat = np.array(lat)

    area = shapely.geometry.Point(lon_o, lat_o).buffer(float(radius) / 100.0)

    numbers = []
    for i in set(labels.flatten()) - {0}:
        
        points = np.transpose([lon[labels==i], lat[labels==i]])
        points = shapely.geometry.MultiPoint(points)
        
        if points.intersects(area):
            numbers.append(i)

    if numbers:
        return  np.any([labels == i for i in numbers], axis=0)
    else:
        return np.zeros(labels.shape, bool)


def label_plumes(d, n_min=0):
    """\
    Label detected plume pixels. Regions with less than n_min are removed.
    """
    d[np.isnan(d)] = 0
    labels = skimage.measure.label(d, background=0)

    i = 1
    final = np.zeros_like(labels)

    for l in set(labels.flatten()):
        if l != 0 and np.sum(labels == l) >= n_min:
            final[labels == l] = i
            i += 1

    return final


def do_test(mean_s, mean_b, var_rand, var_sys, size, q, variance=None, dtype='f4'):
    """
    mean_s:    mean of sample
    mean_b:    mean of background
    variance:  estimated local variance
    
    var_rand:  random variance of sample
    var_sys:   systematic variance of sample
    size:      size of sample
    q:         threshold
    
                 mean_s - mean_bg
    SNR = ----------------------------- > z_q
           np.sqrt(var_rand + var_sys)
    """
    mean_s = np.array(mean_s)
    size = np.array(size)

    if np.ndim(mean_b) == 0:
        mean_b = np.full(mean_s.shape, mean_b)

    if variance is None:
        z_values = np.full(mean_s.shape, np.nan)
        m = size > 0

        z_values[m] = mean_s[m] - mean_b[m]
        z_values[m] /= np.sqrt(var_rand / size[m] + var_sys)
    else:
        z_values = (mean_s - mean_b) / np.sqrt(variance)

    return z_values.astype(dtype), z_values > scipy.stats.norm.ppf(q)


def weighted_mean(x, kernel):
    """
    Computed weighted mean.
    """
    valids = np.isfinite(x)
    
    if np.any(valids):
        kernel = kernel[valids]
        kernel = kernel / kernel.sum()

        return np.sum(x[valids] * kernel)
    else:
        return np.nan


def weighted_mean_var(x, kernel, variance):
    """
    Compute variance reduction of weighted mean.
    """
    valids = np.isfinite(x)
    
    if np.any(valids):
        kernel = kernel[valids]
        kernel = kernel / kernel.sum()

        return variance * np.sum(kernel**2)
    else:
        return np.nan

    
def gaussian_kernel(sigma, size=11):
    """
    Create a gaussian kernel.
    """
    if size % 2 == 0:
        raise ValueError('kernel size needs to be an odd integer')
        
    f = np.zeros([size,size])
    f[size//2, size//2] = 1.0
    g = scipy.ndimage.gaussian_filter(f, sigma=sigma)
    return g


def local_mean(img, size, kernel_type='gaussian', var_rand=1.0):
    """
    Compute local mean, variance reduction and number of valid pixels using
    different kernel_types:

    - neighborhood (size: 1,5,9,13,25)
    - gaussian (size is standard deviation)
    - uniform

    """
    if kernel_type == 'gaussian':
        footprint = gaussian_kernel(sigma=size)

    elif kernel_type == 'uniform':
        footprint = np.ones((size, size))

    elif kernel_type == 'neighborhood':
        if size == 1:
            return img.copy(), np.ones_like(img)

        elif size == 5:
            footprint = np.array([
                [0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]
            ])
        elif size == 13:
            footprint = np.array([
                [0, 0, 1, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 1, 0, 0],
            ])
        elif size == 37:
            footprint = np.array([
                [0,0,1,1,1,0,0],
                [0,1,1,1,1,1,0],
                [1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1],
                [0,1,1,1,1,1,0],
                [0,0,1,1,1,0,0],
            ])
        elif size in [9,25,49,81,121]:
            size = int(np.sqrt(size))
            footprint = np.ones((size,size))
        else:
            raise ValueError('size of neighborhood %d not supported' % size)
            
    else:
        raise ValueError('"kernel_type" needs to be "gaussian", "uniform" or "neighborhood"')

    # only compute if any values in across-track direction
    domain = np.any(img, axis=1)

    # normalize footprint
    footprint = footprint / footprint.sum()
    
    # keep dtype of image
    footprint = footprint.astype(img.dtype)

    # compute mean, variance and number of valid pixels
    mean = np.full(img.shape, np.nan, dtype=img.dtype)
    var = np.full(img.shape, np.nan, dtype=img.dtype)
    n = np.full(img.shape, np.nan, dtype=int)
   
    mean[domain,:] = scipy.ndimage.generic_filter(img[domain,:], function=weighted_mean,
                                                  size=footprint.shape, mode='constant', cval=np.nan,
                                                  extra_arguments=(footprint.flatten(),))

    var[domain, :] = scipy.ndimage.generic_filter(img[domain,:], function=weighted_mean_var,
                                                  size=footprint.shape, mode='constant', cval=np.nan,
                                                  extra_arguments=(footprint.flatten(), var_rand))
    n[domain,:] = scipy.ndimage.generic_filter(
            np.isfinite(img).astype(int)[domain,:], np.count_nonzero,
            footprint=(footprint != 0), mode='constant', cval=0
    )

    return mean, var, n


def local_median(img, size):
    """
    Compute local median for image.
    """
    return scipy.ndimage.generic_filter(img, np.nanmedian, size)


def overlaps_with_sources(lon, lat, lon_o, lat_o, radius):
    """
    lon, lat      longitude and latitude of satellite pixels
    lon_o, lat_o  longitude and latitude of point source
    radius        radius around source (in km)
    
    """
    # FIXME: does not work if radius < pixel size
    #assert np.min(radius) / 100.0 > np.max(np.diff(lon))
    
    # use only valid longitudes and latitudes
    valids = np.isfinite(lon) & np.isfinite(lat)
    lon = np.array(lon)[valids]
    lat = np.array(lat)[valids]
    
    # create points
    points = np.transpose([lon, lat])
    points = shapely.geometry.MultiPoint(points)
    points = points.convex_hull
   
    # create area around source
    overlaps = []
    
    for x,y,r in zip(lon_o, lat_o, radius):
        r = float(r) / 100.0 # km -> degree (roughly)
        area = shapely.geometry.Point(x, y).buffer(r)

        overlaps.append(points.intersects(area))

    return np.array(overlaps, dtype='bool')


def generate_downstream_masks(data, wind_dir_at_source, source, cost_image):
    """
    This finds the cost of moving from the source to any other
    point in an image. Moving downwind is cheap (where np.cos(0°)=1), 
    and moving backwards is not allowed.
    This allows us to select purely the downstream portion of any
    detected plume, disregarding any upstream data.
    
    data                xarray dataframe
    wind_dir_at_source  wind direction at the source (0 degrees is wind from the North)
    source              name of source to compute mask for
    cost_image          numpy array (=1/is_hit) 
    """
    # Find the indices on the grid closest to the source
    dist = ((data.lon-data.lon_o.sel(source=source)).values**2 
          + (data.lat-data.lat_o.sel(source=source)).values**2)
    idx, idy = np.unravel_index(dist.argmin(), dist.shape) 
    
    # Correct for the difference between grid "up" and North direction
    delta = (np.rad2deg(np.arctan2( 
         np.gradient(data.lat, axis=0),
        -np.gradient(data.lon, axis=0)))
             +90)[idx, idy] #(this field...
                            #    delta=0    means the track goes north,
                            #    delta=pi/2 means the track goes east, etc.

    angle_matrix = np.array([[+225,  +180 , +135], 
                             [+270, np.NaN, +90 ], 
                             [+315,  +0   , +45 ]]) # The range [0, 45, ..., 360] degrees layed around this matrix
    
    metric = 1-np.cos( 
                 np.deg2rad( float(wind_dir_at_source)
                           - delta
                           + angle_matrix
                           ) 
                       )
    metric[metric>1] = -1
    metric[1,1] = 0
    
    # Perform a weighted distance walk.
    binimg = np.zeros_like(cost_image)
    binimg[idx, idy] = 1
    out = dip.GreyWeightedDistanceTransform(
               cost_image, dip.Image(binimg)==0, 
               metric=metric, mode='chamfer')
    mask = out<10
    return mask


def unmix_plumes(data, winds, min_plume_size=0):
    '''
    After running the plume detection algorithm, overlapping plumes
    are discarded. This function recovers the portions of the plume
    prior to mixing (i.e., from the source, downstream to the place
    where the plumes overlap). 
    
    data                xarray dataset with observations etc.
    winds               xarray dataset with wind directions
    '''
    # Preserve the originally detected plumes
    data['detected_plume_orig'] = data.detected_plume.copy(deep=True)

    # Copy the Boolean 'is_hit' field into an image field 
    # (1 where is_hit=True, 1e5 otherwise)
    cost_image = dip.Image(1/(data.is_hit.values+1e-5))

    # Loop through all sources a second time, checking for overlaps
    for source in data.source:
        # Returns, e.g., [True, False, False, True] 
        # if source[0] and source[3] overlap.
        list_of_overlaps = \
               (data.detected_plume_orig.sel(source=source) \
               *data.detected_plume_orig).any(dim=['nobs', 'nrows']) 

        # Default: no overlap, nothing to do
        if list_of_overlaps.sum() <= 1:
            continue

        # Get list of overlapping sources
        names_of_overlaps = data.source[list_of_overlaps]
        
        # Get corresponding wind directions
        wind_direction = [winds.direction.sel(source=name) for name in names_of_overlaps]
        
        # Compute directional (downstream) plume masks
        masks = []
        for i, singlesource in enumerate(data.source[list_of_overlaps]):
            mask = generate_downstream_masks(
                data, wind_direction[i], singlesource, cost_image)
            masks.append(mask)

        # Fix the mask belonging to the source
        source_idx = np.where(
                      data.source[list_of_overlaps]==source 
                             )[0][0]
        mask_source = masks[source_idx]
        masks.pop(source_idx)

        # Remove masks if they are downstream
        for mask in masks:
            mask_source -= mask

        # Relabel the detected plumes
        labels = label_plumes(data.is_hit.values*mask_source, 
                              min_plume_size)
        data.detected_plume.loc[dict(source=source)] = \
            find_plume_by_labels(
                    data.lon, data.lat, labels,
                    data['lon_o'].sel(source=source),
                    data['lat_o'].sel(source=source),
                    data['radius'].sel(source=source)
                                        )
    return data


def detect_plumes(data, sources, variable='NO2', variable_std='NO2_std',
                  var_sys=0.0, filter_type='gaussian', filter_size=0.5, q=0.99,
                  min_plume_size=0, background='median'):
    """
    Detects plumes inside remote sensing `data` and assigns them to given
    `sources`.

    Parameters
    ----------
    data : xr.Dataset
        Dataset of remote sensing data read, for example, by
        `ddeq.smartcarb.read_level2`

    sources : xr.Dataset
        Dataset with source locations read, for example, by
        `ddeq.misc.read_point_sources`.

    variable : str, optional
        Name of data array in `data` with the trace gas columns  that is used
        for plume detection.

    variable_str : str, optional
        Name of data array in `data` with the uncertainty of the trace gas
        columns.

    var_sys : float, optional
        Systematic uncertainty of the trace gas field that is not reduced by
        spatial averaging. Standard values used in the SMARTCARB and CoCO2
        project were (0.2 ppm)**2 for CO2 and (0.5e15 cm-2 = 8.3e-6 mol/m²)**2
        for NO2.

    filter_type : str, optional
        Name of filter used for computing the local mean can be "gaussian"
        (default), "uniform" or "neighborhood" (see `ddeq.dplume.local_mean` for
        details).

    filter_size : number, optional
        Size of filter user for computing the locam mean in pixels. Needs to be
        an integer for "uniform" and "neighborhood".

    q : float, optional
        probability for threshold z(q) that a pixel is significantly enhanced
        above the background used for the statistical z-test.

    min_plume_size : integer, optional
        Minimum size of connected pixels that are considered a plume (default:
        0).

    background : float or string, optional
        If number, the background used for the plume detection. The default
        value is "median", which computes the background field using a median
        filter of 100 by 100 pixels.

    Returns
    -------
    xr.Dataset
        Returns `data` with added variables (e.g., `detected_plumes`) that
        contain the results from the plume detection algorithm.

    """
    # Avoid running expensive plume detection when no sources in swath
    overlaps = overlaps_with_sources(data.lon, data.lat, sources['lon_o'],
                                     sources['lat_o'], sources['radius'])

    if not np.any(overlaps):
        return data

    # Add overlapping sources to dataset
    sources = sources.where(xarray.DataArray(overlaps, dims='source'), drop=True)
    data.update(sources)

    # Detect plume

    # Estimate background mean
    if isinstance(background, str) and background == 'median':
        mean_bg = local_median(data[variable], 100)
    else:
        mean_bg = background

    # Estimate random and systematic error of observations
    # Random noise (use scalar)
    var_rand = np.nanmean(data[variable_std].values)**2

    # TODO: estimate systemtic error from data (?)

    # Local mean, variance and number of valid pixels
    mean_s, variance, n_s = local_mean(
        data[variable], size=filter_size, kernel_type=filter_type,
        var_rand=var_rand
    )

    variance = variance + var_sys
    n_s = np.array(n_s, dtype='f4')

    # Z-test
    detected_plume = np.zeros(data[variable].shape + data['source'].shape,
                              dtype=bool)

    z_values, is_hit = do_test(mean_s, mean_bg, None, None,
                               n_s, q, variance=variance)

    # Label plumes
    labels = label_plumes(is_hit, min_plume_size)

    # Identify plumes intersecting with sources
    for j in range(data['source'].size):
        detected_plume[:,:,j] = find_plume_by_labels(data.lon, data.lat, labels,
                                                     data['lon_o'][j],
                                                     data['lat_o'][j],
                                                     data['radius'][j])

    # Dict with some additional info used for visualizing results
    attrs = {
        'trace_gas': variable,
        'probability for z-value': q,
        'filter_type':    filter_type,
        'filter_size':    filter_size,
        'trace_gas_uncertainty (random)':       np.sqrt(var_rand),
        'trace_gas_uncertainty (systematic)':   np.sqrt(var_sys),
    }
    data.attrs.update(attrs)

    dims = data[variable].dims

    data[f'{variable}_local_median'] = xarray.DataArray(mean_bg, dims=dims)
    data['z_values'] = xarray.DataArray(z_values, dims=dims)
    data['is_hit'] = xarray.DataArray(is_hit, dims=dims)
    data['labels'] = xarray.DataArray(labels, dims=dims)
    data[f'local_{variable}_mean'] = xarray.DataArray(mean_s, dims=dims)

    if n_s is not None:
        data[f'local_{variable}_pixels'] = xarray.DataArray(n_s, dims=dims)

    data['detected_plume'] = xarray.DataArray(detected_plume, dims=dims+('source',))
    
    return data
