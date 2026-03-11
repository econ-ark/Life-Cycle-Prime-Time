#!/usr/bin/env python3
"""
System Information Capture for Life-Cycle-Prime-Time Benchmarking

Captures system, environment, and git information for reproducible
benchmark reporting. Adapted from HAFiscal's capture_system_info.py.
"""

import json
import os
import platform
import subprocess
import sys
from pathlib import Path


def run_command(cmd, fallback="unknown"):
    """Run a shell command and return output, or fallback on error."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else fallback
    except (subprocess.TimeoutExpired, Exception):
        return fallback


def get_cpu_info():
    """Get CPU information cross-platform."""
    system = platform.system()

    cpu_info = {
        "model": "unknown",
        "architecture": platform.machine(),
        "cores_physical": None,
        "cores_logical": os.cpu_count(),
        "frequency_mhz": None,
    }

    if system == "Darwin":
        cpu_info["model"] = run_command("sysctl -n machdep.cpu.brand_string")
        physical = run_command("sysctl -n hw.physicalcpu")
        cpu_info["cores_physical"] = int(physical) if physical.isdigit() else None
        freq = run_command("sysctl -n hw.cpufrequency_max")
        if freq.isdigit():
            cpu_info["frequency_mhz"] = int(freq) / 1_000_000

    elif system == "Linux":
        model = run_command("lscpu | grep 'Model name' | cut -d ':' -f 2")
        if model != "unknown":
            cpu_info["model"] = model.strip()
        else:
            cpu_info["model"] = run_command(
                "cat /proc/cpuinfo | grep 'model name' | head -1 | cut -d ':' -f 2"
            ).strip()

        physical = run_command(
            "lscpu | grep 'Core(s) per socket' | awk '{print $NF}'"
        )
        sockets = run_command("lscpu | grep 'Socket(s)' | awk '{print $NF}'")
        if physical.isdigit() and sockets.isdigit():
            cpu_info["cores_physical"] = int(physical) * int(sockets)

        freq = run_command("lscpu | grep 'CPU max MHz' | awk '{print $NF}'")
        if freq.replace(".", "").isdigit():
            cpu_info["frequency_mhz"] = float(freq)

    return cpu_info


def get_memory_info():
    """Get memory information in GB."""
    system = platform.system()

    memory_info = {"total_gb": None, "available_gb": None}

    if system == "Darwin":
        total = run_command("sysctl -n hw.memsize")
        if total.isdigit():
            memory_info["total_gb"] = round(int(total) / (1024**3), 2)
        available = run_command(
            "vm_stat | grep 'Pages free' | awk '{print $3}' | sed 's/\\.//'"
        )
        if available.isdigit():
            memory_info["available_gb"] = round(
                int(available) * 4096 / (1024**3), 2
            )

    elif system == "Linux":
        total = run_command("grep MemTotal /proc/meminfo | awk '{print $2}'")
        if total.isdigit():
            memory_info["total_gb"] = round(int(total) / (1024**2), 2)
        available = run_command(
            "grep MemAvailable /proc/meminfo | awk '{print $2}'"
        )
        if available.isdigit():
            memory_info["available_gb"] = round(int(available) / (1024**2), 2)

    return memory_info


def get_disk_info(path="/"):
    """Get disk information for the given path."""
    try:
        stat = os.statvfs(path)
        free_gb = round((stat.f_bavail * stat.f_frsize) / (1024**3), 2)

        disk_type = "unknown"
        system = platform.system()

        if system == "Darwin":
            dt = run_command(
                "diskutil info / | grep 'Solid State' | awk '{print $3}'"
            )
            disk_type = "SSD" if dt == "Yes" else ("HDD" if dt == "No" else "unknown")
        elif system == "Linux":
            rotational = run_command(
                "cat /sys/block/$(df / | tail -1 | awk '{print $1}'"
                " | sed 's|/dev/||' | sed 's/[0-9]//g')/queue/rotational 2>/dev/null"
            )
            if rotational == "0":
                disk_type = "SSD"
            elif rotational == "1":
                disk_type = "HDD"

        return {"type": disk_type, "free_gb": free_gb}
    except Exception:
        return {"type": "unknown", "free_gb": None}


def get_python_packages():
    """Get versions of key Python packages for this project."""
    packages = {}
    key_packages = [
        "econ-ark",
        "HARK",
        "estimagic",
        "numpy",
        "scipy",
        "statsmodels",
        "pandas",
        "matplotlib",
        "dask",
        "numba",
    ]

    for pkg in key_packages:
        try:
            from importlib.metadata import version

            packages[pkg] = version(pkg)
        except Exception:
            packages[pkg] = "not installed"

    return packages


def get_git_info(repo_path=None):
    """Get git repository information."""
    if repo_path is None:
        repo_path = Path(__file__).parent.parent

    original_dir = os.getcwd()
    try:
        os.chdir(repo_path)

        commit = run_command("git rev-parse HEAD", "unknown")
        branch = run_command("git rev-parse --abbrev-ref HEAD", "unknown")
        dirty = run_command(
            "git diff --quiet && echo 'false' || echo 'true'", "unknown"
        )

        return {
            "commit": commit,
            "branch": branch,
            "dirty": dirty == "true",
        }
    finally:
        os.chdir(original_dir)


def capture_system_info():
    """Capture complete system information."""
    info = {
        "system": {
            "os": platform.system(),
            "os_version": platform.release(),
            "kernel": platform.version(),
            "hostname": platform.node(),
            "cpu": get_cpu_info(),
            "memory": get_memory_info(),
            "disk": get_disk_info(),
        },
        "environment": {
            "python_version": platform.python_version(),
            "environment_type": "unknown",
            "virtual_env": os.environ.get("VIRTUAL_ENV", None),
            "key_packages": get_python_packages(),
        },
        "git": get_git_info(),
    }

    if os.environ.get("VIRTUAL_ENV"):
        if ".venv" in os.environ.get("VIRTUAL_ENV", ""):
            info["environment"]["environment_type"] = "uv"
        else:
            info["environment"]["environment_type"] = "venv"
    elif os.environ.get("CONDA_DEFAULT_ENV"):
        info["environment"]["environment_type"] = "conda"

    return info


def main():
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Capture system information for benchmarking"
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file (default: stdout)",
        type=str,
    )
    parser.add_argument(
        "--pretty",
        "-p",
        help="Pretty-print JSON",
        action="store_true",
    )

    args = parser.parse_args()

    info = capture_system_info()

    indent = 2 if args.pretty else None
    output = json.dumps(info, indent=indent)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"System information saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
