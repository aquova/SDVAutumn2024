import yaml

DATABASE_PATH = "./private/autumn.db"

# Read values from config file
CONFIG_PATH = "./private/config.yaml"
with open(CONFIG_PATH, 'r') as config_file:
    cfg = yaml.safe_load(config_file)

# Set values from config file as constants
DISCORD_KEY = cfg['discord']
LEADERBOARD_URL = cfg['leaderboard']
STORE = cfg['store']
REDIRECT_CHANNELS = cfg['channels']['redirect']
EVENT_ROLES = cfg['roles']['event']
