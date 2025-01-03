# pearasys

![](docs/demo.gif)

`pearasys` is a command-line tool for easily binding and unbinding PCIe device drivers by writing to [sysfs](https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-bus-pci), primarily for use with switching a gpu between `vfio-pci` and an OEM driver.

## Examples

- Binding `nvidia` to a gpu and it's audio device:

```sh
pearasys \
  -d 10de:10f0 -d 10de:1b80 \
  driver vfio-pci unbind \
  driver nvidia new-id
```

- Unbinding `vfio-pci` from a device:

```sh
pearasys \
  -d 10de:10f0 \
  driver vfio-pci remove-id \
  device remove \
  rescan
```

**Note**: Attempting to unbind a driver from a device in use will result in a hung process. In the event this occurs, check to see if your display manager, `nvidia-persistenced`, or another process is running on your GPU.

## Usage

```plaintext
 Usage: pearasys [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

╭─ Options ─────────────────────────────────────────────────────────────────╮
│ --verbose             -v            Verbose output.                       │
│ --slot                -s      slot  <domain>:<bus>:<device>.<func>        │
│ --pid                 -d      pid   <vendor>:<device>                     │
│ --install-completion                Install completion for the current    │
│                                     shell.                                │
│ --show-completion                   Show completion for the current       │
│                                     shell, to copy it or customize the    │
│                                     installation.                         │
│ --help                              Show this message and exit.           │
╰───────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────╮
│ rescan                                                                    │
│ device                                                                    │
│ driver                                                                    │
╰───────────────────────────────────────────────────────────────────────────╯
```

- At least one device must be specified with `--slot` or `--pid` for use with the `device` and `driver` subcommands.
- It is assumed that the files and directories under the /sys hierarchy are owned by `root:root`, so **[running as root is required](https://github.com/pearagit/pearasys/blob/master/src/pearasys/state.py#L22)**.

### `pearasys driver`

Commands for easily writing to the kernel objects under `/sys/bus/pci/drivers/<driver_name>`.

```plaintext
 Usage: pearasys driver [OPTIONS] driver_name COMMAND [ARGS]...

╭─ Arguments ───────────────────────────────────────────────────────────────╮
│ *    driver      driver_name  [required]                                  │
╰───────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────╮
│ --slot  -s      slot  <domain>:<bus>:<device>.<func>                      │
│ --pid   -d      pid   <vendor>:<device>                                   │
│ --help                Show this message and exit.                         │
╰───────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────╮
│ bind                                                                      │
│ unbind                                                                    │
│ new-id                                                                    │
│ remove-id                                                                 │
│ ls                                                                        │
╰───────────────────────────────────────────────────────────────────────────╯
```

### `pearasys device`

Commands for easily reading/writing to the kernel objects under `/sys/bus/pci/devices/<slot>`.

```plaintext
Usage: pearasys device [OPTIONS] COMMAND [ARGS]...

╭─ Options ─────────────────────────────────────────────────────────────────╮
│ --slot  -s      slot  <domain>:<bus>:<device>.<func>                      │
│ --pid   -d      pid   <vendor>:<device>                                   │
│ --help                Show this message and exit.                         │
╰───────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────╮
│ remove            remove device from kernel's list                        │
│ driver-override   overrides the driver for a device                       │
│ driver            Prints the device's driver.                             │
╰───────────────────────────────────────────────────────────────────────────╯
```
