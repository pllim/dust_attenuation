import numpy as np
import pytest

import astropy.units as u
from astropy.modeling import InputParameterError

from ..radiative_transfer import WG00
from .helpers import _invalid_x_range


@pytest.mark.parametrize("tau_V_invalid", [-1.0, 0.2, 100])
def test_invalid_tau_v_input(tau_V_invalid):
    with pytest.raises(InputParameterError) as exc:
        tmodel = WG00(tau_V=tau_V_invalid)
    assert exc.value.args[0] == 'parameter tau_V must be between 0.25 and 50.0'


@pytest.mark.parametrize("x_invalid", [-1.0, 0.05, 10.1, 100.])
def test_invalid_wavenumbers(x_invalid):
    _invalid_x_range(x_invalid, WG00(tau_V=1), 'WG00')


@pytest.mark.parametrize("x_invalid_wavenumber",
                         [-1.0, 0.05, 10.1, 100.]/u.micron)
def test_invalid_wavenumbers_imicron(x_invalid_wavenumber):
    _invalid_x_range(x_invalid_wavenumber, WG00(tau_V=1), 'WG00')


@pytest.mark.parametrize("x_invalid_micron",
                         u.micron/[-1.0, 0.05, 10.1, 100.])
def test_invalid_micron(x_invalid_micron):
    _invalid_x_range(x_invalid_micron, WG00(tau_V=1), 'WG00')


@pytest.mark.parametrize("x_invalid_angstrom",
                         u.angstrom*1e4/[-1.0, 0.05, 10.1, 100.])
def test_invalid_angstrom(x_invalid_angstrom):
    _invalid_x_range(x_invalid_angstrom, WG00(tau_V=1), 'WG00')


