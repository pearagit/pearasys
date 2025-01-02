from pathlib import Path
import typer
from typing import Annotated, Callable, List, Literal, Optional
from pylspci.device import Device
from dataclasses import asdict
from rich import print

from pearasys.pci.driver import DriverCommand, parse_driver
from pearasys.utils import write_attr, device_path
from pearasys.state import PearaSysState
from pearasys.parser import DeviceParser

app = typer.Typer(
    short_help="Access resources under /sys/bus/pci/devices/",
    help="See https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-bus-pci",
)

state: PearaSysState = None


def driver_command(
    device: Device,
    command: DriverCommand,
    verbose: bool = False,
):
    driver = parse_driver(device.driver)
    if driver is None:
        print(
            f"[yellow]Warning[/yellow]: Skipping {str(device.slot)}, no driver bound."
        )
        return
    getattr(__import__("pearasys").driver, DriverCommand(command).value)(
        driver, [device], verbose
    )


@app.callback()
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
    cmd: Annotated[
        DriverCommand,
        typer.Option(
            "--driver",
            metavar="driver",
            help="See pearasys pci driver --help",
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
    state.validate()
    if cmd is None:
        return
    for device in state.devices:
        driver_command(device, cmd, state.verbose)


@app.command(help="remove device from kernel's list")
def remove():
    global state
    for device in state.devices:
        write_attr(1, device_path(device).joinpath("remove"), state.verbose)


def parse_driver_override(value: str) -> str:
    if value == "":
        return value  # "may be cleared with an empty string (echo > driver_override)"
    parse_driver(value).name


@app.command(help="/sys/bus/pci/devices/.../driver_override")
def driver_override(
    driver: Annotated[
        str,
        typer.Argument(parser=parse_driver, metavar="driver_name", show_default=False),
    ],
):
    global state
    for device in state.devices:
        write_attr(
            driver, device_path(device).joinpath("driver_override"), state.verbose
        )
