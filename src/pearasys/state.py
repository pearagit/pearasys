from dataclasses import dataclass, field
from pathlib import Path
from typing import List
from pylspci.device import Device
import typer
import os
from rich import print

from pearasys.utils import err_log, select_devices


@dataclass
class PearaSysState:
    verbose: bool = False
    devices: List[Device] = field(default_factory=List)
    driver: Path = None

    def validate(self, interactive: bool = True):
        self.devices = (
            self.devices
            if len(self.devices) > 0
            else select_devices(multi=True) if interactive is True else []
        )
        if os.geteuid() != 0:
            print("[bold red]Error:[/bold red] root permissions required.")
            raise typer.Exit(1)
        if len(self.devices) == 0:
            err_log.print("[bold red]Error:[/bold red] No devices provided.")
            raise typer.Exit(1)
