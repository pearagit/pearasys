from typing import Annotated, Callable, Dict, List, Optional
import os

import typer
from pylspci.device import Device
from rich import print
import sys

from pearapci.utils import write_attr
from pearapci.state import PearaPCIState
from pearapci.parser import DeviceParser

from pearapci.device import app as device_app
from pearapci.driver import app as driver_app
from pearapci.service import app as service_app


app = typer.Typer()
app.add_typer(device_app, name="device")
app.add_typer(driver_app, name="driver")
app.add_typer(service_app, name="service")


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
    state = PearaPCIState(verbose, (slots or []) + (pids or []))
    ctx.obj = state


@app.command(help="/sys/bus/pci/rescan")
def rescan(ctx: typer.Context):
    state: PearaPCIState = ctx.obj
    write_attr(1, "/sys/bus/pci/rescan", state.verbose)
