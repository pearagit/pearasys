from typing import Annotated, List, Optional

from pearasys.parser import DeviceParser
from pylspci.device import Device
import typer

from pearasys.state import PearaSysState

from pearasys.pci import app as pci_app
from pearasys.service import app as service_app


app = typer.Typer(no_args_is_help=True)
app.add_typer(pci_app, name="pci")
app.add_typer(service_app, name="service")


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
