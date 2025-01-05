import os
from dataclasses import asdict
from pathlib import Path
from typing import Annotated, List, Optional

import typer
from pylspci.device import Device
from rich import print

from pearasys.parser import DeviceParser
from pearasys.state import PearaSysState
from pearasys.utils import device_id, write_attr

app = typer.Typer(
    short_help="Access resources under /sys/bus/pci/drivers/",
    help="See https://www.kernel.org/doc/Documentation/filesystems/sysfs-pci.txt",
)

state: PearaSysState = (None, None, False)


def parse_driver(value: str):
    driver = Path(f"/sys/bus/pci/drivers/{value}")
    if not driver.exists():
        if os.system(f"modprobe -f {value}") != 0:
            raise typer.BadParameter(f"Error: Failed to add kernel module `{value}`.")
    return driver


def driver_bind(driver: Path, device: Device, verbose: bool = False):
    if device.driver == driver.name:
        print(
            f"[yellow]Warning[/yellow]: Skipping device {str(device.slot)}, current driver is {driver.name}"
        )
        return
    write_attr(str(device.slot), driver / "bind", verbose)


def driver_unbind(driver: Path, device: Device, verbose: bool = False):
    if device.driver is None:
        print(
            f"[yellow]Warning[/yellow]: Skipping device {str(device.slot)}, no driver bound."
        )
        return
    write_attr(str(device.slot), driver / "unbind", verbose)


def driver_new_id(driver: Path, device: Device, verbose: bool = False):
    write_attr(
        device_id(device),
        driver / "new_id",
        verbose,
    )


def driver_remove_id(driver: Path, device: Device, verbose: bool = False):
    write_attr(
        device_id(device),
        driver / "remove_id",
        verbose,
    )


@app.callback()
def callback(
    ctx: typer.Context,
    driver: Annotated[
        Path,
        typer.Argument(parser=parse_driver, metavar="driver_name", show_default=False),
    ],
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
):
    global state
    state = ctx.obj
    devices = (slots or []) + (pids or [])
    # copy context state to local state if a callback param is present
    if len(devices) > 0:
        state = PearaSysState(**asdict(state))
        state.devices = devices
    state.driver = driver
    state.validate()


@app.command(help="/sys/bus/pci/drivers/.../bind")
def bind():
    global state
    for device in state.devices:
        driver_bind(state.driver, device, state.verbose)


@app.command(help="/sys/bus/pci/drivers/.../unbind")
def unbind():
    global state
    for device in state.devices:
        driver_unbind(state.driver, device, state.verbose)


@app.command(help="/sys/bus/pci/drivers/.../new_id")
def new_id():
    global state
    for device in state.devices:
        driver_new_id(state.driver, device, state.verbose)


@app.command(help="/sys/bus/pci/drivers/.../remove_id")
def remove_id():
    global state
    for device in state.devices:
        driver_remove_id(state.driver, device, state.verbose)
