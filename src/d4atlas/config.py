import json
from dataclasses import dataclass
from dotenv import load_dotenv, dotenv_values
load_dotenv()

@dataclass
class D4AtlasConfig: 
    verbose: bool = False
    DEBUG: bool = False
    show_timings: bool = False
    show_cache_hits: bool = False
    LOGLEVEL: str = 'INFO'
    IMAGE_URL: str = 'https://github.com/D4DataTools/d4Atlas/blob/main/docs/Sanctuary_Eastern_Continent_map.jpg?raw=true'

DATA_ROOT = os.getenv('DATA_ROOT') or ""

SNO_GROUP_MAP = {
    "SubZone": "Subzone"
}

