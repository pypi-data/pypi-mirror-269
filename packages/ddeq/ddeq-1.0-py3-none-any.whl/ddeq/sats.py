
import glob
import os

import numpy as np
import pandas as pd
import xarray as xr
import scipy


_PSD_GROUP = 'PRODUCT/SUPPORT_DATA/DETAILED_RESULTS'
_PSG_GROUP = 'PRODUCT/SUPPORT_DATA/GEOLOCATIONS'
_PSI_GROUP = 'PRODUCT/SUPPORT_DATA/INPUT_DATA'



class Level2TropomiDataset:
    def __init__(self, pattern, root=''):
        """
        Level-2 class for TROPOMI NO2 product.

        Parameters
        ----------
        pattern : str
            A filename pattern used to match the TROPOMI files based on given
            date. Date formatting is used to find the correct file using, for
            example, "S5P_NO2_%Y%m%d.nc".

        root : str
            Data path to TROPOMI files.
        """
        self.pattern = os.path.join(root, pattern)

    def get_filenames(self, date):
        """
        foo
        """
        return sorted(glob.glob(date.strftime(self.pattern)))

    def read_date(self, date):
        """
        Returns a list of TROPOMI NO2 Level-2 data.

        Parameters
        ----------
        date : datetime.datetime

        Returns
        -------
        list of xr.Dataset
            List of TROPOMI datasets for given date.
        """
        return [
            xr.open_dataset(filename)
            for filename in self.get_filenames(date)
        ]


def read_level2(filename, product='nitrogendioxide_tropospheric_column',
                qa_threshold=0.75):
    """
    Read Tropomi NO2 fields. Works with version from NASA data portal.
    """
    data = xr.Dataset()

    with xr.open_dataset(filename) as nc_file:
        data.attrs.update(nc_file.attrs)

    with xr.open_dataset(filename, group='PRODUCT') as nc_file:
        data['time_utc'] = nc_file['time_utc'].copy()
        data['time_utc'] = data['time_utc'].astype('datetime64[ns]')

        data['lon'] = nc_file['longitude'].copy()
        data['lat'] = nc_file['latitude'].copy()

        # TODO: use independent estimate of standard deviation
        data['NO2'] = nc_file[product].copy()
        data['NO2_std'] = nc_file[f'{product}_precision'].copy()
        data['NO2_std'][:] = 14e-6

        data['qa_value'] = nc_file['qa_value'].copy()
        data['NO2'] = data['NO2'].where(data['qa_value'] > qa_threshold)

    with xr.open_dataset(filename, group=_PSG_GROUP) as nc_file:
        data['lonc'] = nc_file['longitude_bounds'].copy()
        data['latc'] = nc_file['latitude_bounds'].copy()

    with xr.open_dataset(filename, group=_PSD_GROUP) as nc_file:
        data['clouds'] = \
            nc_file['cloud_radiance_fraction_nitrogendioxide_window'].copy()

    # surface pressure in product from NASA portal is already in Pa
    # in contrast to user guide which claims hPa
    with xr.open_dataset(filename, group=_PSI_GROUP) as nc_file:
        data['psurf'] = nc_file['surface_pressure'].copy()

    return data



def read_S5P_NO2_matlab_file(filename):
    """
    Reads TROPOMI NO2 data from matlab files created in CoCO2 project.
    """
    F = scipy.io.loadmat(filename)

    time = np.asarray([pd.to_datetime(time)
        for time in F['time_utc'][:,0]])[:,0].astype('datetime64[ns]')

    shape = F['nitrogendioxide_tropospheric_column'].T.shape

    data = xr.Dataset(
      data_vars = dict(
          NO2 = (["nobs", "nrows"], F['nitrogendioxide_tropospheric_column'].T),
          NO2_std=(["nobs", "nrows"],
                   F['nitrogendioxide_tropospheric_column_precision'].T),
          latc=(["nobs", "nrows", "corner"], F['latitude_bounds'].T),
          lonc=(["nobs", "nrows", "corner"], F['longitude_bounds'].T),
          time_utc=(["nobs"], time ),
          psurf=(["nobs", "nrows"], F['surface_pressure'].T),
          clouds=(['nobs', 'nrows'], np.full(shape, 0.0))
      ),
      coords=dict(
          lat=(['nobs', 'nrows'], F['latitude'].T),
          lon=(['nobs', 'nrows'], F['longitude'].T),
          time=(time[0])
      ),
      attrs = dict(description="TROPOMI"),
    )
    data['NO2'].attrs.update({"cloud_threshold": 0.30,
                              "units": 'mol m-2',
                             "noise_level": 15e-6,
                             })
    data['NO2_std'][:] = 15e-6
    data['NO2_std'].attrs.update({"cloud_threshold": 0.30,
                                  "units": 'mol m-2'})

    data['NO2'].values[F['qa_value'].T < 0.75] = np.nan
    data['NO2_std'].values[F['qa_value'].T < 0.75] = np.nan

    return data