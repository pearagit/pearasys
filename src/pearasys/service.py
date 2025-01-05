import os
import sys
from pathlib import Path
from typing import Annotated, List, Optional

import typer
from jinja2 import Environment, PackageLoader
from pylspci.device import Device
from pystemd.systemd1 import Manager as SystemdManager
from pystemd.systemd1 import Unit
from rich import print

from pearasys.state import PearaSysState

app = typer.Typer(help="pearasys systemd service related commands.")

manager = SystemdManager()
environment = Environment(loader=PackageLoader("pearasys", "templates"))
template = environment.get_template("pearasys-device@driver.service")


def load_service_unit(device: Device, driver: Path) -> Unit:
    unit = Unit(f"pearasys-{str(device.slot)}@{str(driver)}.service")
    unit.load()
    return unit


def get_device_service_files(device: Device) -> List[Path]:
    manager.load()
    units = []
    for file, _ in manager.Manager.ListUnitFilesByPatterns(
        [], [f"pearasys-{str(device.slot)}@*".encode()]
    ):
        units += [Path(file.decode())]
    return units


def parse_abs_path(value: str) -> Path:
    return Path(value).absolute()


@app.command(help="Installs a systemd service to manage a device's driver.")
def install(
    ctx: typer.Context,
    driver: Annotated[
        str,
        typer.Argument(metavar="driver_name", show_default=False),
    ],
    prefix: Annotated[
        Optional[Path],
        typer.Option(
            "--prefix",
            parser=parse_abs_path,
            metavar="path",
            help="Specify the service installation directory.",
        ),
    ] = "/etc/systemd/system",
):
    state: PearaSysState = ctx.obj
    if len(state.devices) > 1:
        raise typer.BadParameter(
            "Only one device can be specified per service installation."
        )

    device = state.devices[0]
    device_unit_files = get_device_service_files(device)
    new_unit_name = f"pearasys-{str(device.slot)}@{driver}.service"
    new_unit_file = prefix / new_unit_name
    if new_unit_file not in device_unit_files:
        device_unit_files += [new_unit_file]
    for unit_file in device_unit_files:
        conflicts = [u.name for u in device_unit_files if u != unit_file]
        content = template.render(pearasys_bin=sys.argv[0], conflicts=conflicts)
        with open(unit_file, mode="w", encoding="utf-8") as file:
            file.write(content)
    os.system("systemctl daemon-reload")
    print(
        f"Service installed successfully. Start service with command: [orange1]`systemctl start {new_unit_name}`[/orange1]"
    )
