from . import config

def main():
    configs = config.load_config()
    print("Loaded config:")
    print(configs)
