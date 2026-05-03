from dataclasses import dataclass

from animated_a_star_cli.core.config import Config


@dataclass
class RenderContext:
    cfg: Config
