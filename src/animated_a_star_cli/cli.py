import sys

from animated_a_star_cli.core import config
from animated_a_star_cli.ui import parser, render
from animated_a_star_cli.ui.render_context import RenderContext


def main():
    cfg = _load_config()
    render_ctx = RenderContext(cfg)
    render.draw(render_ctx)


def _load_config() -> config.Config:  # ty:ignore[invalid-return-type]
    try:
        return parser.load_config()
    except FileNotFoundError:
        _print_error_and_exit("Config file not found.", exit_code=3)
    except parser.ParserError as e:
        error_msg = (
            f"Error loading config: {str(e).capitalize()}. "
            "Please check your config file."
        )
        _print_error_and_exit(error_msg, exit_code=2)
    except Exception as e:
        _print_error_and_exit(f"Unexpected error: {e}", exit_code=1)


def _print_error_and_exit(message: str, exit_code: int = 1):
    print(message)
    sys.exit(exit_code)
