from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    path_color: str
    wall_color: str
    closed_color: str
    source_color: str
    dest_color: str


MONOKAI = Theme(
    path_color="bold #a6e22e",
    wall_color="#5c6370",
    closed_color="bold #fd971f",
    source_color="bold #66d9ef",
    dest_color="bold #f92672",
)

DRACULA = Theme(
    path_color="bold #50fa7b",
    wall_color="#6272a4",
    closed_color="bold #f1fa8c",
    source_color="bold #8be9fd",
    dest_color="bold #ff79c6",
)

NORD = Theme(
    path_color="bold #88c0d0",
    wall_color="#4c566a",
    closed_color="bold #ebcb8b",
    source_color="bold #81a1c1",
    dest_color="bold #bf616a",
)

GRUVBOX = Theme(
    path_color="bold #b8bb26",
    wall_color="#665c54",
    closed_color="bold #fabd2f",
    source_color="bold #83a598",
    dest_color="bold #fb4934",
)

TOKYO_NIGHT = Theme(
    path_color="bold #9ece6a",
    wall_color="#565f89",
    closed_color="bold #e0af68",
    source_color="bold #7aa2f7",
    dest_color="bold #f7768e",
)

CATPPUCCIN = Theme(
    path_color="bold #a6e3a1",
    wall_color="#6c7086",
    closed_color="bold #f9e2af",
    source_color="bold #89b4fa",
    dest_color="bold #f38ba8",
)

DEFAULT_THEME = DRACULA

THEMES = {
    "monokai": MONOKAI,
    "dracula": DRACULA,
    "nord": NORD,
    "gruvbox": GRUVBOX,
    "tokyo-night": TOKYO_NIGHT,
    "catppuccin": CATPPUCCIN,
    "default": DEFAULT_THEME,
}