def get_taux_cor_vals(tauV, geo, dust, distrib):
    # correct values are taken from the publicly available tables
    # of Witt & Gordon (2000, ApJ, Volume 528, pp. 799-816)

    # ensure parameters are lower cases
    geo = geo.lower()
    dust = dust.lower()
    distrib = distrib.lower()

    # testing wavelengths
    x = np.array([1000., 1142., 1285., 1428., 1571., 1714., 1857., 2000.,
                  2142., 2285., 2428., 2571., 2714., 2857., 3000., 3776.,
                  4754., 5985., 7535., 9487., 11943., 15036., 18929.,
                  23830., 30001])

    # add units
    x = x*1e-4 * u.micron

    # correct values
    if dust == 'smc':
        if geo == 'shell':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([1.677, 1.188, 0.927, 0.757, 0.646,
                                         0.560, 0.503, 0.459, 0.424, 0.392,
                                         0.365, 0.342, 0.321, 0.295, 0.280,
                                         0.228, 0.174, 0.126, 0.090, 0.061,
                                         0.039, 0.025, 0.018, 0.010, 0.008])
                elif tauV == 1.0:
                    cor_vals = np.array([7.070, 5.083, 3.987, 3.275, 2.809,
                                         2.446, 2.198, 2.000, 1.846, 1.703,
                                         1.578, 1.474, 1.381, 1.268, 1.202,
                                         0.975, 0.736, 0.528, 0.376, 0.249,
                                         0.161, 0.099, 0.069, 0.049, 0.021])
                elif tauV == 10.0:
                    cor_vals = np.array([95.924, 74.314, 60.329, 40.619,
                                         28.683, 26.403, 26.022, 23.075,
                                         19.489, 19.894, 18.844, 18.153,
                                         16.263, 15.311, 14.386, 11.601,
                                         8.842, 6.337, 4.525, 2.971, 1.849,
                                         1.103, 0.75, 0.514, 0.225])
                elif tauV == 50.0:
                    cor_vals = np.array([0.000, 0.000, 0.000, 0.000, 0.000,
                                         0.000, 0.000, 0.000, 0.000, 0.000,
                                         0.000, 0.000, 0.000, 106.015, 100.498,
                                         80.488, 61.764, 40.317, 28.576,
                                         18.196, 10.668, 6.377, 4.291, 2.913,
                                         1.229])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([1.197, 0.928, 0.759, 0.64, 0.559,
                                         0.494, 0.447, 0.412, 0.384, 0.358,
                                         0.335, 0.315, 0.297, 0.275, 0.261,
                                         0.215, 0.165, 0.121, 0.088, 0.059,
                                         0.038, 0.024, 0.017, 0.012, 0.005])
                elif tauV == 1.0:
                    cor_vals = np.array([2.502, 2.194, 1.978, 1.784, 1.640,
                                         1.510, 1.414, 1.330, 1.262, 1.194,
                                         1.134, 1.078, 1.026, 0.966, 0.927,
                                         0.787, 0.621, 0.466, 0.345, 0.234,
                                         0.154, 0.096, 0.067, 0.047, 0.021])
                elif tauV == 10.0:
                    cor_vals = np.array([6.974, 5.758, 5.070, 4.603, 4.290,
                                         4.048, 3.857, 3.731, 3.617, 3.506,
                                         3.421, 3.338, 3.253, 3.168, 3.110,
                                         2.897, 2.640, 2.353, 2.047, 1.666,
                                         1.256, 0.865, 0.632, 0.456, 0.212])
                elif tauV == 50.0:
                    cor_vals = np.array([29.007, 20.918, 15.608, 13.969,
                                         12.009, 11.134, 10.418, 9.755,
                                         9.240, 8.592, 8.193, 7.821, 7.464,
                                         7.110, 6.880, 6.059, 5.182, 4.432,
                                         3.825, 3.269, 2.798, 2.355, 2.009,
                                         1.658, 0.943])

        elif geo == 'cloudy':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.372, 0.304, 0.258, 0.222, 0.197,
                                         0.176, 0.162, 0.149, 0.140, 0.131,
                                         0.123, 0.116, 0.112, 0.102, 0.098,
                                         0.082, 0.063, 0.047, 0.034, 0.023,
                                         0.015, 0.009, 0.007, 0.005, 0.002])
                elif tauV == 1.0:
                    cor_vals = np.array([0.581, 0.544, 0.512, 0.481, 0.455,
                                         0.429, 0.410, 0.392, 0.378, 0.364,
                                         0.350, 0.337, 0.325, 0.308, 0.299,
                                         0.261, 0.214, 0.166, 0.126, 0.088,
                                         0.059, 0.037, 0.026, 0.019, 0.008])
                elif tauV == 10.0:
                    cor_vals = np.array([0.682, 0.674, 0.670, 0.665, 0.656,
                                         0.650, 0.646, 0.642, 0.638, 0.636,
                                         0.632, 0.629, 0.626, 0.621, 0.616,
                                         0.604, 0.581, 0.549, 0.510, 0.451,
                                         0.372, 0.280, 0.216, 0.162, 0.080])
                elif tauV == 50.0:
                    cor_vals = np.array([0.697, 0.694, 0.688, 0.692, 0.688,
                                         0.688, 0.685, 0.680, 0.680, 0.680,
                                         0.678, 0.678, 0.678, 0.676, 0.674,
                                         0.667, 0.663, 0.650, 0.643, 0.620,
                                         0.591, 0.548, 0.505, 0.451, 0.300])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.330, 0.277, 0.241, 0.211, 0.190,
                                         0.170, 0.157, 0.147, 0.138, 0.130,
                                         0.123, 0.116, 0.110, 0.103, 0.098,
                                         0.083, 0.065, 0.048, 0.036, 0.024,
                                         0.016, 0.010, 0.007, 0.005, 0.002])
                elif tauV == 1.0:
                    cor_vals = np.array([0.481, 0.451, 0.429, 0.408, 0.389,
                                         0.370, 0.356, 0.343, 0.332, 0.322,
                                         0.311, 0.301, 0.294, 0.281, 0.273,
                                         0.243, 0.204, 0.161, 0.125, 0.089,
                                         0.060, 0.039, 0.027, 0.020, 0.009])
                elif tauV == 10.0:
                    cor_vals = np.array([0.605, 0.588, 0.570, 0.560, 0.550,
                                         0.543, 0.538, 0.533, 0.531, 0.524,
                                         0.520, 0.521, 0.515, 0.511, 0.507,
                                         0.498, 0.480, 0.457, 0.429, 0.385,
                                         0.327, 0.257, 0.205, 0.158, 0.081])
                elif tauV == 50.0:
                    cor_vals = np.array([0.665, 0.654, 0.645, 0.637, 0.627,
                                         0.621, 0.617, 0.613, 0.610, 0.606,
                                         0.600, 0.600, 0.598, 0.596, 0.588,
                                         0.579, 0.564, 0.549, 0.530, 0.512,
                                         0.488, 0.455, 0.425, 0.386, 0.273])

        elif geo == 'dusty':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.887, 0.671, 0.543, 0.455, 0.393,
                                         0.345, 0.313, 0.287, 0.267, 0.249,
                                         0.232, 0.218, 0.206, 0.190, 0.181,
                                         0.149, 0.115, 0.084, 0.061, 0.041,
                                         0.027, 0.017, 0.012, 0.008, 0.003])
                elif tauV == 1.0:
                    cor_vals = np.array([2.107, 1.780, 1.551, 1.373, 1.238,
                                         1.129, 1.046, 0.977, 0.922, 0.870,
                                         0.823, 0.779, 0.740, 0.691, 0.661,
                                         0.558, 0.437, 0.324, 0.238, 0.161,
                                         0.106, 0.066, 0.047, 0.033, 0.015])
                elif tauV == 10.0:
                    cor_vals = np.array([4.423, 4.107, 3.841, 3.629, 3.474,
                                         3.340, 3.233, 3.142, 3.076, 2.985,
                                         2.921, 2.867, 2.807, 2.728, 2.668,
                                         2.478, 2.203, 1.910, 1.602, 1.247,
                                         0.911, 0.610, 0.441, 0.316, 0.146])
                elif tauV == 50.0:
                    cor_vals = np.array([6.052, 5.636, 5.437, 5.256, 5.091,
                                         4.989, 4.858, 4.767, 4.693, 4.628,
                                         4.556, 4.468, 4.417, 4.335, 4.301,
                                         4.107, 3.813, 3.501, 3.186, 2.782,
                                         2.359, 1.900, 1.555, 1.242, 0.669])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.733, 0.578, 0.481, 0.409, 0.359,
                                         0.318, 0.290, 0.268, 0.250, 0.234,
                                         0.219, 0.206, 0.196, 0.181, 0.173,
                                         0.143, 0.111, 0.081, 0.059, 0.040,
                                         0.026, 0.016, 0.012, 0.008, 0.003])
                elif tauV == 1.0:
                    cor_vals = np.array([1.411, 1.253, 1.135, 1.037, 0.958,
                                         0.892, 0.834, 0.791, 0.753, 0.719,
                                         0.686, 0.655, 0.629, 0.593, 0.570,
                                         0.490, 0.394, 0.300, 0.224, 0.154,
                                         0.103, 0.065, 0.045, 0.032, 0.014])
                elif tauV == 10.0:
                    cor_vals = np.array([2.379, 2.188, 2.074, 1.988, 1.924,
                                         1.865, 1.821, 1.791, 1.762, 1.741,
                                         1.718, 1.680, 1.663, 1.628, 1.612,
                                         1.543, 1.438, 1.306, 1.153, 0.957,
                                         0.743, 0.530, 0.398, 0.293, 0.140])
                elif tauV == 50.0:
                    cor_vals = np.array([3.566, 3.281, 3.079, 2.911, 2.807,
                                         2.714, 2.640, 2.578, 2.530, 2.486,
                                         2.444, 2.396, 2.371, 2.324, 2.301,
                                         2.194, 2.070, 1.926, 1.808, 1.655,
                                         1.497, 1.299, 1.132, 0.956, 0.575])

    elif dust == 'mw':
        if geo == 'shell':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([1.002, 0.655, 0.468, 0.374, 0.336,
                                         0.330, 0.361, 0.457, 0.568, 0.503,
                                         0.394, 0.329, 0.294, 0.270, 0.254,
                                         0.216, 0.168, 0.129, 0.096, 0.061,
                                         0.044, 0.032, 0.022, 0.016, 0.010])
                elif tauV == 1.0:
                    cor_vals = np.array([4.146, 2.750, 1.992, 1.600, 1.444,
                                         1.418, 1.548, 1.942, 2.386, 2.123,
                                         1.672, 1.401, 1.252, 1.151, 1.085,
                                         0.921, 0.711, 0.544, 0.402, 0.252,
                                         0.181, 0.128, 0.089, 0.064, 0.046])
                elif tauV == 10.0:
                    cor_vals = np.array([53.322, 31.335, 24.372, 19.092,
                                         17.299, 16.716, 18.468, 22.657,
                                         27.293, 22.778, 20.205, 15.946,
                                         14.418, 13.263, 12.796, 10.948,
                                         8.615, 6.564, 4.825, 3.015, 2.099,
                                         1.444, 0.986, 0.691, 0.485])
                elif tauV == 50.0:
                    cor_vals = np.array([0.000, 0.000, 0.000, 0.000, 0.000,
                                         0.000, 0.000, 0.000, 0.000, 0.000,
                                         0.000, 110.43, 100.063, 94.504,
                                         90.384, 76.520, 59.569, 46.469,
                                         30.557, 17.523, 11.821, 8.239, 5.688,
                                         3.944, 2.73])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.813, 0.567, 0.421, 0.342, 0.310,
                                         0.306, 0.332, 0.412, 0.499, 0.449,
                                         0.360, 0.304, 0.273, 0.253, 0.239,
                                         0.205, 0.160, 0.125, 0.093, 0.060,
                                         0.043, 0.031, 0.022, 0.015, 0.011])
                elif tauV == 1.0:
                    cor_vals = np.array([2.036, 1.643, 1.336, 1.148, 1.066,
                                         1.052, 1.118, 1.312, 1.503, 1.395,
                                         1.186, 1.043, 0.960, 0.900, 0.857,
                                         0.752, 0.605, 0.479, 0.366, 0.237,
                                         0.172, 0.123, 0.087, 0.062, 0.045])
                elif tauV == 10.0:
                    cor_vals = np.array([5.161, 4.221, 3.731, 3.433, 3.318,
                                         3.290, 3.391, 3.678, 3.990, 3.807,
                                         3.489, 3.257, 3.155, 3.062, 3.001,
                                         2.852, 2.617, 2.380, 2.106, 1.675,
                                         1.363, 1.059, 0.792, 0.589, 0.433])
                elif tauV == 50.0:
                    cor_vals = np.array([16.324, 12.203, 9.364, 8.169, 7.654,
                                         7.542, 7.984, 9.130, 10.430, 9.721,
                                         8.375, 7.413, 6.996, 6.689, 6.452,
                                         5.870, 5.128, 4.489, 3.929, 3.297,
                                         2.915, 2.580, 2.253, 1.935, 1.601])

        elif geo == 'cloudy':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.276, 0.202, 0.153, 0.126, 0.115,
                                         0.113, 0.123, 0.150, 0.180, 0.163,
                                         0.132, 0.113, 0.102, 0.095, 0.090,
                                         0.078, 0.061, 0.048, 0.036, 0.023,
                                         0.017, 0.012, 0.009, 0.006, 0.004])
                elif tauV == 1.0:
                    cor_vals = np.array([0.530, 0.462, 0.399, 0.355, 0.333,
                                         0.331, 0.348, 0.395, 0.435, 0.413,
                                         0.365, 0.330, 0.308, 0.292, 0.280,
                                         0.252, 0.208, 0.170, 0.133, 0.089,
                                         0.066, 0.047, 0.034, 0.024, 0.018])
                elif tauV == 10.0:
                    cor_vals = np.array([0.683, 0.660, 0.646, 0.633, 0.626,
                                         0.626, 0.634, 0.644, 0.658, 0.649,
                                         0.639, 0.632, 0.621, 0.619, 0.610,
                                         0.604, 0.578, 0.552, 0.517, 0.453,
                                         0.393, 0.328, 0.260, 0.203, 0.154])
                elif tauV == 50.0:
                    cor_vals = np.array([0.696, 0.692, 0.687, 0.682, 0.678,
                                         0.680, 0.681, 0.687, 0.689, 0.686,
                                         0.681, 0.680, 0.676, 0.674, 0.671,
                                         0.667, 0.661, 0.650, 0.641, 0.620,
                                         0.604, 0.573, 0.535, 0.492, 0.442])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.255, 0.193, 0.150, 0.125, 0.115,
                                         0.113, 0.122, 0.147, 0.174, 0.159,
                                         0.131, 0.113, 0.103, 0.095, 0.091,
                                         0.079, 0.063, 0.050, 0.038, 0.024,
                                         0.018, 0.013, 0.009, 0.006, 0.005])
                elif tauV == 1.0:
                    cor_vals = np.array([0.443, 0.393, 0.350, 0.317, 0.301,
                                         0.297, 0.311, 0.345, 0.375, 0.359,
                                         0.324, 0.297, 0.280, 0.268, 0.258,
                                         0.235, 0.199, 0.165, 0.131, 0.089,
                                         0.067, 0.049, 0.035, 0.025, 0.019])
                elif tauV == 10.0:
                    cor_vals = np.array([0.577, 0.557, 0.539, 0.523, 0.518,
                                         0.517, 0.523, 0.537, 0.550, 0.544,
                                         0.529, 0.517, 0.510, 0.504, 0.503,
                                         0.491, 0.476, 0.460, 0.433, 0.386,
                                         0.344, 0.296, 0.241, 0.193, 0.151])
                elif tauV == 50.0:
                    cor_vals = np.array([0.653, 0.635, 0.617, 0.607, 0.599,
                                         0.601, 0.603, 0.617, 0.631, 0.623,
                                         0.610, 0.601, 0.595, 0.590, 0.586,
                                         0.575, 0.565, 0.548, 0.534, 0.511,
                                         0.496, 0.472, 0.447, 0.416, 0.378])

        elif geo == 'dusty':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.589, 0.402, 0.295, 0.238, 0.215,
                                         0.212, 0.230, 0.289, 0.353, 0.315,
                                         0.251, 0.211, 0.190, 0.175, 0.165,
                                         0.141, 0.111, 0.086, 0.065, 0.041,
                                         0.030, 0.021, 0.015, 0.011, 0.008])
                elif tauV == 1.0:
                    cor_vals = np.array([1.624, 1.254, 0.991, 0.837, 0.770,
                                         0.759, 0.815, 0.976, 1.137, 1.044,
                                         0.870, 0.755, 0.689, 0.641, 0.609,
                                         0.531, 0.423, 0.333, 0.253, 0.163,
                                         0.119, 0.085, 0.060, 0.043, 0.031])
                elif tauV == 10.0:
                    cor_vals = np.array([3.904, 3.498, 3.166, 2.955, 2.849,
                                         2.826, 2.913, 3.137, 3.350, 3.233,
                                         2.995, 2.824, 2.720, 2.637, 2.582,
                                         2.416, 2.177, 1.932, 1.663, 1.257,
                                         0.997, 0.756, 0.556, 0.411, 0.299])
                elif tauV == 50.0:
                    cor_vals = np.array([5.543, 5.111, 4.791, 4.565, 4.486,
                                         4.451, 4.543, 4.799, 4.988, 4.858,
                                         4.628, 4.449, 4.338, 4.239, 4.193,
                                         4.017, 3.786, 3.514, 3.240, 2.800,
                                         2.468, 2.136, 1.801, 1.487, 1.192])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.517, 0.366, 0.274, 0.225, 0.204,
                                         0.201, 0.218, 0.270, 0.325, 0.293,
                                         0.236, 0.200, 0.181, 0.167, 0.158,
                                         0.136, 0.107, 0.084, 0.063, 0.040,
                                         0.029, 0.021, 0.015, 0.011, 0.008])
                elif tauV == 1.0:
                    cor_vals = np.array([1.181, 0.968, 0.805, 0.696, 0.648,
                                         0.642, 0.682, 0.791, 0.896, 0.837,
                                         0.720, 0.640, 0.592, 0.556, 0.531,
                                         0.469, 0.383, 0.308, 0.236, 0.156,
                                         0.115, 0.083, 0.058, 0.042, 0.030])
                elif tauV == 10.0:
                    cor_vals = np.array([2.122, 1.935, 1.799, 1.721, 1.681,
                                         1.672, 1.704, 1.789, 1.874, 1.835,
                                         1.744, 1.682, 1.633, 1.602, 1.583,
                                         1.520, 1.428, 1.319, 1.185, 0.961,
                                         0.802, 0.638, 0.489, 0.372, 0.278])
                elif tauV == 50.0:
                    cor_vals = np.array([3.139, 2.825, 2.599, 2.462, 2.393,
                                         2.395, 2.442, 2.578, 2.728, 2.637,
                                         2.490, 2.380, 2.321, 2.282, 2.242,
                                         2.167, 2.050, 1.951, 1.827, 1.658,
                                         1.535, 1.405, 1.257, 1.095, 0.931])

    else:
        cor_vals = np.array([0.0])

    return (x, cor_vals)


