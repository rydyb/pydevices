import os
import unittest
from driver import Wavemeter


WAVEMETER_ADDRESS = os.getenv("WAVEMETER_ADDRESS")


class TestCamera(unittest.TestCase):

    def setUp(self):
        if not WAVEMETER_ADDRESS:
            self.skipTest("WAVEMETER_ADDRESS not set")
        self.wavemeter = Wavemeter(WAVEMETER_ADDRESS)

    def test_version(self):
        version = self.wavemeter.version()
        self.assertEqual(version["TypeID"], 7)

    def test_pressure(self):
        pressure = self.wavemeter.pressure()
        self.assertIsInstance(pressure, float)
        self.assertGreaterEqual(pressure, 800)
        self.assertLessEqual(pressure, 1200)

    def test_temperature(self):
        temperature = self.wavemeter.temperature()
        self.assertIsInstance(temperature, float)
        self.assertGreaterEqual(temperature, 16)
        self.assertLessEqual(temperature, 30)

    def test_frequency(self):
        frequency = self.wavemeter.frequency(1)
        self.assertIsInstance(frequency, float)
        self.assertGreaterEqual(frequency, 190)
        self.assertLessEqual(frequency, 200)

    def test_wavelength(self):
        wavelength = self.wavemeter.wavelength(1)
        self.assertIsInstance(wavelength, float)
        self.assertGreaterEqual(wavelength, 400)
        self.assertLessEqual(wavelength, 1600)


if __name__ == "__main__":
    unittest.main()
