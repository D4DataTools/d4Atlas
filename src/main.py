import json
from pathlib import Path

from loader import *
from marker import *
from helpers_geom import *
from world import * 
from render import * 


 # Globals 
IMAGE_URL = 

markers = {}

processed_marker_set = {}

sno_group_map = {
    "SubZone": "Subzone"
}

process_marker_set()
write_atlas_html(markers)