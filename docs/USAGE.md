# CLI Reference

<!--toc:start-->

- [CLI Reference](#cli-reference)
  - [`pearasys pci`](#pearasys-pci)
    - [`pearasys pci rescan`](#pearasys-pci-rescan)
    - [`pearasys pci device`](#pearasys-pci-device)
      - [`pearasys pci device driver-override`](#pearasys-pci-device-driver-override)
      - [`pearasys pci device bind`](#pearasys-pci-device-bind)
      - [`pearasys pci device unbind`](#pearasys-pci-device-unbind)
      - [`pearasys pci device new-id`](#pearasys-pci-device-new-id)
      - [`pearasys pci device remove-id`](#pearasys-pci-device-remove-id)
      - [`pearasys pci device remove`](#pearasys-pci-device-remove)
      - [`pearasys pci device rescan`](#pearasys-pci-device-rescan)
      - [`pearasys pci device reset`](#pearasys-pci-device-reset)
    - [`pearasys pci driver`](#pearasys-pci-driver)
      - [`pearasys pci driver bind`](#pearasys-pci-driver-bind)
      - [`pearasys pci driver unbind`](#pearasys-pci-driver-unbind)
      - [`pearasys pci driver new-id`](#pearasys-pci-driver-new-id)
      - [`pearasys pci driver remove-id`](#pearasys-pci-driver-remove-id)
  - [`pearasys service`](#pearasys-service) - [`pearasys service install`](#pearasys-service-install)
  <!--toc:end-->

**Usage**:

```console
pearasys [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `-v, --verbose`: Verbose output.
- `-s, --slot slot`: &lt;domain&gt;:&lt;bus&gt;:&lt;device&gt;.&lt;func&gt;
- `-d, --pid pid`: &lt;vendor&gt;:&lt;device&gt;
- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
- `--help`: Show this message and exit.

**Commands**:

- `pci`: Access PCI related resources under...
- `service`: pearasys systemd service related commands.

## `pearasys pci`

Access PCI related resources under /sys/bus/pci

**Usage**:

```console
pearasys pci [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...
```

**Options**:

- `--help`: Show this message and exit.

**Commands**:

- `rescan`: Forces a rescan and re-discovers removed...
- `device`: Access resources under /sys/bus/pci/devices/
- `driver`: Access resources under /sys/bus/pci/drivers/

### `pearasys pci rescan`

Forces a rescan and re-discovers removed devices.

**Usage**:

```console
pearasys pci rescan [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

### `pearasys pci device`

See <https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-bus-pci>

**Usage**:

```console
pearasys pci device [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `-s, --slot slot`: &lt;domain&gt;:&lt;bus&gt;:&lt;device&gt;.&lt;func&gt;
- `-d, --pid pid`: &lt;vendor&gt;:&lt;device&gt;
- `--driver driver_name`: Driver to be used, overriding the current driver (if any). Example: pearasys -s &lt;slot&gt; pci device --driver=vfio-pci bind
- `--help`: Show this message and exit.

**Commands**:

- `driver-override`: /sys/bus/pci/devices/&lt;device&gt;/driver_override
- `bind`: /sys/bus/pci/devices/&lt;device&gt;/driver/bind
- `unbind`: /sys/bus/pci/devices/&lt;device&gt;/driver/unbind
- `new-id`: /sys/bus/pci/devices/&lt;device&gt;/driver/new_id
- `remove-id`: /sys/bus/pci/devices/&lt;device&gt;/driver/remove_id
- `remove`: /sys/bus/pci/devices/&lt;device&gt;/remove
- `rescan`: /sys/bus/pci/devices/&lt;device&gt;/rescan
- `reset`: /sys/bus/pci/devices/&lt;device&gt;/reset

#### `pearasys pci device driver-override`

/sys/bus/pci/devices/&lt;device&gt;/driver_override

**Usage**:

```console
pearasys pci device driver-override [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

#### `pearasys pci device bind`

Attempts to bind the specified device(s) to the driver given by the argument. Unbinds the device(s) from it&#x27;s current driver, if any.

**Usage**:

```console
pearasys pci device bind [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

#### `pearasys pci device unbind`

Unbinds the specified device(s) from it&#x27;s currently bound driver(s).

**Usage**:

```console
pearasys pci device unbind [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

#### `pearasys pci device new-id`

Adds the device ID of the specified devices to it&#x27;s currently bound driver, or the value of --driver if specified.

**Usage**:

```console
pearasys pci device new-id [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

#### `pearasys pci device remove-id`

Removes the device ID of the specified devices to it&#x27;s currently bound driver, or the value of --driver if specified.

**Usage**:

```console
pearasys pci device remove-id [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

#### `pearasys pci device remove`

Removes device from kernel&#x27;s list

**Usage**:

```console
pearasys pci device remove [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

#### `pearasys pci device rescan`

Rescans the device&#x27;s parent/child bus(es).

**Usage**:

```console
pearasys pci device rescan [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

#### `pearasys pci device reset`

Resets the device if a reset function is present.

**Usage**:

```console
pearasys pci device reset [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

### `pearasys pci driver`

See <https://www.kernel.org/doc/Documentation/filesystems/sysfs-pci.txt>

**Usage**:

```console
pearasys pci driver [OPTIONS] driver_name COMMAND [ARGS]...
```

**Arguments**:

- `driver_name`: [required]

**Options**:

- `-s, --slot slot`: &lt;domain&gt;:&lt;bus&gt;:&lt;device&gt;.&lt;func&gt;
- `-d, --pid pid`: &lt;vendor&gt;:&lt;device&gt;
- `--help`: Show this message and exit.

**Commands**:

- `bind`: /sys/bus/pci/drivers/.../bind
- `unbind`: /sys/bus/pci/drivers/.../unbind
- `new-id`: /sys/bus/pci/drivers/.../new_id
- `remove-id`: /sys/bus/pci/drivers/.../remove_id

#### `pearasys pci driver bind`

/sys/bus/pci/drivers/.../bind

**Usage**:

```console
pearasys pci driver bind [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

#### `pearasys pci driver unbind`

/sys/bus/pci/drivers/.../unbind

**Usage**:

```console
pearasys pci driver unbind [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

#### `pearasys pci driver new-id`

/sys/bus/pci/drivers/.../new_id

**Usage**:

```console
pearasys pci driver new-id [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

#### `pearasys pci driver remove-id`

/sys/bus/pci/drivers/.../remove_id

**Usage**:

```console
pearasys pci driver remove-id [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

## `pearasys service`

pearasys systemd service related commands.

**Usage**:

```console
pearasys service [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--help`: Show this message and exit.

**Commands**:

- `install`: Installs a systemd service to manage a...

### `pearasys service install`

Installs a systemd service to manage a device&#x27;s driver.

**Usage**:

```console
pearasys service install [OPTIONS] driver_name
```

**Arguments**:

- `driver_name`: [required]

**Options**:

- `--prefix path`: Specify the service installation directory. [default: /etc/systemd/system]
- `--help`: Show this message and exit.
