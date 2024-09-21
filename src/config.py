import yaml

DEFAULT_TRICKS = 10
DEFAULT_TREATS = 10

DATABASE_PATH = "./private/autumn.db"

# Read values from config file
CONFIG_PATH = "./private/config.yaml"
with open(CONFIG_PATH, 'r') as config_file:
    cfg = yaml.safe_load(config_file)

# Set values from config file as constants
DISCORD_KEY = cfg['discord']
STORE = cfg['store']
