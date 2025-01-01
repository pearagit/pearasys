from pathlib import Path
from typing import Annotated
from pylspci.device import Device
from pystemd.systemd1 import Unit, Manager
from dataclasses import asdict
import jinja2
import shutil
import typer

from pearapci.state import PearaPCIState
from pearapci.driver import parse_driver, bind, unbind

app = typer.Typer(help="Helper for pearapci systemd service.")


def load_service_unit(device: Device, driver: Path) -> Unit:
    unit = Unit(f"pearapci-{str(device.slot)}@{str(driver)}.service")
    unit.load()
    return unit


@app.callback()
def callback(
    ctx: typer.Context,
    driver: Annotated[
        Path,
        typer.Argument(parser=parse_driver, metavar="driver_name", show_default=False),
    ],
):
    state = ctx.obj
    state.driver = driver


@app.command()
def start(
    ctx: typer.Context,
):
    state: PearaPCIState = ctx.obj
    manager = Manager()
    manager.Manager
    for device in state.devices:
        if str(device.driver) == state.driver.name:
            continue
        lstate = PearaPCIState(**asdict(state))
        lstate.devices = [device]
        bind(lstate)


@app.command()
def stop(
    ctx: typer.Context,
):
    state: PearaPCIState = ctx.obj
    for device in state.devices:
        if device.driver is None:
            continue
        unbind(parse_driver(device.driver), [device])


@app.command()
def install(
    ctx: typer.Context,
):

    service_file = Path(__file__).parent / "pearapci-device@driver.service"
