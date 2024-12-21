from itertools import groupby
from pathlib import Path
from typing import Callable

from pyfzf.pyfzf import FzfPrompt
from pylspci.device import Device
from pylspci.parsers.verbose import VerboseParser
from rich.console import Console

err_log = Console(stderr=True)

def group_by[T](lst: list[T], key: Callable[[T], str], bijective: bool = False, reverse: bool = False) -> dict[str, T] | dict[str, list[T]]:
    lst = sorted(lst, key=key)
    if reverse:
        lst.reverse()
    return {
        gkey: next(group) if bijective else list(group)
        for gkey, group in groupby(lst, key=key)
    }

def lspci(
    slot: str = None,
    device: str = None,
) -> list[Device]:
    devices = VerboseParser().run(
        verbose=True,
        kernel_drivers=True,
        hide_single_domain=False,
        slot_filter=slot,
        device_filter=device,
    )
    return devices

def get_device(
    slot: str = None,
    device: str = None,
) -> Device | None:
    return next(iter(lspci(slot=slot, device=device)), None)


def get_all_grouped_devices(devices: list[Device] = None) -> list[Device]:
    groups = set([d.iommu_group for d in devices])
    grouped_devices = group_by(lspci(), lambda d: d.iommu_group)
    return sum([grouped_devices[group] for group in groups], [])


def select_devices(
    choices: dict[str, list[Device]] = None,
    prompt: str = "Select Device: ",
    multi: bool = False,
) -> list[Device]:
    if choices is None:
        choices = {f"{d.slot.__str__()}: {d.device.__str__()}": [d] for d in lspci()}
    chosen = FzfPrompt().prompt(choices.keys(), f"--read0 {"--no-multi" if multi is False else ""} --prompt='{prompt}'", '\0')
    if multi is False:
        chosen = ["\n".join(chosen)]
    devices = [item for sublist in [choices[c] for c in chosen] for item in sublist]
    return devices

def select_iommu_group() -> list[Device]:
    device_grouping= group_by(lspci(), lambda d: d.iommu_group, reverse=True)
    choices = {}

    for iommu_group, devices in device_grouping.items():
        prefix = f"IOMMU Group {iommu_group}: "
        key = f"{prefix}{f"\n{" " * len(prefix)}".join([d.device.__str__() for d in devices])}"
        choices[key] = devices
    return (select_devices(
        choices=choices,
        prompt="Select IOMMU Group: ",
        required=True,
    ))

def device_id(device: Device) -> str:
    return f"0x{device.vendor.id:x} 0x{device.device.id:x}"


def device_path(device: Device) -> Path:
    return Path(f"/sys/bus/pci/devices/{device.slot.__str__()}")

def write_attr(data: str, path: Path, verbose: bool = False):
    if verbose:
        print(f"echo '{data}' > {path}")
    f = open(str(path), "a")
    f.write(str(data))
    f.close()



