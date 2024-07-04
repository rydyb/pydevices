# Highfinesse

Provides an artiq-compatible driver for [HighFinesse wavelength meters](https://www.highfinesse.com/en/wavelengthmeter/).

## Prequisite

Unfortunately, our wavemeter can only be connected to a computer via USB and the wavemeter software does not host a network-compatible API, such that we need to run our [own wavemeter network service](https://github.com/rydyb/godevices/releases/tag/v0.1.0).