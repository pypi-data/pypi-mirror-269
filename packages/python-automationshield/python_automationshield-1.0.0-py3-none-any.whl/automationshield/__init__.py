# read version from installed package
from importlib.metadata import version
__version__ = version("python_aeroshield")

from .controller import ShieldController
from .exception import AutomationShieldException
from .shields import AeroShield, FloatShield, MagnetoShield, DummyShield


import platform

from pathlib import Path

from .arduino import download_cli, setup_cli, cli_dir, cli_path

system = platform.system()

if system in ("Windows", "Linux", "Darwin"):
    if not cli_dir.exists():
        print(f"Downloading arduino-cli to {cli_dir}")
        download_cli(system)
        print("Performing setup for arduino-cli")
        setup_cli()

    else:
        print(f"Arduino-cli found in {cli_dir}")

else:
    print("Arduino-cli not available for current machine")
