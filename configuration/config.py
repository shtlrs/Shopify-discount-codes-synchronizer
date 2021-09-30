import configparser
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

EXECUTION_TIME_INTERVAL = int(os.getenv("EXECUTION_TIME_INTERVAL"))

# The path to configuration package
CONFIG_DIRECTORY = Path(__file__).parent

# Representation of config.ini as Path
CONFIG_INI_FILENAME = Path("config.ini")

# Path of config.ini
CONFIG_INI_FILE = CONFIG_DIRECTORY.joinpath(CONFIG_INI_FILENAME)

config = configparser.ConfigParser()
config.read(CONFIG_INI_FILE.absolute().as_posix())

sections = [config[section_name] for section_name in config.sections()]

