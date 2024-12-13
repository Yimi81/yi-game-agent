from pathlib import Path
print(str(Path.home()))
import os
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))