@pytest.mark.parametrize("tauV", [0.25, 1.0, 10.0, 50.0])
@pytest.mark.parametrize("geometries", ['shell', 'cloudy', 'dusty'])
@pytest.mark.parametrize("dust_types", ['smc', 'mw'])
@pytest.mark.parametrize("dust_distribs", ['homogeneous', 'clumpy'])
def test_WG00_values(tauV, geometries, dust_types, dust_distribs):
    # get the correct values
    x, cor_vals = get_taux_cor_vals(tauV, geometries, dust_types,
                                    dust_distribs)
    # initialize model
    tmodel = WG00(tauV, geometry=geometries, dust_type=dust_types,
                  dust_distribution=dust_distribs)

    # test taux
    np.testing.assert_allclose(tmodel(x), cor_vals*1.086, atol=1e-10)


@pytest.mark.parametrize("tauV", [0.25, 1.0, 10.0, 50.0])
@pytest.mark.parametrize("geometries", ['shell', 'cloudy', 'dusty'])
@pytest.mark.parametrize("dust_types", ['smc', 'mw'])
@pytest.mark.parametrize("dust_distribs", ['homogeneous', 'clumpy'])
def test_attenuation_WG00_attenuate_values(tauV, geometries, dust_types,
                                           dust_distribs):

    # get the correct values
    x, cor_vals = get_taux_cor_vals(tauV, geometries, dust_types,
                                    dust_distribs)

    # calculate the cor_vals in fractional units
    cor_vals = np.power(10.0, -0.4*(cor_vals*1.086))

    # initialize model
    tmodel = WG00(tauV, geometry=geometries, dust_type=dust_types,
                  dust_distribution=dust_distribs)

    # test
    np.testing.assert_allclose(tmodel.attenuate(x), cor_vals, atol=1e-10)

