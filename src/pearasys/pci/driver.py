from pathlib import Path
from typing import Annotated, Callable, List, Optional
from pylspci.device import Device
from dataclasses import asdict
import typer
import os
from enum import Enum
from rich import print

from pearasys.state import PearaSysState
from pearasys.utils import write_attr, device_id, device_path
from pearasys.parser import DeviceParser

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
    if len(devices) > 0:
        state = PearaSysState(**asdict(state))
        state.devices = devices
    state.driver = driver
    if ctx.invoked_subcommand != "ls":
        state.validate()


@app.command(help="/sys/bus/pci/drivers/.../bind")
def bind(driver=None, devices=None, verbose=None):
    global state
    devices = devices or state.devices
    driver = driver or state.driver
    verbose = verbose if verbose is not None else state.verbose
    for device in devices:
        if device.driver == driver.name:
            print(
                f"[yellow]Warning[/yellow]: Skipping {str(device.slot)}, current driver is {driver.name}"
            )
            continue
        write_attr(device.slot.__str__(), driver.joinpath("bind"), verbose)


@app.command(help="/sys/bus/pci/drivers/.../unbind")
def unbind(driver=None, devices=None, verbose=None):
    global state
    devices = devices or state.devices
    driver = driver or state.driver
    verbose = verbose if verbose is not None else state.verbose
    for device in devices:
        if device.driver is None:
            print(
                f"[yellow]Warning[/yellow]: Skipping {str(device.slot)}, device is not bound."
            )
            continue
        write_attr(device.slot.__str__(), driver.joinpath("unbind"), verbose)


@app.command(help="/sys/bus/pci/drivers/.../new_id")
def new_id(driver=None, devices=None, verbose=None):
    global state
    devices = devices or state.devices
    driver = driver or state.driver
    verbose = verbose if verbose is not None else state.verbose
    for device in devices:
        write_attr(
            device_id(device),
            driver.joinpath("new_id"),
            verbose,
        )


@app.command(help="/sys/bus/pci/drivers/.../remove_id")
def remove_id(driver=None, devices=None, verbose=None):
    global state
    devices = devices or state.devices
    driver = driver or state.driver
    verbose = verbose if verbose is not None else state.verbose
    for device in devices:
        write_attr(
            device_id(device),
            driver.joinpath("remove_id"),
            verbose,
        )


@app.command(help="Lists the files in the driver directory.")
def ls():
    global state
    os.system(f"ls -lah --color=always {state.driver}")


class DriverCommand(str, Enum):
    new_id = "new-id"
    remove_id = "remove-id"
    bind = "bind"
    unbind = "unbind"
