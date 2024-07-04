import os
import unittest
from driver import Wavemeter


WAVEMETER_ADDRESS = os.getenv("WAVEMETER_ADDRESS")


class TestCamera(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        if not WAVEMETER_ADDRESS:
            self.skipTest("WAVEMETER_ADDRESS not set")
        self.wavemeter = Wavemeter(WAVEMETER_ADDRESS)

    async def test_version(self):
        version = await self.wavemeter.version()
        self.assertEqual(version["TypeID"], 7)

    async def test_pressure(self):
        pressure = await self.wavemeter.pressure()
        self.assertIsInstance(pressure, float)
        self.assertGreaterEqual(pressure, 800)
        self.assertLessEqual(pressure, 1200)

    async def test_temperature(self):
        temperature = await self.wavemeter.temperature()
        self.assertIsInstance(temperature, float)
        self.assertGreaterEqual(temperature, 16)
        self.assertLessEqual(temperature, 30)

    async def test_frequency(self):
        frequency = await self.wavemeter.frequency(1)
        self.assertIsInstance(frequency, float)
        self.assertGreaterEqual(frequency, 190)
        self.assertLessEqual(frequency, 200)

    async def test_wavelength(self):
        wavelength = await self.wavemeter.wavelength(1)
        self.assertIsInstance(wavelength, float)
        self.assertGreaterEqual(wavelength, 400)
        self.assertLessEqual(wavelength, 1600)


if __name__ == "__main__":
    unittest.main()
