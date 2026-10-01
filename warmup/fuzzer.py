import subprocess
import sys
from pathlib import Path


target = Path(__file__).with_name("target.py")
subprocess.run([sys.executable, str(target)], input="a==b", text=True, check=False)
