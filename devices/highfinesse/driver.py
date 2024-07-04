import requests


class UnexpectedUnitError(ValueError):
    """
    Raised when the unit of a measurement is not the expected one.
    """

    def __init__(self, got: str, want: str):
        super().__init__(f"Expected unit {want} but got {got}")


class Wavemeter:
    """
    Wavemeter driver for HighFinesse wavemeters.

    The driver communicates with a [HTTP REST service][1] running on the wavemeter computer.

    [1]: https://github.com/rydyb/godevices/releases/tag/v0.1.0
    """

    def __init__(self, address: str):
        self._address = address

    def version(self):
        """
        Returns a version object.
        """
        return self._request("/")

    def pressure(self):
        """
        Returns the pressure in mbar measured inside the wavemeter.
        """
        response = self._request("/pressure")
        if response["Unit"] != "mbar":
            raise UnexpectedUnitError(response["Unit"], "mbar")
        return response["Value"]

    def temperature(self) -> float:
        """
        Returns the temperature in °C measured inside the wavemeter.
        """
        response = self._request("/temperature")
        if response["Unit"] != "°C":
            raise UnexpectedUnitError(response["Unit"], "°C")
        return response["Value"]

    def frequency(self, channel: int) -> float:
        """
        Returns the frequency in THz of the specified channel.
        """
        response = self._request(f"/frequency/{channel}")
        if response["Unit"] != "THz":
            raise UnexpectedUnitError(response["Unit"], "THz")
        return response["Value"]

    def wavelength(self, channel: int) -> float:
        """
        Returns the wavelength in nm of the specified channel.
        """
        response = self._request(f"/wavelength/{channel}")
        if response["Unit"] != "nm":
            raise UnexpectedUnitError(response["Unit"], "nm")
        return response["Value"]

    def _request(self, path: str):
        response = requests.get(f"http://{self._address}{path}")
        response.raise_for_status()
        return response.json()