@pytest.mark.parametrize("dust_type", ['smc', 'mw'])
def test_extinction(dust_type):
    # correct values are taken from the publicly available tables
    # of Witt & Gordon (2000, ApJ, Volume 528, pp. 799-816)

    # ensure parameters are lower cases
    dust_type = dust_type.lower()

    # testing wavelengths
    x = np.array([1000., 1142., 1285., 1428., 1571., 1714., 1857., 2000.,
                  2142., 2285., 2428., 2571., 2714., 2857., 3000., 3776.,
                  4754., 5985., 7535., 9487., 11943., 15036., 18929.,
                  23830., 30001])

    # add units
    x = x*1e-4 * u.micron

    tmodel = WG00(1,dust_type=dust_type)

    if dust_type == 'mw':
        tau_tauV = np.array([5.238, 3.918, 3.182, 2.780, 2.584, 2.509,
                                2.561, 2.843, 3.190, 2.910, 2.472, 2.194,
                                2.022, 1.905, 1.818, 1.527, 1.199, 0.909,
                                0.667, 0.440, 0.304, 0.210, 0.145, 0.100,
                                0.069])
    elif dust_type == 'smc':
        tau_tauV = np.array([9.675, 7.440, 6.068, 5.167, 4.536, 4.074,
                             3.700, 3.379, 3.101, 2.857, 2.642, 2.452,
                             2.282, 2.133, 2.031, 1.610, 1.221, 0.880,
                             0.630, 0.430, 0.272, 0.166, 0.111, 0.075,
                             0.033])

    np.testing.assert_allclose(tau_tauV, tmodel.get_extinction(x, 1)/1.086)

