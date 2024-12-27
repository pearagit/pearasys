from pathlib import Path
from pearapci.driver import parse_driver
import typer
from typing import Annotated, List, Literal, Optional
from pylspci.device import Device
from dataclasses import asdict
from rich import print

from pearapci.utils import write_attr, device_path
from pearapci.state import PearaPCIState
from pearapci.parser import DeviceParser
from pearapci.driver import app as driver_app

app = typer.Typer()
state: PearaPCIState = None


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
):
    global state
    state = ctx.obj
    devices = (slots or []) + (pids or [])
    if len(devices) > 0:
        state = PearaPCIState(**asdict(state))
        state.devices = devices
    state.validate()


@app.command(help="remove device from kernel's list")
def remove():
    global state
    for device in state.devices:
        write_attr(1, device_path(device).joinpath("remove"), state.verbose)


def parse_driver_override(value: str) -> str:
    if value == "":
        return value  # "may be cleared with an empty string (echo > driver_override)"
    parse_driver(value).name


@app.command(help="overrides the driver for a device")
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


@app.command(help="Prints the device's driver.")
def driver():
    for device in state.devices:
        print(f"[yellow]{device.driver}[/yellow]")
