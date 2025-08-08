import os
from blinker import Signal
import configparser
from . import wlmData
from . import wlmConst


def write_ini(filename: str, settings: dict):
    cfg = configparser.RawConfigParser()
    cfg.optionxform = str
    cfg["default"] = {k: str(v) for k, v in settings.items()}
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        cfg.write(f)


def map_wlm_modes(mode, value):
    if mode == wlmConst.cmiPressure:
        return {"quantity": "pressure", "value": value, "unit": "mbar"}
    elif mode == wlmConst.cmiTemperature:
        return {"quantity": "temperature", "value": value, "unit": "celsius"}
    elif mode == wlmConst.cmiWavelength1:
        return {"quantity": "wavelength", "channel": 1, "value": value, "unit": "nm"}
    elif mode == wlmConst.cmiWavelength2:
        return {"quantity": "wavelength", "channel": 2, "value": value, "unit": "nm"}
    elif mode == wlmConst.cmiWavelength3:
        return {"quantity": "wavelength", "channel": 3, "value": value, "unit": "nm"}
    elif mode == wlmConst.cmiWavelength4:
        return {"quantity": "wavelength", "channel": 4, "value": value, "unit": "nm"}
    elif mode == wlmConst.cmiWavelength5:
        return {"quantity": "wavelength", "channel": 5, "value": value, "unit": "nm"}
    elif mode == wlmConst.cmiWavelength6:
        return {"quantity": "wavelength", "channel": 6, "value": value, "unit": "nm"}
    elif mode == wlmConst.cmiWavelength7:
        return {"quantity": "wavelength", "channel": 7, "value": value, "unit": "nm"}
    elif mode == wlmConst.cmiWavelength8:
        return {"quantity": "wavelength", "channel": 8, "value": value, "unit": "nm"}
    return None


class Wavemeter:
    def __init__(
        self, address: str, control_port: int = 7171, callback_port: int = 7172
    ):
        self.address = address
        self.control_port = control_port
        self.callback_port = callback_port
        self._dll = None
        self._data = Signal()
        self._handle = None

    def open(self):
        write_ini(
            os.path.join(os.path.expanduser("~/.config/HighFinesse"), "wlmData.ini"),
            {
                "version": 4,
                "address": self.address,
                "port": self.control_port,
                "port2": self.callback_port,
                "offload": 1,
                "loglevel": 3,
                "errormode": 9,
            },
        )
        try:
            self._dll = wlmData.LoadDLL()
        except OSError as e:
            raise RuntimeError(f"Could not load wlmData DLL: {e}")
        if self._dll.GetWLMCount(0) == 0:
            raise RuntimeError("No running WLM server instance found.")

    def close(self):
        self._dll = None

    def version(self) -> str:
        if self._dll is None:
            raise RuntimeError("Wavemeter not open")
        t = self._dll.GetWLMVersion(0)
        v = self._dll.GetWLMVersion(1)
        r = self._dll.GetWLMVersion(2)
        b = self._dll.GetWLMVersion(3)
        return f"{t}.{v}.{r}.{b}"

    def frequency(self) -> float:
        if self._dll is None:
            raise RuntimeError("Wavemeter not open")
        return self._dll.GetFrequency(0.0)

    def wavelength(self) -> float:
        if self._dll is None:
            raise RuntimeError("Wavemeter not open")
        return self._dll.GetWavelength(0.0)

    def temperature(self) -> float:
        if self._dll is None:
            raise RuntimeError("Wavemeter not open")
        return self._dll.GetTemperature(0.0)

    def pressure(self) -> float:
        if self._dll is None:
            raise RuntimeError("Wavemeter not open")
        return self._dll.GetPressure(0.0)

    def exposure(self, channel: int) -> int:
        if self._dll is None:
            raise RuntimeError("Wavemeter not open")
        return self._dll.GetExposure(int(channel))

    def listen(self, priority: int = 2):
        if self._dll is None:
            raise RuntimeError("Wavemeter not open")
        if self._handle is not None:
            raise RuntimeError("Already listening for callbacks")

        @wlmData.CALLBACK_TYPE
        def handle(mode, intval, dblval):
            event = map_wlm_modes(mode, dblval)
            if event is not None:
                self._data.send(event)

        self._handle = wlmData.CALLBACK_TYPE(handle)

        self._dll.Instantiate(
            wlmConst.cInstNotification,
            wlmConst.cNotifyInstallCallback,
            self._handle,
            priority,
        )

    def unlisten(self):
        if self._dll is None:
            raise RuntimeError("Wavemeter not open")
        if self._handle is None:
            raise RuntimeError("Not currently listening for callbacks")
        self._dll.Instantiate(
            wlmConst.cInstNotification, wlmConst.cNotifyRemoveCallback, None, 0
        )
        self._handle = None

    def subscribe(self, callback):
        self._data.connect(callback)

    def unsubscribe(self, callback):
        self._data.disconnect(callback)