@pytest.mark.parametrize("dust_type", ['smc', 'mw'])
def test_albedo(dust_type):
    # correct values are taken from the publicly available tables
    # of Witt & Gordon (2000, ApJ, Volume 528, pp. 799-816)

    # ensure parameters are lower cases
    dust_type = dust_type.lower()

    # testing wavelengths
    x = np.array([1000., 1142., 1285., 1428., 1571., 1714., 1857., 2000.,
                  2142., 2285., 2428., 2571., 2714., 2857., 3000., 3776.,
                  4754., 5985., 7535., 9487., 11943., 15036., 18929.,
                  23830., 30001])

    # add units
    x = x*1e-4 * u.micron

    tmodel = WG00(1,dust_type=dust_type)

    if dust_type == 'mw':
        albedo = np.array([0.320, 0.409, 0.481, 0.526, 0.542, 0.536, 0.503,
                           0.432, 0.371, 0.389, 0.437, 0.470, 0.486, 0.499,
                           0.506, 0.498, 0.502, 0.491, 0.481, 0.500, 0.473,
                           0.457, 0.448, 0.424, 0.400])

    elif dust_type == 'smc':
        albedo = np.array([0.400, 0.449, 0.473, 0.494, 0.508, 0.524, 0.529,
                           0.528, 0.523, 0.520, 0.516, 0.511, 0.505, 0.513,
                           0.515, 0.498, 0.494, 0.489, 0.484, 0.493, 0.475,
                           0.465, 0.439, 0.417, 0.400 ])

    np.testing.assert_allclose(albedo, tmodel.get_albedo(x))


