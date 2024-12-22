import typer

from pearapci.utils import write_attr, device_path, err_log
from pearapci.state import PearaPCIState

app = typer.Typer()


@app.command()
def remove(ctx: typer.Context):
    state: PearaPCIState = ctx.obj
    if len(state.devices) == 0:
        err_log.print("[bold red]Error:[/bold red] No devices provided.")
        raise typer.Exit(1)
    for device in state.devices:
        write_attr(1, device_path(device).joinpath("remove"), state.verbose)
