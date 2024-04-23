

from scipy.special import erf
import scipy.integrate

import numpy as np



def point_plume_model(x, Q, x0=None):
    if x0 is None:
        return np.full(x.shape, Q)
    else:
        return Q * decay_function(x, 0.0, x0)


def city_plume_model(x, Q, sigma, x0=None, x_source=0.0, B=0.0, dx=1e3):
    """
    Function describes how flux changes when passing over an area source
    (e.g., city).

    x : along-plume distance (in meters)
    sigma: width of gaussian
    x_source : plume source
    x0: decay distance

    B: background
    """
    # high-resolution x-distance
    xhigh = np.arange(x[0]-50e3, x[-1]+200e3, dx)

    # decay function
    e = decay_function(xhigh, x_source, x0)

    # gaussian
    xgauss = np.arange(-50e3, +50e3+dx/2, dx)
    g = gauss(xgauss, 1.0, sigma, 0.0)

    # convolution
    f = scipy.ndimage.convolve(e, g, mode='nearest')

    # scaling with source strength assumed
    M = Q * f / f.max() + B

    # interpolate
    M = np.interp(x, xhigh, M)

    return M


class FixedGaussCurve:
    def __init__(self, sigma, shift):
        """\
        A Gauss curve with fixed standard width (sigma) and center position
        (shift).
        """
        self.sigma = sigma
        self.shift = shift

    def __call__(self, x, E0, slope=0.0, offset=0.0):
        return gauss(x, E0, self.sigma, self.shift, slope, offset)


def gauss(x, E0, sigma, shift, slope=0.0, offset=0.0):
    """
    """
    if np.isnan(slope):
        slope = 0.0
    if np.isnan(offset):
        offset = 0.0

    e = E0 / (sigma * np.sqrt(2.0 * np.pi)) * np.exp(-0.5 * ((x - shift) / sigma)**2)
    e += slope * x + offset

    return e


def decay_function(x, x_source, x0=None):
    """
    Exp. decay in x direction downstream of x_source with decay distance x0.
    """
    e = np.zeros_like(x)
    downstream = x > x_source

    if x0 is None:
        e[downstream] = 1.0
    else:
        e[downstream] = np.exp(-(x[downstream] - x_source) / x0)

    return e


def error_function(x, E0, sigma, box_width=20e3, shift=0.0, slope=0.0,
                   offset=0.0):
    """\
    An error function plus a linear function.

    The error function is the convolution of Gaussian and box function. The
    integral of the error function is E0.

    sigma - standard deivation of the Gaussian
    box_width - widht of the box function
    slope - slope of the linear function
    offset - offset of the linear function
    """
    delta = 0.5 * box_width
    a = sigma * np.sqrt(2.0)

    x1 = (x - shift + delta) / a
    x2 = (x - shift - delta) / a

    g = E0 * ( erf(x1) - erf(x2) ) / (4.0 * delta)
    g += x * slope + offset

    return g


class NO2toNOxConversion:
    def __init__(self, params, params_std):
        """
        Model to convert NO2 to NOx line densities using a negative exponential
        function.

        f(t) = m * np.exp(tau * t) + f

        Parameters
        ----------
        params : np.ndarray
            model parameters (m, tau and f)

        params_std : np.ndarray
            1-sigma uncertainty of model parameters
        """
        self.params = params
        self.params_std = params_std

    def neg_exp(self, t, m, tau, f):
        return m * np.exp(tau * t) + f

    # derivatives of neg_exp with respect to m, tau and f
    def _d_neg_exp_m(self, t, m, tau, f):
        return np.exp(tau * t)

    def _d_neg_exp_tau(self, t, m, tau, f):
        return m * t * np.exp(tau * t)

    def _d_neg_exp_f(self, t, m, tau, f):
        return np.repeat(1, len(t))

    def get_sigma(self, t, popt, pcov):
        return np.sqrt(
              self._d_neg_exp_m(t, *popt)**2 * pcov[0]**2
            + self._d_neg_exp_tau(t, *popt)**2 * pcov[1]**2
            + self._d_neg_exp_f(t, *popt)**2 * pcov[2]**2
        )

    def __call__(self, time):
        """\
        Compute scaling factors and their precision to convert NO2 to NOx line
        densities as a function of time since emissions.
        """
        f = self.neg_exp(time, *self.params)
        f_std = self.get_sigma(time, self.params, self.params_std)

        # set upstream values to background f0
        f[time < 0] = self.params[2]
        f_std[time < 0] = self.params_std[2]

        return f, f_std



def peak_model(Q, sigma_x, sigma_y, x0, y0, corr, B, grids):
    """
    Model that describes a peak in divergence map, which we want to fit at 
    each source

    Q = peak integral corresponding emission in kg/s
    sigma_x, sigma_y = deviations x and y directions in km
    x0, y0 = center of the peak
    corr = correlation between x and y dimensions
    theta = parameters that to be optimized
    B = Background in kg/m²/s
    grid = cropped grid around the source
    """
    # Kilometer grids
    X, Y = grids[0], grids[1]

    # Normalization
    N = Q / (2 * np.pi * sigma_x * sigma_y * np.sqrt(1 - corr**2))
    G = N * np.exp(
        - (X - x0)**2 / (2 * sigma_x**2 * (1 - corr**2))
        - (Y - y0)**2 / (2 * sigma_y**2 * (1 - corr**2))
        + corr * (X - x0) * (Y - y0) / (sigma_x * sigma_y * (1 - corr**2))
    ) + B

    return G
