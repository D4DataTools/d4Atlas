import json
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv, dotenv_values
load_dotenv()

@dataclass
class D4AtlasConfig: 
    verbose: bool = False
    debug: bool = False
    show_timings: bool = False
    show_cache_hits: bool = False
    loglevel: str = 'INFO'
    data_root: Path | None = (
        Path(os.getenv("DATA_ROOT"))
        if os.getenv("DATA_ROOT")
        else None
    )
    image_url: str = 'https://github.com/D4DataTools/d4Atlas/blob/main/docs/Sanctuary_Eastern_Continent_map.jpg?raw=true'

SNO_GROUP_MAP = {
    "SubZone": "Subzone"
}

