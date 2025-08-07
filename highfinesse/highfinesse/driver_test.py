import time
import unittest

from .driver import Wavemeter


class TestWavemeterHardware(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.wlm = Wavemeter("10.163.100.21", control_port=7171, callback_port=7172)
        cls.wlm.open()

    @classmethod
    def tearDownClass(cls):
        cls.wlm.close()

    def test_version_returns_string(self):
        version = self.wlm.version()
        self.assertEqual(version, "7.4980.6533.1")

    def test_frequency(self):
        freq = self.wlm.frequency()
        self.assertIsInstance(freq, float)
        self.assertGreater(freq, 0.0)

    def test_wavelength(self):
        wvl = self.wlm.wavelength()
        self.assertIsInstance(wvl, float)
        self.assertGreater(wvl, 0.0)

    def test_temperature(self):
        temp = self.wlm.temperature()
        self.assertIsInstance(temp, float)
        self.assertGreater(temp, -100.0)  # sanity lower bound
        self.assertLess(temp, 200.0)  # sanity upper bound

    def test_pressure(self):
        pres = self.wlm.pressure()
        self.assertIsInstance(pres, float)
        self.assertGreater(pres, 0.0)

    def test_exposure(self):
        expo = self.wlm.exposure(0)
        self.assertIsInstance(expo, int)
        self.assertGreaterEqual(expo, 0)

    def test_callback(self):
        callback_called = False

        def callback(param):
            nonlocal callback_called
            callback_called = True

        self.wlm.listen(callback)
        time.sleep(1)
        self.wlm.unlisten()
        self.assertTrue(callback_called)


if __name__ == "__main__":
    unittest.main()
