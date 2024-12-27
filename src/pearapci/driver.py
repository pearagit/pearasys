from pathlib import Path
from typing import Annotated, List, Optional
from pylspci.device import Device
from dataclasses import asdict
import typer
import os

from pearapci.state import PearaPCIState
from pearapci.utils import write_attr, device_id
from pearapci.parser import DeviceParser

app = typer.Typer()
state: PearaPCIState = None


def parse_driver(value: str):
    driver = Path(f"/sys/bus/pci/drivers/{value}")
    if not driver.exists():
        raise typer.BadParameter(
            f"Driver {value} is not present, try `sudo modprobe {value}`, or even `sudo modprobe -f {value}`"
        )
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
        state = PearaPCIState(**asdict(state))
        state.devices = devices
    state.driver = driver
    if ctx.invoked_subcommand != "ls":
        state.validate()


@app.command()
def bind():
    global state
    for device in state.devices:
        write_attr(device.slot.__str__(), state.driver.joinpath("bind"), state.verbose)


@app.command()
def unbind():
    global state
    for device in state.devices:
        write_attr(
            device.slot.__str__(), state.driver.joinpath("unbind"), state.verbose
        )


@app.command()
def new_id():
    global state
    for device in state.devices:
        write_attr(
            device_id(device),
            state.driver.joinpath("new_id"),
            state.verbose,
        )


@app.command()
def remove_id():
    global state
    for device in state.devices:
        write_attr(
            device_id(device),
            state.driver.joinpath("remove_id"),
            state.verbose,
        )


@app.command()
def ls():
    global state
    os.system(f"ls -lah --color=always {state.driver}")
