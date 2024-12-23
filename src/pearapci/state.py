from dataclasses import dataclass, field
from pathlib import Path
from typing import List
from pylspci.device import Device
import typer

from pearapci.utils import err_log, select_devices


@dataclass
class PearaPCIState:
    verbose: bool = False
    devices: List[Device] = field(default_factory=List)
    driver: Path = None

    def validate(self):
        self.devices = (
            self.devices if len(self.devices) > 0 else select_devices(multi=True)
        )
        if len(self.devices) == 0:
            err_log.print("[bold red]Error:[/bold red] No devices provided.")
            raise typer.Exit(1)