@pytest.mark.parametrize("dust_type", ['smc', 'mw'])
def test_scattering_phase_function(dust_type):
    # correct values are taken from the publicly available tables
    # of Witt & Gordon (2000, ApJ, Volume 528, pp. 799-816)

    # ensure parameters are lower cases
    dust_type = dust_type.lower()

    # testing wavelengths
    x = np.array([1000., 1142., 1285., 1428., 1571., 1714., 1857., 2000.,
                  2142., 2285., 2428., 2571., 2714., 2857., 3000., 3776.,
                  4754., 5985., 7535., 9487., 11943., 15036., 18929.,
                  23830., 30001])

    # add units
    x = x*1e-4 * u.micron

    tmodel = WG00(1,dust_type=dust_type)

    if dust_type == 'mw':
        g = np.array([0.800, 0.783, 0.767, 0.756, 0.745, 0.736, 0.727,
                      0.720, 0.712, 0.707, 0.702, 0.697, 0.691, 0.685,
                      0.678, 0.646, 0.624, 0.597, 0.563, 0.545, 0.533,
                      0.511, 0.480, 0.445, 0.420])

    elif dust_type == 'smc':
        g = np.array([0.800, 0.783, 0.767, 0.756, 0.745, 0.736, 0.727,
                      0.720, 0.712, 0.707, 0.702, 0.697, 0.691, 0.685,
                      0.678, 0.646, 0.624, 0.597, 0.563, 0.545, 0.533,
                      0.511, 0.480, 0.445, 0.420])

    np.testing.assert_allclose(g, tmodel.get_scattering_phase_function(x))



