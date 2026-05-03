import sys

from animated_a_star_cli.core import config
from animated_a_star_cli.core.astar_state import AStarState
from animated_a_star_cli.ui import parser, render
from animated_a_star_cli.ui.render_context import RenderContext


def main():
    cfg = _load_config()
    astar_state = AStarState()
    render_ctx = RenderContext(cfg, astar_state)
    render.draw(render_ctx)


def _load_config() -> config.Config:  # ty:ignore[invalid-return-type]
    error_prefix = "Error loading config:"

    try:
        return parser.load_config()
    except FileNotFoundError:
        _print_error_and_exit(f"{error_prefix}: Config file not found.", exit_code=3)
    except parser.ParserError as e:
        error_msg = (
            f"{error_prefix} {str(e).capitalize()}. Please check your config file."
        )
        _print_error_and_exit(error_msg, exit_code=2)
    except Exception as e:
        _print_error_and_exit(
            f"Unexpected error while loading config: {e}", exit_code=1
        )


def _print_error_and_exit(message: str, exit_code: int = 1):
    print(message)
    sys.exit(exit_code)
