# HighFinesse

Support for HighFinesse wavemeter WS7 with 8-channel multiplexer.

## Installation

```shell
pip install git+https://github.com/rydyb/pydevices.git@main#subdirectory=highfinesse
```

You will also have to install the package library shipped with your NetAccess wavemeter software as `.deb` or `.rpm`.

## Usage

Stream pressure, temperature, wavelength or frequency as newline-separated:
```shell
python -m highfinesse.main frequency --host 10.163.100.20
```

Stream pressure, temperature and wavelength via callback mode:
```shell
python -m highfinesse.main stream --host 10.163.100.20
```

Start sipyco RPC server for ARTIQ:
```shell
python -m highfinesse.main sipyco
```
