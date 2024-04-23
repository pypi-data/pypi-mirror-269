
import cartopy.crs as ccrs
import numpy as np
import pandas as pd
import xarray as xr

import ddeq


def estimate_emissions(data, winds, sources, curves, gas,
                       variable='{gas}_minus_estimated_background_mass',
                       L_min=0, L_max=None, decay_time=np.nan,
                       min_pixel_number=10):
    """
    Estimate emissions using the integrated mass enhancement (IME) method.

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

    gas : str
        Gas for which emissions will be estimated.

    variable : str, optional
        Name of variable in `data` with gas enhancement above background in mass
        columns (units: kg m-2).

    L_min : float, optional
        Along-plume distance where mass integration starts. Default is the
        source location, i.e. L_min = 0.0.

    L_max : float, optional
        Along-plume distance where mass integration ends. Default is the plume
        length minus 10 km, but at least 10 km.

    decay_time : float, optional
        The decay time of the gas in seconds. If np.nan, no decay time is used.

    min_pixel_number : int, optional
        Minimum number of pixels needed for estimating emissions.

    Returns
    -------
    xr.Dataset
        Results dataset with estimated emissions for each source with additional
        parameters.
    """

    time = pd.Timestamp(data.time.values)
    results = {}

    extra_variables = [
        ('L_min', 'm'),
        ('L_max', 'm'),
        ('wind_speed', 'm s-1'),
        ('wind_speed_precision', 'm s-1'),
        ('wind_direction', '°'),
        ('decay_time', 's'),
        ('emissions_scaling_factor', '1'),
        ('integrated_{gas}_mass', 'kg'),
        ('integrated_{gas}_mass_precision', 'kg')
    ]

    for name, source in sources.groupby('source', squeeze=False):

        results[name] = ddeq.misc.init_results_dataset(
            source, [gas], extra_vars=extra_variables,
            method='integrated mass enhancement')

        if name not in data.source:
            continue

        this = ddeq.misc.select_source(data, source=name)

        # minimum number of detected pixles for IME approach
        if this['detected_plume'].sum() <= min_pixel_number:
            continue

        # no multiple sources
        if ddeq.misc.has_multiple_sources(data, name):
            continue

        # no upstream detections for non-cities
        if (
            str(this.type.values) != 'city' and
            sum(this.xp.values[this.detected_plume] < -2e3) > 5
        ):
            continue

        # plume area
        area = this['plume_area'].values

        # interpolate missing data
        vcd = this[variable.format(gas=gas)].values
        missing_data = np.isfinite(vcd)

        # fill cloud- and data-gaps
        kernel = ddeq.dplume.gaussian_kernel(sigma=2)
        vcd = np.where(np.isfinite(vcd), vcd,
                       ddeq.misc.normalized_convolution(vcd, kernel))

        # fraction of missing pixels in plume area
        fraction = np.sum(missing_data[area]) / np.sum(area)
        if fraction < 0.75:
            continue


        # plume length 10 km shorter than most distance detected pixel
        # but at least 10 km
        plume_length = np.max(this['xp'].values[area])

        if L_max is None:
            L_max = plume_length

            if L_max >= 20e3:
                L_max -= 10e3

        # reduce L_max if plume length is given byt larger than detected plume
        if L_max > plume_length:
            L_max = plume_length

        L = L_max - L_min
        L_std = 0.1 * L

        # any missing values remain in detected plume
        if np.sum(np.isnan(
            vcd[this['detected_plume'].values &
                (L_min <= this.xp) & (this.xp <= L_max)]
        )) > 0:
            continue


        # wind speed and its uncertainty
        wind = winds.sel(source=name)

        U = float(wind['speed'])
        D = float(wind['direction'])
        U_std = float(wind['speed_precision'])

        # don't estimate if angle between wind direction and center curve > 45°
        angle = ddeq.misc.compute_angle_between_curve_and_wind(
            curves[name], D, crs=ccrs.epsg(data.x.attrs['epsg'])
        )
        if np.abs(angle) > 45.0:
            flux = np.nan

        # compute integrated mass enhancement
        integration_area = area & (L_min <= this['xp']) & (this['xp'] <= L_max)
        A = data['pixel_area'].values
        ime = np.nansum(vcd[integration_area] * A[integration_area])

        if np.isnan(decay_time):
            flux = U / L * ime

            # uncertainty (considering IME, L and U)
            mass_std = this[f'{gas}_mass'].attrs.get('noise_level', np.nan)
            ime_std = np.mean(A[integration_area]) * mass_std * \
                      np.sqrt(np.sum(area))
            flux_std = 1.0 / L * np.sqrt(U**2 * ime_std**2 + ime**2 * U_std**2 +
                                       U**2 * ime**2 / L**2 * L_std**2)
        else:
            # correction factor
            L0 = U * decay_time
            c = decay_time * (np.exp(-L_min / L0) - np.exp(-L_max / L0))

            flux = ime / c

            # TODO
            ime_std = np.nan
            flux_std = np.nan

        results[name]['L_min'] = L_min
        results[name]['L_max'] = L_max
        results[name]['wind_speed'] = U
        results[name]['wind_speed_precision'] = U_std
        results[name]['wind_direction'] = D
        results[name][f'integrated_{gas}_mass'] = ime
        results[name][f'integrated_{gas}_mass_precision'] = ime_std

        # correction factors (for NO2 decay)
        results[name]['decay_time'] = decay_time

        results[name][f'{gas}_estimated_emissions'] = flux
        results[name][f'{gas}_estimated_emissions_precision'] = flux_std


    return xr.concat(results.values(), dim='source')