def get_fsca_corr_vals(tauV, geo, dust, distrib):
    # correct values are taken from the publicly available tables
    # of Witt & Gordon (2000, ApJ, Volume 528, pp. 799-816)

    # ensure parameters are lower cases
    geo = geo.lower()
    dust = dust.lower()
    distrib = distrib.lower()

    # testing wavelengths
    x = np.array([1000., 1428., 1857., 2285., 2714., 3776., 7535.,
                  9487., 18929., 30001])

    # add units
    x = x*1e-4 * u.micron

    # correct values
    if dust == 'smc':
        if geo == 'shell':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.115, 0.225, 0.241, 0.218, 0.19,
                                         0.153, 0.0722, 0.0526, 0.013,
                                         0.00359])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.105, 0.183, 0.2, 0.184, 0.164,
                                         0.136, 0.0679, 0.0503, 0.0127,
                                         0.00354])

        if geo == 'dusty':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.129, 0.183, 0.183, 0.161, 0.138,
                                         0.109, 0.0502, 0.0364, 0.00895,
                                         0.00247])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.104, 0.153, 0.158, 0.141, 0.123,
                                         0.0993, 0.0481, 0.0353, 0.00879,
                                         0.00243])

        if geo == 'cloudy':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.063, 0.0948, 0.0978, 0.0868,
                                         0.0759, 0.0603, 0.0284, 0.0207,
                                         0.00512, 0.00141])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.0484, 0.0779, 0.0838, 0.0769,
                                         0.0683, 0.0568, 0.0286, 0.0212,
                                         0.00538, 0.0015])
    elif dust == 'mw':
        if geo == 'shell':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.128, 0.221, 0.201, 0.154, 0.171,
                                         0.148, 0.0752, 0.0545, 0.0172,
                                         0.00744])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.103, 0.187, 0.171, 0.129, 0.149,
                                         0.132, 0.0706, 0.0521, 0.0168,
                                         0.00731])

        if geo == 'dusty':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.107, 0.162, 0.147, 0.115, 0.123,
                                         0.105, 0.0524, 0.0377, 0.0118,
                                         0.00511])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.0884, 0.142, 0.13, 0.1, 0.111,
                                         0.0961, 0.05, 0.0365, 0.0116,
                                         0.00503])

        if geo == 'cloudy':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.0545, 0.0873, 0.0796, 0.0618,
                                         0.0674, 0.0582, 0.0297, 0.0215,
                                         0.00677, 0.00293])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.0437, 0.0776, 0.0712, 0.0539,
                                         0.0619, 0.0551, 0.0297, 0.0219,
                                         0.00709, 0.00309])

    return x, cor_vals
@pytest.mark.parametrize("tauV", [0.25])
@pytest.mark.parametrize("geometries", ['shell', 'cloudy', 'dusty'])
@pytest.mark.parametrize("dust_types", ['smc', 'mw'])
@pytest.mark.parametrize("dust_distribs", ['homogeneous', 'clumpy'])
def test_fsca_WG00(tauV, geometries, dust_types, dust_distribs):
    # get the correct values
    x, cor_vals = get_fsca_corr_vals(tauV, geometries, dust_types, dust_distribs)

    # initialize model
    tmodel = WG00(tauV, geometry=geometries, dust_type=dust_types,
                  dust_distribution=dust_distribs)

    # test
    np.testing.assert_allclose(tmodel.get_fsca(x, tauV), cor_vals, atol=1e-10)


def get_fdir_corr_vals(tauV, geo, dust, distrib):
    # correct values are taken from the publicly available tables
    # of Witt & Gordon (2000, ApJ, Volume 528, pp. 799-816)

    # ensure parameters are lower cases
    geo = geo.lower()
    dust = dust.lower()
    distrib = distrib.lower()

    # testing wavelengths
    x = np.array([1000., 1428., 1857., 2285., 2714., 3776., 7535.,
                  9487., 18929., 30001])

    # add units
    x = x*1e-4 * u.micron

    # correct values
    if dust == 'smc':
        if geo == 'shell':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.0717, 0.244, 0.363, 0.457, 0.535,
                                        0.643, 0.841, 0.889, 0.969, 0.988])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.197, 0.344, 0.44, 0.515, 0.579,
                                         0.67, 0.848, 0.892, 0.971, 0.991])

        if geo == 'dusty':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.283, 0.451, 0.548, 0.619, 0.676,
                                         0.753, 0.891, 0.924, 0.98, 0.994])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.376, 0.511, 0.591, 0.65, 0.699,
                                         0.768, 0.894, 0.926, 0.98, 0.994])

        if geo == 'cloudy':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.626, 0.706, 0.753, 0.79, 0.819,
                                         0.862, 0.938, 0.956, 0.988, 0.997])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.67, 0.732, 0.771, 0.801, 0.827,
                                         0.864, 0.936, 0.955, 0.988, 0.996])

    elif dust == 'mw':
        if geo == 'shell':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.239, 0.467, 0.496, 0.451, 0.575,
                                         0.658, 0.833, 0.886, 0.962, 0.983])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.34, 0.523, 0.546, 0.51, 0.612,
                                         0.683, 0.84, 0.89, 0.962, 0.982])

        if geo == 'dusty':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.448, 0.626, 0.648, 0.614, 0.704,
                                         0.763, 0.885, 0.922, 0.973, 0.987])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.508, 0.656, 0.674, 0.646, 0.724,
                                         0.777, 0.889, 0.924, 0.974, 0.987])

        if geo == 'cloudy':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.704, 0.794, 0.805, 0.788, 0.835,
                                         0.867, 0.935, 0.955, 0.985, 0.993])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.731, 0.805, 0.814, 0.799, 0.84,
                                         0.869, 0.933, 0.954, 0.984, 0.992])

    return x, cor_vals

