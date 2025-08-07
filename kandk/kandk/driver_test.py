import unittest
import kandk

class TestFrequencyCounter(unittest.TestCase):

    def setUp(self):
        self.fc = kandk.FrequencyCounter(device_host="10.163.100.48", channels=8)
        self.fc.open()

    def tearDown(self):
        try:
            self.fc.close()
        except Exception:
            pass

    def test_open(self):
        pass

    def test_report(self):
        for i in range(10):
            freqs = self.fc.report()
            self.assertIsNotNone(freqs)
            self.assertEqual(len(freqs), 8)
            self.assertTrue(
                    all(x > 0 for x in freqs),
                    f"Found non‐positive elements in {freqs}"
            )


if __name__ == "__main__":
    unittest.main()
