from typing import Annotated, Callable, Dict, List, Optional
import re
import os
import click

import typer
from pylspci.device import Device
from rich import print

from pearapci.utils import get_device, write_attr
from pearapci.device import app as device_app
from pearapci.driver import app as driver_app
from pearapci.state import PearaPCIState


app = typer.Typer()
app.add_typer(device_app, name="device")
app.add_typer(driver_app, name="driver")


def parse_pid(pid: str):
    match = re.match(r"([0-9a-fA-F]{4}):([0-9a-fA-F]{4})", pid)
    if not match:
        raise typer.BadParameter("PID must be in the format vvvv:dddd")
    device = get_device(device=pid)
    if device is None:
        raise typer.BadParameter(f"No device with pid: {pid}")
    return device


def parse_slot(slot: str):
    match = re.match(r"\b([0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}.\d{1})", slot)
    if not match:
        raise typer.BadParameter("Slot must be in the format dddd:dd:d.d")
    device = get_device(slot=slot)
    if device is None:
        raise typer.BadParameter(f"No devices with slot: {slot}")
    return device


class DeviceParser(click.ParamType):
    name = "CustomClass"
    parsers: Dict[str, Callable[[str], str]] = {"slots": parse_slot, "pids": parse_pid}

    def convert(self, value, param, ctx):
        return self.parsers[param.name](value)


@app.callback(chain=True)
def callback(
    ctx: typer.Context,
    verbose: Annotated[
        Optional[bool], typer.Option("--verbose", "-v", help="Verbose output.")
    ] = False,
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
    if os.geteuid() != 0:
        print("[bold red]Error:[/bold red] root permissions required.")
        raise typer.Exit(1)
    slots = slots or []
    pids = pids or []
    state = PearaPCIState(verbose, slots + pids)

    ctx.obj = state


@app.command()
def rescan(ctx: typer.Context):
    state: PearaPCIState = ctx.obj
    write_attr(1, "/sys/bus/pci/rescan", state.verbose)
