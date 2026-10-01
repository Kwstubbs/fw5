import os
from pathlib import Path
import subprocess


target = Path(__file__).with_name("target.py")
subprocess.run(["python3.11", str(target)], input=os.urandom(32), check=False)