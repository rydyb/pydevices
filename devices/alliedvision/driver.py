import vmbpy
import threading
import time
import queue

vmb = vmbpy.VmbSystem.get_instance()


class Camera:
    """
    Base class for Alliedvision PoE cameras.

    :param camera_id: camera identifier, e.g., "DEV_000F3100A8D1"
    """

    def __init__(
        self,
        camera_id: str,
    ):
        self._id = camera_id

        # reference to the background thread
        self._thread = None
        # thread-safe queues for the images
        self._images = queue.Queue()
        # event to signal the thread to stop
        self._stop = threading.Event()
        # lock to avoid race conditions while starting/stopping the acquisition loop
        self._lock = threading.Lock()

    @staticmethod
    def available_camera_ids():
        """
        Returns a list of available camera identifiers.
        """
        with vmb:
            return [camera.get_id() for camera in vmb.get_all_cameras()]

    @property
    def id(self) -> str:
        """
        Returns the camera identifiers of cameras found in the local network.
        """
        return self._id

    @property
    def name(self) -> str:
        """
        Returns the camera name.
        """
        with self._lock:
            with vmb, vmb.get_camera_by_id(self._id) as camera:
                return camera.get_name()

    @property
    def model(self) -> str:
        """
        Returns the camera model.
        """
        with self._lock:
            with vmb, vmb.get_camera_by_id(self._id) as camera:
                return camera.get_model()

    @property
    def serial(self) -> str:
        """
        Returns the camera serial number.
        """
        with self._lock:
            with vmb, vmb.get_camera_by_id(self._id) as camera:
                return camera.get_serial()

    @property
    def width(self) -> int:
        """
        Returns the camera image width in number of pixels.
        """
        with self._lock:
            with vmb, vmb.get_camera_by_id(self._id) as camera:
                return camera.Width.get()

    @property
    def height(self) -> int:
        """
        Returns the camera image height in number of pixels.
        """
        with self._lock:
            with vmb, vmb.get_camera_by_id(self._id) as camera:
                return camera.Height.get()

    def __enter__(self):
        self.start_acquisition()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_acquisition()

    def configure(
        self,
        gain_auto=False,
        gamma=1.0,
        exposure_auto=False,
        exposure_mode="TriggerWidth",
        trigger_source="Line1",
        trigger_selector="FrameStart",
        acquisition_mode="Continuous",
        action_device_key=1,
        action_group_key=1,
        action_group_mask=1,
    ):
        """
        Configure the camera with the specified parameters, see Ref. [1] for details.

        [1]: https://cdn.alliedvision.com/fileadmin/content/documents/products/cameras/various/features/GigE_Features_Reference.pdf
        """
        with self._lock:
            with vmb, vmb.get_camera_by_id(self._id) as camera:
                adjust_package_size(camera)

                camera.Gamma.set(gamma)
                if not gain_auto:
                    camera.GainAuto.set("Off")
                if not exposure_auto:
                    camera.ExposureAuto.set("Off")

                camera.ActionDeviceKey.set(action_device_key)
                camera.ActionGroupKey.set(action_group_key)
                camera.ActionGroupMask.set(action_group_mask)
                camera.AcquisitionMode.set(acquisition_mode)
                camera.ExposureMode.set(exposure_mode)
                camera.TriggerSource.set(trigger_source)
                camera.TriggerSelector.set(trigger_selector)
                camera.TriggerMode.set("On")

    def start_acquisition(self):
        """
        Starts the acquisition loop thread to enqueue frames from the camera in the background.
        """
        self._stop.clear()

        def frame_handler(camera: vmbpy.Camera, _: vmbpy.Stream, frame: vmbpy.Frame):
            self._images.put(frame.as_numpy_ndarray())
            camera.queue_frame(frame)

        def acquisition_loop():
            self._lock.acquire()

            with vmb, vmb.get_camera_by_id(self._id) as camera:
                camera.start_streaming(frame_handler)
                camera.AcquisitionStart.run()
                self._lock.release()

                while not self._stop.is_set():
                    time.sleep(0.1)

                self._lock.acquire()
                camera.AcquisitionStop.run()
                camera.stop_streaming()

        self._thread = threading.Thread(target=acquisition_loop)
        self._thread.daemon = True
        self._thread.start()

    def stop_acquisition(self):
        """
        Stops the acquisition loop thread.
        """
        self._stop.set()

        if self._thread is not None:
            self._thread.join()
        self._thread = None

    def software_trigger(self):
        with self._lock:
            with vmb, vmb.get_camera_by_id(self._id) as camera:
                camera.TriggerSoftware.run()

    def action_command_trigger(self, device_key=1, group_key=1, group_mask=1):
        """
        Executes an action command (ethernet) trigger.
        """
        with self._lock:
            with vmb, vmb.get_camera_by_id(self._id) as camera:
                interface = camera.get_interface()
                interface.ActionDeviceKey.set(device_key)
                interface.ActionGroupKey.set(group_key)
                interface.ActionGroupMask.set(group_mask)
                interface.ActionCommand.run()

    def retrieve_image(self):
        """
        Retrieves an image from the queue, blocking until an image is available.
        """
        return self._images.get()


def adjust_package_size(camera: Camera):
    stream = camera.get_streams()[0]
    stream.GVSPAdjustPacketSize.run()

    while not stream.GVSPAdjustPacketSize.is_done():
        time.sleep(0.1)
