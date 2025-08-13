from api_watchdog.cli import parse_args
from api_watchdog.entry import run_cli, run_gui

if __name__ == "__main__":
    args = parse_args()
    if args.cli:
        run_cli()
    else:
        run_gui()
