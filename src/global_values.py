import json
from pathlib import Path
import os
from dotenv import load_dotenv, dotenv_values
from functools import cache
load_dotenv()

IMAGE_URL = 'https://github.com/D4DataTools/d4Atlas/blob/main/docs/Sanctuary_Eastern_Continent_map.jpg?raw=true '
DATA_ROOT = os.getenv('DATA_ROOT')
VERBOSE = False
markers = {}

processed_marker_set = {}

sno_group_map = {
    "SubZone": "Subzone"
}

