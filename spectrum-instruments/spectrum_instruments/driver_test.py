import spcm
import unittest
import numpy as np
import spectrum_instruments


class TestGeneric(unittest.TestCase):
    def test_list_devices(self):
        devices = spectrum_instruments.list_devices()
        assert isinstance(devices, list)
        assert all(isinstance(dev, dict) for dev in devices)
        assert all("device_identifier" in dev for dev in devices)
        assert all("serial_number" in dev for dev in devices)
        assert all("family" in dev for dev in devices)
        assert all("num_channels" in dev for dev in devices)
        assert all("product_name" in dev for dev in devices)


class TestSignalGenerator(unittest.TestCase):

    def setUp(self):
        self.sg = spectrum_instruments.SignalGenerator(
            serial_number=18996,
            sample_rate=1e9,
            output_voltage=1.0,
            verbose=False,
        )

    def tearDown(self):
        try:
            self.sg.close()
        except Exception:
            pass

    def test_initialization(self):
        pass

    def test_transfer_waveform_raises_on_bad_length(self):
        bad = np.zeros(10, dtype=float)  # not multiple of 32
        with self.assertRaises(spcm.SpcmException):
            self.sg.transfer_waveform(bad)

    def test_transfer_waveform_hardware(self):
        good = np.linspace(-1, 1, 32, dtype=float)
        try:
            self.sg.transfer_waveform(good)
        except Exception as e:
            self.fail(f"transfer_waveform raised unexpectedly: {e}")

    def test_arm_external_trigger_hardware(self):
        try:
            self.sg.start_triggered_playback()
        except Exception as e:
            self.fail(f"arm_external_trigger raised unexpectedly: {e}")

    def test_continuous_playback_hardware(self):
        try:
            self.sg.start_continuous_playback()
        except Exception as e:
            self.fail(f"continuous_playback raised unexpectedly: {e}")


if __name__ == "__main__":
    unittest.main()
