"""Verify execution runtime, hardware, package versions, and write access for STEP-023 (local CPU or Kaggle GPU)."""

from __future__ import annotations

import json
import os
import platform
import sys
import tempfile
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any


def _pkg_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "not-installed"


def collect_runtime_inventory() -> dict[str, Any]:
    """Inspect actual OS, Python, installed packages, GPU/CUDA state, and write permissions."""
    inv: dict[str, Any] = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "os": platform.platform(),
        "machine": platform.machine(),
        "python_version": sys.version.split()[0],
        "cpu_count": os.cpu_count(),
        "packages": {
            "numpy": _pkg_version("numpy"),
            "pillow": _pkg_version("pillow"),
            "opencv-python": _pkg_version("opencv-python"),
            "PyYAML": _pkg_version("PyYAML"),
            "pytest": _pkg_version("pytest"),
            "onnxruntime": _pkg_version("onnxruntime"),
            "torch": _pkg_version("torch"),
            "torchvision": _pkg_version("torchvision"),
            "ultralytics": _pkg_version("ultralytics"),
        },
        "gpu": {
            "cuda_available": False,
            "device_count": 0,
            "devices": [],
            "torch_cuda_version": "N/A",
            "cudnn_version": "N/A",
        },
        "smoke_checks": {
            "write_permission_ok": False,
            "onnxruntime_import_ok": False,
            "torch_tensor_smoke_ok": False,
            "ultralytics_import_ok": False,
        },
    }

    # Check temp write permission
    try:
        with tempfile.TemporaryDirectory() as tmpd:
            probe = Path(tmpd) / "write_probe.txt"
            probe.write_text("ok", encoding="utf-8")
            inv["smoke_checks"]["write_permission_ok"] = probe.read_text(encoding="utf-8") == "ok"
    except OSError as exc:
        inv["smoke_checks"]["write_permission_error"] = str(exc)

    # Check onnxruntime
    try:
        import onnxruntime as ort  # noqa: F401

        inv["smoke_checks"]["onnxruntime_import_ok"] = True
        inv["onnxruntime_providers"] = ort.get_available_providers()
    except Exception:
        pass

    # Check PyTorch & CUDA if installed
    try:
        import torch

        cuda_ok = bool(torch.cuda.is_available())
        inv["gpu"]["cuda_available"] = cuda_ok
        inv["gpu"]["torch_cuda_version"] = str(torch.version.cuda or "none")
        inv["gpu"]["cudnn_version"] = str(torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else "none")
        if cuda_ok:
            cnt = int(torch.cuda.device_count())
            inv["gpu"]["device_count"] = cnt
            devices = []
            for idx in range(cnt):
                props = torch.cuda.get_device_properties(idx)
                devices.append(
                    {
                        "index": idx,
                        "name": torch.cuda.get_device_name(idx),
                        "total_vram_gb": round(props.total_memory / (1024**3), 2),
                    }
                )
            inv["gpu"]["devices"] = devices
            x = torch.randn((1, 3, 64, 64), device="cuda:0")
            inv["smoke_checks"]["torch_tensor_smoke_ok"] = tuple(x.shape) == (1, 3, 64, 64)
        else:
            x = torch.randn((1, 3, 64, 64), device="cpu")
            inv["smoke_checks"]["torch_tensor_smoke_ok"] = tuple(x.shape) == (1, 3, 64, 64)
    except ImportError:
        pass

    # Check Ultralytics if installed
    try:
        import ultralytics

        inv["smoke_checks"]["ultralytics_import_ok"] = True
        inv["ultralytics_reported_version"] = str(getattr(ultralytics, "__version__", "unknown"))
    except ImportError:
        pass

    return inv


def main() -> None:
    inv = collect_runtime_inventory()
    print(json.dumps(inv, indent=2))


if __name__ == "__main__":
    main()
