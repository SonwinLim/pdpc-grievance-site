"""Run an intake subcommand with CREATIVE_HUB_DATA_DIR set to the Hub projects dir."""
import os
import sys

os.environ["CREATIVE_HUB_DATA_DIR"] = r"E:\Bespoke\Minimax_Hub\projects"

# Now invoke the intake CLI
from pathlib import Path
sys.path.insert(0, r"E:\Bespoke\Minimax_Hub")
sys.path.insert(0, r"E:\Bespoke\Minimax_Hub\.venv\Lib\site-packages")

# Use the same python interpreter as the shell
import runpy
sys.argv[0] = "intake"
runpy.run_module("intake", run_name="__main__", alter_sys=True)