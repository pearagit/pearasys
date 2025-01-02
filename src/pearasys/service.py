from pathlib import Path
from typing import Annotated, List, Optional
from pylspci.device import Device
from pystemd.systemd1 import Unit, Manager as SystemdManager
import typer
from jinja2 import Environment, PackageLoader
import sys

from pearasys.state import PearaSysState
from pearasys.pci.driver import parse_driver
from pearasys.parser import DeviceParser

app = typer.Typer(help="pearasys systemd service related commands.")

manager = SystemdManager()
environment = Environment(loader=PackageLoader("pearasys", "templates"))
template = environment.get_template("pearasys-device@driver.service")


def install_service(name: str, content: str):
    pass


def load_service_unit(device: Device, driver: Path) -> Unit:
    unit = Unit(f"pearasys-{str(device.slot)}@{str(driver)}.service")
    unit.load()
    return unit


def get_device_unit_files(device: Device) -> List[Path]:
    manager.load()
    units = list()
    for file, _ in manager.Manager.ListUnitFilesByPatterns(
        [], [f"pearasys-{str(device.slot)}@*".encode()]
    ):
        units += Path(file.decode())
    return units


@app.callback()
def callback(
    ctx: typer.Context,
    driver: Annotated[
        Path,
        typer.Argument(parser=parse_driver, metavar="driver_name", show_default=False),
    ],
):
    state: PearaSysState = ctx.obj
    # service commands can safely use the context state as commands are not chained
    state.driver = driver
    state.validate()


@app.command()
def install(
    ctx: typer.Context,
    prefix: Annotated[
        Optional[Path],
        typer.Option(
            "--prefix",
            parser=lambda value: Path(value).absolute(),
            help="Specify the service installation directory, must be an absolute path.",
        ),
    ] = "/etc/systemd/system",
):
    state: PearaSysState = ctx.obj
    if len(state.devices) > 1:
        raise typer.BadParameter(
            "Only one device can be specified for service installation."
        )
    device = state.devices[0]
    text = template.render(pearasys_bin=sys.argv[0], conflicts=[])
    print(prefix)
    # print(get_device_unit_files(device))
    # environment = Environment(
    #     loader=FileSystemLoader(Path(__file__).parent.parent / "templates")
    # )
    # template = environment.get_template("pearasys-device@driver.service")
    # units.append(
    #     Path("/etc/systemd/system/")
    #     / (f"pearasys-{str(device.slot)}@{state.driver.name}.service")
    # )
    # new_unit = f"pearasys-{str(device.slot)}@{state.driver.name}.service"
    # service_file = (
    #     Path("/etc/systemd/system/")
    #     / f"pearasys-{str(device.slot)}@{state.driver.name}.service"
    # )

    # print(units)
    # for unit_file in units:
    #     conflicts = []
    #     for conflict in units:
    #         if conflict != unit_file:
    #             conflicts.append(conflict)
    #     content = template.render(pearasys_bin=sys.argv[0], conflicts=conflicts)
    #     with open(unit_file, mode="w", encoding="utf-8") as file:
    #         file.write(content)

    # for device in state.devices:
    #     environment = Environment(
    #         loader=FileSystemLoader(Path(__file__).parent.parent / "templates")
    #     )
    #     template = environment.get_template("pearasys-device@driver.service")
    #     path = (
    #         Path("/etc/systemd/system/")
    #         / f"pearasys-{str(device.slot)}@{state.driver.name}.service"
    #     )
    #     content = template.render(pearasys_bin=sys.argv[0])
    #     with open(path, mode="w", encoding="utf-8") as file:
    #         file.write(content)
    # print(service_file)


# @app.command()
# def start(
#     slot: Annotated[
#         Device,
#         typer.Argument(
#             help="<domain>:<bus>:<device>.<func>",
#             metavar="slot",
#             click_type=DeviceParser(),
#             show_default=False,
#         ),
#     ],
#     driver: Annotated[
#         Path,
#         typer.Argument(parser=parse_driver, metavar="driver_name", show_default=False),
#     ],
# ):
#     # bind(driver , [device], True)
#     pass
#     # for device in state.devices:
#     #     if str(device.driver) == state.driver.name:
#     #         continue
#     #     lstate = PearaSysState(**asdict(state))
#     #     lstate.devices = [device]
#     #     bind(lstate)
#
#
# @app.command()
# def stop(
#     ctx: typer.Context,
#     slot: Annotated[
#         Device,
#         typer.Argument(
#             help="<domain>:<bus>:<device>.<func>",
#             metavar="slot",
#             click_type=DeviceParser(),
#             show_default=False,
#         ),
#     ],
#     driver: Annotated[
#         Path,
#         typer.Argument(parser=parse_driver, metavar="driver_name", show_default=False),
#     ],
# ):
#     state: PearaSysState = ctx.obj
#     for device in state.devices:
#         if device.driver is None:
#             continue
#         unbind(parse_driver(device.driver), [device])
#
#
