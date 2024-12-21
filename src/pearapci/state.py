from dataclasses import dataclass, field
from pathlib import Path
from typing import Annotated, Callable, Dict, List, Optional
from pylspci.device import Device


@dataclass
class PearaPCIState:
    verbose: bool = False
    devices: List[Device] = field(default_factory=List)
    driver: Path = None
