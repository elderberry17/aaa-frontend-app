from aiohttp.web import run_app
from lib.app import create_app
import sys


sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')


def main() -> None:
    app = create_app()
    run_app(app, port=8000)


if __name__ == "__main__":
    main()
