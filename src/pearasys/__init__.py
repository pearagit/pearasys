from typing import Annotated, List, Optional

import typer
from pylspci.device import Device

from pearasys.parser import DeviceParser
from pearasys.pci import app as pci_app
from pearasys.service import app as service_app
from pearasys.state import PearaSysState

app = typer.Typer()
app.add_typer(pci_app, name="pci")
app.add_typer(service_app, name="service")


def recursive_help(cmd, parent=None):
    ctx = typer.Context(cmd, parent=parent)
    print(cmd.get_help(ctx))
    print()
    commands = getattr(cmd, "commands", {})
    for sub in commands.values():
        recursive_help(sub, ctx)


@app.callback()
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
    state = PearaSysState(verbose, (slots or []) + (pids or []))
    ctx.obj = state
