"""
Rough draft of a script to get the total and free space of all physical drives on a system.
"""

import logging
from typing import Any

import psutil

LOGGER = logging.getLogger(__name__)


def convert_bytes_to_gb(bytes_value: int) -> str:
    """
    Convert bytes to gigabytes.

    Args:
        bytes_value (int): The value in bytes.

    Returns:
        str: The value in gigabytes, formatted as a string with 2 decimal places.
    """
    gb_value = bytes_value / (1024**3)
    return f"{gb_value:.2f} GB"


ignore_fs_types = {
    "proc",
    "sysfs",
    "tmpfs",
    "devtmpfs",
    "devfs",
    "squashfs",
    "cgroup",
    "cgroup2",
    "overlay",
    "none",
    "autofs",
    "rpc_pipefs",
    "hugetlbfs",
    "tracefs",
    "mqueue",
    "securityfs",
    "debugfs",
    "binfmt_misc",
    "configfs",
    "efivarfs",
    "fuse.gvfsd-fuse",
    "fuse.gvfs-fuse-daemon",
    "fusectl",
    "pstore",
    "sys_kernel_debug",
    "sys_kernel_config",
}


def get_drive_info() -> list[dict[str, Any]]:
    """
    Get a list of all physical mounted drives with their total and free space, excluding virtual or system mounts.

    Returns:
        list[dict[str, Any]]: A list of dictionaries each containing the mount point, total space, and free space.
    """
    drives = []
    for partition in psutil.disk_partitions():
        if partition.fstype not in ignore_fs_types:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                drive = {
                    "Mount Point": partition.mountpoint,
                    "Total Space": convert_bytes_to_gb(usage.total),
                    "Free Space": convert_bytes_to_gb(usage.free),
                }
                drives.append(drive)
            except PermissionError:
                LOGGER.debug(f"Access denied to {partition.mountpoint}")
            except Exception as e:
                LOGGER.debug(f"Could not access {partition.mountpoint}: {e}")
    return drives
