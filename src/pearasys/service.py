import os
import sys
from pathlib import Path
from typing import Annotated, List, Optional

import typer
from jinja2 import Environment, PackageLoader
from pylspci.device import Device
from pystemd.systemd1 import Manager as SystemdManager
from pystemd.systemd1 import Unit
from rich import inspect, print
import shutil

from pearasys.state import PearaSysState

app = typer.Typer(help="pearasys systemd service related commands.")

manager = SystemdManager()
environment = Environment(loader=PackageLoader("pearasys", "templates"))

defaults_tmpl = environment.get_template("10-defaults.conf")
bin_tmpl = environment.get_template("10-pearasys.conf")
conflict_tmpl = environment.get_template("conflict.conf")
inst_tmpl = environment.get_template("instance.service")


def get_instance_name(unit_name: str) -> str:
    _, second = unit_name.split("@")
    return second.replace(".service", "")


def get_device_units(device: Device) -> List[Path]:
    manager.load()
    units = []
    for file, _ in manager.Manager.ListUnitFilesByPatterns(
        [], [f"pearasys-{str(device.slot)}@*".encode()]
    ):
        units += [Path(file.decode())]
    return units


def parse_abs_path(value: str) -> Path:
    return Path(value).absolute()


@app.command(help="Installs a systemd service to manage a device & driver.")
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
            help="Directory to install non-instantiated service files.",
        ),
    ] = "/usr/local/lib/systemd/system",
    iprefix: Annotated[
        Optional[Path],
        typer.Option(
            "--iprefix",
            parser=parse_abs_path,
            metavar="path",
            help="Directory to install instantiated service files (i.e. `pearasys-0000:04:00.0@nvidia.service`).",
        ),
    ] = "/etc/systemd/system",
):
    state: PearaSysState = ctx.obj
    if len(state.devices) > 1:
        raise typer.BadParameter(
            "Only one device can be specified per service installation."
        )

    device = state.devices[0]

    inst_name = f"pearasys-{str(device.slot)}@{driver}.service"
    dropin_path = prefix / "pearasys-@.service.d"
    inst_path = iprefix / inst_name
    defaults_path = dropin_path / defaults_tmpl.name

    dropin_path.mkdir(parents=True, exist_ok=True)
    inst_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(inst_tmpl.filename, inst_path)
    shutil.copy(defaults_tmpl.filename, defaults_path)

    bin_path = dropin_path / bin_tmpl.name
    with open(bin_path, mode="w", encoding="utf-8") as file:
        file.write(bin_tmpl.render(pearasys_bin=sys.argv[0]))

    device_units = get_device_units(device)
    # installation is complete if there are no conflicting units
    if len(device_units) == 0 or (inst_path in device_units and len(device_units) == 1):
        return

    if inst_path not in device_units:
        device_units += [inst_path]
    for unit in device_units:
        conflicts = [u.name for u in device_units if u != unit]
        udropin_path = Path(f"{unit}.d")
        udropin_path.mkdir(parents=True, exist_ok=True)
        for conflict in conflicts:
            conflict_path = (
                udropin_path / f"{get_instance_name(conflict)}_conflict.conf"
            )
            with open(conflict_path, mode="w", encoding="utf-8") as file:
                file.write(conflict_tmpl.render(conflict=conflict))
