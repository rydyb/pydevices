# K+K

Support for K+K FXE device included in some Menlo frequency combs.

## Installation

```shell
pip install git+https://github.com/rydyb/pydevices.git@main#subdirectory=kandk
```

## Usage

Stream frequencies as comma-separated values:
```shell
python -m kandk.main stream
```

Start sipyco RPC server for ARTIQ:
```shell
python -m kandk.main sipyco
```
