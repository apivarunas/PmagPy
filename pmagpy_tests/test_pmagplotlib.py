import os
import sys
import unittest
import cartopy
from pmagpy import pmag
from pmagpy import pmagplotlib
from pmag_env import set_env
WD = pmag.get_test_WD()
import matplotlib
import matplotlib.pyplot as plt


class TestPlotDir(unittest.TestCase):
    """pmagplotlib.plot_dir draws the fit on the Zijderveld plot."""

    def setUp(self):
        self.ZED = {'eqarea': 1, 'zijd': 2}
        plt.figure(1)
        plt.figure(2)
        steps = [(10., 40., 5.), (15., 45., 4.), (20., 50., 3.), (22., 48., 2.), (25., 52., 1.)]
        self.data = [[i, d, inc, m, 'g'] for i, (d, inc, m) in enumerate(steps)]

    def tearDown(self):
        plt.close('all')

    def fit_line(self, calculation_type):
        mpars = pmag.domean(self.data, 0, 4, calculation_type)
        pmagplotlib.plot_dir(self.ZED, mpars, self.data, 0)
        line = plt.figure(2).gca().lines[-2]  # the x-y line; the x-z line follows
        return mpars, line.get_xdata(), line.get_ydata()

    def test_vector_mean_from_origin(self):
        mpars, x, y = self.fit_line('DE-VM')
        self.assertEqual((x[0], y[0]), (0., 0.))
        self.assertGreater(abs(x[1]), 0)

    def test_anchored_line_from_origin(self):
        mpars, x, y = self.fit_line('DE-BFL-A')
        self.assertEqual((x[0], y[0]), (0., 0.))

    def test_free_line_about_centre_of_mass(self):
        mpars, x, y = self.fit_line('DE-BFL')
        self.assertNotEqual((x[0], y[0]), (0., 0.))
        self.assertAlmostEqual((x[0] + x[1])/2, mpars['center_of_mass'][0]/self.data[0][3])


class TestPlotMagMap(unittest.TestCase):

    def setUp(self):
        print('sys.platform', sys.platform)
        print('matplotlib backend', matplotlib.get_backend())
        print('matplotlib version', matplotlib.__version__)

    def tearDown(self):
        pass

    @unittest.skipIf(set_env.IS_LINUX and 'discover' in sys.argv, 'test fails on Linux env, works on Linux otherwise')
    def test_success(self):
        date, mod, lon_0, alt, ghfile = 1956.0725, 'cals10k.2', 0, 0, ""  # only date is required
        Ds, Is, Bs, Brs, lons, lats = pmag.do_mag_map(
            date, mod=mod, lon_0=lon_0, alt=alt, file=ghfile)
        res_0 = pmagplotlib.plot_mag_map(
            1, Bs, lons, lats, 'B', date=date, contours=True, lon_0=10, proj="Mollweide")  # plot the field strength
        res_1 = pmagplotlib.plot_mag_map(
            2, Is, lons, lats, 'I', date=date, contours=True)  # plot the inclination
        res_2 = pmagplotlib.plot_mag_map(
            3, Ds, lons, lats, 'D', date=date, contours=True)
        if cartopy.__version__ != "0.16.0":
            for res in [res_0, res_1, res_2]:
                self.assertIsInstance(res, cartopy.mpl.geoaxes.GeoAxesSubplot)
        else:
            for res in [res_1, res_2]:
                self.assertIsInstance(res, cartopy.mpl.geoaxes.GeoAxesSubplot)
        print('completed plot_magmap test')