@pytest.mark.parametrize("tauV", [0.25])
@pytest.mark.parametrize("geometries", ['shell', 'cloudy', 'dusty'])
@pytest.mark.parametrize("dust_types", ['smc', 'mw'])
@pytest.mark.parametrize("dust_distribs", ['homogeneous', 'clumpy'])
def test_fdir_WG00(tauV, geometries, dust_types, dust_distribs):
    # get the correct values
    x, cor_vals = get_fdir_corr_vals(tauV, geometries, dust_types, dust_distribs)

    # initialize model
    tmodel = WG00(tauV, geometry=geometries, dust_type=dust_types,
                  dust_distribution=dust_distribs)

    # test
    np.testing.assert_allclose(tmodel.get_fdir(x, tauV), cor_vals, atol=1e-10)


def get_fesc_corr_vals(tauV, geo, dust, distrib):
    # correct values are taken from the publicly available tables
    # of Witt & Gordon (2000, ApJ, Volume 528, pp. 799-816)

    # ensure parameters are lower cases
    geo = geo.lower()
    dust = dust.lower()
    distrib = distrib.lower()

    # testing wavelengths
    x = np.array([1000., 1428., 1857., 2285., 2714., 3776., 7535.,
                  9487., 18929., 30001])

    # add units
    x = x*1e-4 * u.micron

    # correct values
    if dust == 'smc':
        if geo == 'shell':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.187, 0.469, 0.605, 0.675, 0.725,
                                         0.796, 0.913, 0.941, 0.982, 0.992])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.302, 0.527, 0.639, 0.699, 0.743,
                                         0.806, 0.916, 0.943, 0.983, 0.995])

        if geo == 'dusty':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.412, 0.635, 0.732, 0.78, 0.814,
                                         0.862, 0.941, 0.96, 0.989, 0.997])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.48, 0.664, 0.749, 0.791, 0.822,
                                         0.867, 0.942, 0.961, 0.989, 0.997])

        if geo == 'cloudy':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.689, 0.801, 0.85, 0.877, 0.894,
                                         0.922, 0.966, 0.977, 0.993, 0.998])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.719, 0.81, 0.855, 0.878, 0.896,
                                         0.921, 0.965, 0.976, 0.993, 0.998])

    elif dust == 'mw':
        if geo == 'shell':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.367, 0.688, 0.697, 0.605, 0.745,
                                         0.806, 0.908, 0.941, 0.979, 0.99])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.444, 0.71, 0.717, 0.639, 0.761,
                                         0.815, 0.911, 0.942, 0.979, 0.989])

        if geo == 'dusty':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.555, 0.788, 0.794, 0.73, 0.827,
                                         0.868, 0.937, 0.96, 0.985, 0.992])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.596, 0.799, 0.804, 0.746, 0.835,
                                         0.873, 0.939, 0.96, 0.986, 0.992])

        if geo == 'cloudy':
            if distrib == 'homogeneous':
                if tauV == 0.25:
                    cor_vals = np.array([0.759, 0.881, 0.885, 0.85, 0.903,
                                         0.925, 0.964, 0.977, 0.992, 0.996])

            elif distrib == 'clumpy':
                if tauV == 0.25:
                    cor_vals = np.array([0.775, 0.882, 0.885, 0.853, 0.902,
                                         0.924, 0.963, 0.976, 0.991, 0.995])

    return x, cor_vals

@pytest.mark.parametrize("tauV", [0.25])
@pytest.mark.parametrize("geometries", ['shell', 'cloudy', 'dusty'])
@pytest.mark.parametrize("dust_types", ['smc', 'mw'])
@pytest.mark.parametrize("dust_distribs", ['homogeneous', 'clumpy'])
def test_fesc_WG00(tauV, geometries, dust_types, dust_distribs):
    # get the correct values
    x, cor_vals = get_fesc_corr_vals(tauV, geometries, dust_types, dust_distribs)

    # initialize model
    tmodel = WG00(tauV, geometry=geometries, dust_type=dust_types,
                  dust_distribution=dust_distribs)

    # test
    np.testing.assert_allclose(tmodel.get_fesc(x, tauV), cor_vals, atol=1e-10)
