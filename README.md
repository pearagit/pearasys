![pearasys demo](docs/demo.gif)

# pearasys

`pearasys` is a command-line tool for easily binding and unbinding PCIe device drivers by writing to [sysfs](https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-bus-pci), primarily for use with switching a gpu between `vfio-pci` and an OEM driver.

## `systemd`

`pearasys` supports using systemd to control your device's drivers through a service. To install a service for a device, use the `service install` command:

```console
$ sudo pearasys -d 10de:1b80 service install nvidia
Service installed successfully. Start service with command: `systemctl start pearasys-0000:04:00.0@nvidia.service`
```

See the documentation for [`pearasys service`](./docs/USAGE.md#pearasys-service) for more information.

## Examples

- Binding `nvidia` to a gpu and it's audio device:

```console
pearasys \
  -d 10de:10f0 -d 10de:1b80 \
  pci \ # pci sub commands are chainable
    driver vfio-pci unbind \
    driver nvidia new-id
```

- Unbinding `vfio-pci` from a device:

```console
pearasys \
  -d 10de:10f0 \
  pci \
    driver vfio-pci remove-id \
    device remove \
    rescan
```

**Note**: Attempting to unbind a driver from a device in use will result in a hung process. In the event this occurs, check to see if your display manager, `nvidia-persistenced`, or another process is running on your GPU.

## Usage

See [USAGE.md](docs/USAGE.md) for more information.
