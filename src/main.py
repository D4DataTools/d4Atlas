import json
from pathlib import Path

from loader import *
from marker import *
from helpers_geom import *
from world import * 
from render import * 


 # Globals 
IMAGE_URL = 'https://github.com/D4DataTools/d4Atlas/blob/main/docs/Sanctuary_Eastern_Continent_map.jpg'

markers = {}

processed_marker_set = {}

sno_group_map = {
    "SubZone": "Subzone"
}

process_marker_set()
write_atlas_html(markers)