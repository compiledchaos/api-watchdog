from api_watchdog.entry import run_cli, run_gui
from api_watchdog.cli import parse_args
import sys
from api_watchdog.utils.logger import get_logger

if __name__ == "__main__":
    args = parse_args()
    try:
        if args.cli:
            run_cli()
        else:
            run_gui()
    except Exception as e:
        logger = get_logger(name="api_watchdog", log_to_console=True, log_to_file=False)
        logger.error(f"Error: {e}")
        sys.exit(1)
