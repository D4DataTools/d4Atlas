import d4atlas
from pathlib import Path


sanctuary = d4atlas.World.load('Sanctuary_Eastern_Continent')

print(sanctuary.zone_art)

d4atlas.render_atlas_site(sanctuary, Path('test'))