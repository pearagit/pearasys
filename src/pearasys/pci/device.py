from dataclasses import asdict
from pathlib import Path
from typing import Annotated, List, Optional

import typer
from pylspci.device import Device
from rich import print

from pearasys.pci.driver import (
    parse_driver,
    driver_bind,
    driver_unbind,
    driver_new_id,
    driver_remove_id,
)
from pearasys.parser import DeviceParser
from pearasys.state import PearaSysState
from pearasys.utils import device_path, write_attr

app = typer.Typer(
    short_help="Access resources under `/sys/bus/pci/devices/`",
    help="See the [sysfs-bus-pci documentation](https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-bus-pci)",
)

state: PearaSysState = None


def parse_driver_override(value: str) -> str:
    # override may be cleared with an empty string
    return value if value == "" else parse_driver(value).name


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    slots: Annotated[
        Optional[List[Device]],
        typer.Option(
            "--slot",
            "-s",
            help="<domain>:<bus>:<device>.<func>",
            metavar="slot",
            click_type=DeviceParser(),
            show_default=False,
        ),
    ] = None,
    pids: Annotated[
        Optional[List[Device]],
        typer.Option(
            "--pid",
            "-d",
            help="<vendor>:<device>",
            metavar="pid",
            click_type=DeviceParser(),
            show_default=False,
        ),
    ] = None,
    driver: Annotated[
        Optional[Path],
        typer.Option(
            "--driver",
            parser=parse_driver,
            metavar="driver_name",
            show_default=False,
            help="Driver to be used, overriding the current driver (if any). Example: pearasys -s <slot> pci device --driver=vfio-pci bind",
        ),
    ] = None,
):

    global state
    state = ctx.obj
    devices = (slots or []) + (pids or [])
    # copy context state to local state if a callback param is present
    if len(devices) > 0 or driver is not None:
        state = PearaSysState(**asdict(state))
    state.devices = devices if len(devices) > 0 else state.devices
    state.driver = driver if driver is not None else state.driver
    state.validate()


@app.command(help="`/sys/bus/pci/devices/<device>/driver_override`")
def driver_override():
    global state
    if state.driver is None:
        raise typer.BadParameter("Driver must be specified.")
    for device in state.devices:
        write_attr(state.driver, device_path(device) / "driver_override", state.verbose)


@app.command(
    short_help="`/sys/bus/pci/devices/<device>/driver/bind`",
    help="Attempts to bind the specified device(s) to the driver given by the argument. Unbinds the device(s) from it's current driver, if any.",
)
def bind():
    global state
    if state.driver is None:
        raise typer.BadParameter("Driver must be specified.")
    for device in state.devices:
        if device.driver is not None:
            driver_unbind(parse_driver(device.driver), device, state.verbose)
        driver_bind(state.driver, device, state.verbose)


@app.command(
    short_help="`/sys/bus/pci/devices/<device>/driver/unbind`",
    help="Unbinds the specified device(s) from it's currently bound driver(s).",
)
def unbind():
    global state
    for device in state.devices:
        if device.driver is None:
            print(
                f"[yellow]Warning[/yellow]: Skipping device {str(device.slot)}, no driver bound."
            )
            continue
        driver_unbind(parse_driver(device.driver), device, state.verbose)


@app.command(
    short_help="`/sys/bus/pci/devices/<device>/driver/new_id`",
    help="Adds the device ID of the specified devices to it's currently bound driver, or the value of --driver if specified.",
)
def new_id():
    global state
    for device in state.devices:
        driver = (
            parse_driver(device.driver) if device.driver is not None else state.driver
        )
        if driver is None:
            print(
                f"[yellow]Warning[/yellow]: Skipping device {str(device.slot)}, no driver bound."
            )
            continue
        driver_new_id(device.driver, device, state.verbose)


@app.command(
    short_help="`/sys/bus/pci/devices/<device>/driver/remove_id`",
    help="Removes the device ID of the specified devices to it's currently bound driver, or the value of --driver if specified.",
)
def remove_id():
    global state
    for device in state.devices:
        driver = (
            parse_driver(device.driver) if device.driver is not None else state.driver
        )
        if driver is None:
            print(
                f"[yellow]Warning[/yellow]: Skipping device {str(device.slot)}, no driver specified or bound."
            )
            continue
        driver_remove_id(driver, device, state.verbose)


@app.command(
    short_help="`/sys/bus/pci/devices/<device>/remove`",
    help="Removes device from kernel's list",
)
def remove():
    global state
    for device in state.devices:
        write_attr(1, device_path(device) / "remove", state.verbose)


@app.command(
    short_help="`/sys/bus/pci/devices/<device>/rescan`",
    help="Rescans the device's parent/child bus(es).",
)
def rescan():
    global state
    for device in state.devices:
        write_attr(1, device_path(device) / "rescan", state.verbose)


@app.command(
    short_help="`/sys/bus/pci/devices/<device>/reset`",
    help="Resets the device if a reset function is present.",
)
def reset():
    global state
    for device in state.devices:
        reset_file = device_path(device) / "reset"
        if reset_file.exists():
            write_attr(1, reset_file, state.verbose)
        else:
            print(
                f"[yellow]Warning[/yellow]: Skipping device {str(device.slot)}, no reset function."
            )
