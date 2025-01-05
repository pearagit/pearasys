import re
from typing import Callable, Dict

import click
import typer

from pearasys.utils import get_device

PID_REGEX = r"([0-9a-fA-F]{4}):([0-9a-fA-F]{4})"
SLOT_REGEX = r"\b([0-9a-fA-F]{4}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}.\d{1})"


def parse_pid(pid: str):
    match = re.match(PID_REGEX, pid)
    if not match:
        raise typer.BadParameter("PID must be in the format vvvv:dddd")
    device = get_device(device=pid)
    if device is None:
        raise typer.BadParameter(f"No device with pid: {pid}")
    return device


def parse_slot(slot: str):
    match = re.match(SLOT_REGEX, slot)
    if not match:
        raise typer.BadParameter("Slot must be in the format dddd:dd:d.d")
    device = get_device(slot=slot)
    if device is None:
        raise typer.BadParameter(f"No devices with slot: {slot}")
    return device


class DeviceParser(click.ParamType):
    name = "Device"
    parsers: Dict[str, Callable[[str], str]] = {"slots": parse_slot, "pids": parse_pid}

    def convert(self, value, param, _):
        return self.parsers[param.name](value)
