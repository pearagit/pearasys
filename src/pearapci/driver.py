from pathlib import Path
from typing import Annotated
import typer

from pearapci.state import PearaPCIState
from pearapci.utils import write_attr, device_id, err_log

app = typer.Typer()


def parse_driver(value: str):
    driver = Path(f"/sys/bus/pci/drivers/{value}")
    if not driver.exists():
        raise typer.BadParameter(
            f"Driver {value} is not present, try `sudo modprobe {value}`"
        )
    return driver


@app.callback()
def callback(
    ctx: typer.Context,
    driver: Annotated[
        Path,
        typer.Argument(parser=parse_driver, metavar="driver_name", show_default=False),
    ],
):
    state: PearaPCIState = ctx.obj
    state.driver = driver
    if len(state.devices) == 0:
        err_log.print("[bold red]Error:[/bold red] No devices provided.")
        raise typer.Exit(1)


@app.command()
def bind(
    ctx: typer.Context,
):
    state: PearaPCIState = ctx.obj
    for device in state.devices:
        write_attr(device.slot.__str__(), state.driver.joinpath("bind"), state.verbose)


@app.command()
def unbind(
    ctx: typer.Context,
):
    state: PearaPCIState = ctx.obj
    for device in state.devices:
        write_attr(
            device.slot.__str__(), state.driver.joinpath("unbind"), state.verbose
        )


@app.command()
def new_id(
    ctx: typer.Context,
):
    state: PearaPCIState = ctx.obj
    for device in state.devices:
        write_attr(
            device_id(device),
            state.driver.joinpath("new_id"),
            state.verbose,
        )


@app.command()
def remove_id(
    ctx: typer.Context,
):
    state: PearaPCIState = ctx.obj
    for device in state.devices:
        write_attr(
            device_id(device),
            state.driver.joinpath("remove_id"),
            state.verbose,
        )
