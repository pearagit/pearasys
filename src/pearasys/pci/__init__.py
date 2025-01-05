import typer

from pearasys.pci.device import app as device_app
from pearasys.pci.driver import app as driver_app
from pearasys.state import PearaSysState
from pearasys.utils import write_attr

app = typer.Typer(
    chain=True,
    help="Access PCI related resources under `/sys/bus/pci`",
)

app.add_typer(device_app, name="device")
app.add_typer(driver_app, name="driver")


@app.command(help="Forces a rescan and re-discovers removed devices.")
def rescan(ctx: typer.Context):
    state: PearaSysState = ctx.obj
    write_attr(1, "/sys/bus/pci/rescan", state.verbose)
