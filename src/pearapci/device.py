import typer

from pearapci.utils import write_attr, device_path
from pearapci.state import PearaPCIState

app = typer.Typer()


@app.command()
def remove(ctx: typer.Context):
    state: PearaPCIState = ctx.obj
    state.validate()
    for device in state.devices:
        write_attr(1, device_path(device).joinpath("remove"), state.verbose)
