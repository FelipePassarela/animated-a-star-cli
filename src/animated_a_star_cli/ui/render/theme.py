from dataclasses import dataclass


@dataclass
class Theme:
    path_color: str
    wall_color: str
    closed_color: str
    source_color: str
    dest_color: str


DEFAULT_THEME = Theme(
    path_color="bold green",
    wall_color="grey50",
    closed_color="bold yellow",
    source_color="bold",
    dest_color="bold",
)
THEME1 = Theme(
    path_color="bold magenta",
    wall_color="grey50",
    closed_color="bold yellow",
    source_color="bold blue",
    dest_color="bold red",
)
THEME2 = Theme(
    path_color="bold cyan",
    wall_color="grey50",
    closed_color="bold yellow",
    source_color="bold blue",
    dest_color="bold red",
)
