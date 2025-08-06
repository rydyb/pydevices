import os
import configparser
from . import wlmData


def write_ini(filename: str, settings: dict):
    cfg = configparser.RawConfigParser()
    cfg.optionxform = str
    cfg["default"] = {k: str(v) for k, v in settings.items()}
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        cfg.write(f)


class Wavemeter:
    def __init__(
        self, address: str, control_port: int = 7171, callback_port: int = 7172
    ):
        self.address = address
        self.control_port = control_port
        self.callback_port = callback_port
        self._dll = None

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

    def frequency(self, channel: int) -> float:
        if self._dll is None:
            raise RuntimeError("Wavemeter not open")
        return self._dll.GetFrequency(float(channel))

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
