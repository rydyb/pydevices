# Alliedvision

Provides an artiq-compatible driver for ethernet-based [Alliedvision](https://www.alliedvision.com) cameras.

## Setup

Enter the development shell:
```shell
nix develop
```

## Usage

List available camera identifies:
```shell
python -c "from devices.alliedvision import Camera; print(Camera.available_camera_ids())"
```

Run tests:
```shell
CAMERA_ID=DEV_000F315E02DF python ./devices/alliedvision/driver_test.py
```

## Examples

Wait for a digital trigger to start image acquisition:
```python
with Camera("<camera id>") as camera:
    image = camera.retrieve_image()
    print(image.shape)
```

Configure the camera for an action command (ethernet-based trigger) and start an image acquisition:
```python
camera = Camera("<camera id">)
camera.configure(trigger_source="Action0")
camera.start_acquisition()
image = camera.retrieve_iamge()
print(image.shape)
camera.stop_acquisition()
```