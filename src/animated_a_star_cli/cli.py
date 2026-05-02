import sys

from . import config


def main():
    try:
        cfg = config.load_config()
        print("Loaded config:")
        print(cfg)
    except FileNotFoundError:
        print("Config file not found.")
        sys.exit(3)
    except config.ConfigError as e:
        error_msg = f"{str(e).capitalize()}. Please check your config file."
        print(f"Error loading config: {error_msg}")
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
