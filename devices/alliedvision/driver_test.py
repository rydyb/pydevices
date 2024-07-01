import os
import numpy
import unittest
from driver import Camera


CAMERA_ID = os.getenv("CAMERA_ID")


class TestCamera(unittest.TestCase):

    def setUp(self):
        if not CAMERA_ID:
            self.skipTest("CAMERA_ID not set")
        self.camera = Camera(CAMERA_ID)

    def test_available_camera_ids(self):
        ids = Camera.available_camera_ids()
        self.assertIsInstance(ids, list)
        self.assertGreater(len(ids), 0)

    def test_id(self):
        self.assertEqual(self.camera.id, CAMERA_ID)

    def test_name(self):
        name = self.camera.name
        self.assertIsInstance(name, str)
        self.assertGreater(len(name), 0)

    def test_model(self):
        model = self.camera.model
        self.assertIsInstance(model, str)
        self.assertGreater(len(model), 0)

    def test_serial(self):
        serial = self.camera.serial
        self.assertIsInstance(serial, str)
        self.assertGreater(len(serial), 0)

    def test_width(self):
        width = self.camera.width
        self.assertEqual(width, 1936)

    def test_height(self):
        height = self.camera.height
        self.assertEqual(height, 1216)

    def test_action_command_trigger(self):
        self.camera.configure(trigger_source="Action0")
        with self.camera as camera:
            camera.action_command_trigger()
            image = camera.retrieve_image()
        self.assertIsInstance(image, numpy.ndarray)

    def test_software_trigger(self):
        self.camera.configure(trigger_source="Software")
        with self.camera as camera:
            camera.software_trigger()
            image = self.camera.retrieve_image()
        self.assertIsInstance(image, numpy.ndarray)


if __name__ == "__main__":
    unittest.main()
