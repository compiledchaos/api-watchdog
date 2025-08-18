
import sys, os, pathlib
# Add project root (which contains the 'api_watchdog' package) to sys.path
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
