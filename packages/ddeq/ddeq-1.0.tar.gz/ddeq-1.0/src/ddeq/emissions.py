
import numpy as np
import pandas
import xarray
import ucat
import ddeq


def compute_plume_signal(data, trace_gas):
    """
    Compute plume signal for trace gas
    """
    name = f'{trace_gas}_minus_estimated_background'
    signal = data[trace_gas] - data[f'{trace_gas}_estimated_background']

    data[name] = xarray.DataArray(signal, dims=data[trace_gas].dims,
                                  attrs=data[trace_gas].attrs)
    return data


def prepare_data(data, gas='CO2'):
    """
    The functions prepares `data` for emission quantification with includes
    estimating the background field, computing the local enhancement above the
    background (plume signal) and converting units to mass column densities
    (in kg m-2).

    Parameters
    ----------
    data : xr.Dataset
        Remote sensing dataset with trace gas variable.

    gas : str, optional
        Name of trace gas in in data.

    Returns
    -------
    xr.Dataset
        The dataset `data` with added background fields and variables with gas
        fields in mass column densities denoted with the "_mass" suffix.
    """
    data[f'{gas}_isfinite'] = np.isfinite(data[gas])

    # estimate background
    data = ddeq.background.estimate(data, gas)

    # compute CO2/NO2 enhancement
    data = compute_plume_signal(data, gas)

    # convert ppm to kg/m2
    for variable in [gas,
                     f'{gas}_estimated_background',
                     f'{gas}_minus_estimated_background']:

        values = data[variable]
        attrs = values.attrs

        name = f'{variable}_mass'

        if data[gas].attrs['units'] == 'molecules cm-2':
            input_unit = 'cm-2'
        elif data[gas].attrs['units'] == 'ppm':
            input_unit = 'ppmv'
        else:
            input_unit = str(data[gas].attrs['units'])

        if gas == 'NOx':
            molar_mass = 'NO2'
        else:
            molar_mass = str(gas)

        psurf = data['psurf'] if 'psurf' in data else data['suface_pressure']
        data[name] = xarray.DataArray(
            ucat.convert_columns(
                values, input_unit, 'kg m-2', p=psurf,
                molar_mass=molar_mass
            ),
            dims=values.dims, attrs=values.attrs
        )

        if 'noise_level' in attrs:
            noise_level = attrs['noise_level']

            # noise scenarios from SMARTCARB project
            if isinstance(noise_level, str):
                if gas == 'CO2':
                    noise_level = {
                        'low': 0.5,
                        'medium': 0.7,
                        'high': 1.0
                    }[noise_level]

                elif gas in ['NO2', 'NOx']:
                    noise_level = {
                        'low': 1.0e15,
                        'high': 2e15,
                        'S5': 1.3e15
                    }[noise_level]
                else:
                    raise ValueError

            attrs['noise_level'] = ucat.convert_columns(
                noise_level, input_unit, 'kg m-2', molar_mass=molar_mass,
                p=np.nanmean(psurf)
            )

        data[name].attrs.update(attrs)
        data[name].attrs['units'] = 'kg m-2'

    return data



def convert_NO2_to_NOx_emissions(results, f=1.32):
    """
    Convert NO2 fluxes/emissions (i.e. units: "kg s-1") to NOx fluxes/emissions
    using the NO2 to NOx conversion factor assuming that a fraction of NOx is in
    is nitrogen monoxide.

    Parameters
    ----------
    results : xr.Dataset
        Results dataset with estimated emissions.

    f : float, optional
        The scaling factor using a default value of 1.32.

    Returns
    -------
    xr.Dataset
        The results dataset with added variables for NOx emissions.
    """
    for key in results:
        if key.startswith('NO2') and results[key].attrs.get('units') == 'kg s-1':
            new_key = key.replace('NO2', 'NOx')
            results[new_key] = f * xarray.DataArray(results[key], dims=results[key].dims)
            results[new_key].attrs.update(results[key].attrs)

    return results
