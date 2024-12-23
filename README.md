# pearapci

![](demo.gif)

`pearapci` is a command-line tool for easily binding and unbinding PCIe device drivers by writing to [sysfs](https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-bus-pci), primarily for use with switching a gpu between `vfio-pci` and an OEM driver.

## Examples

- Unbinding `vfio-pci` from a device:

```sh
pearapci \
  -d 10de:10f0 \
  driver vfio-pci remove-id \
  device remove \
  rescan
```

- Binding `nvidia` to a gpu and it's audio device:

```sh
pearapci \
  -d 10de:10f0 -d 10de:1b80 \
  driver vfio-pci unbind \
  driver nvidia new-id
```

## Usage

```plaintext
 Usage: pearapci [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

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
- Root privileges required

### `pearapci driver`

Commands for easily writing to the kernel objects under `/sys/bus/pci/drivers/<driver_name>`.

```plaintext
 Usage: pearapci driver [OPTIONS] driver_name COMMAND [ARGS]...

╭─ Arguments ───────────────────────────────────────────────────────────────╮
│ *    driver      driver_name  [required]                                  │
╰───────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                               │
╰───────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────╮
│ bind                                                                      │
│ unbind                                                                    │
│ new-id                                                                    │
│ remove-id                                                                 │
╰───────────────────────────────────────────────────────────────────────────╯
```

### `pearapci device`

Commands for easily writing to the kernel objects under `/sys/bus/pci/devices/<slot>`. Currently, the only worthwhile file is `remove`. The other files/functions are left as an exercise to the reader.

```plaintext
 Usage: pearapci device [OPTIONS] COMMAND [ARGS]...

╭─ Options ─────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                               │
╰───────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────╮
│ remove                                                                    │
╰───────────────────────────────────────────────────────────────────────────╯
```
