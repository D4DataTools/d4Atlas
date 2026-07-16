from pathlib import Path
from global_values import *

def calc_zone_art(world):
    zone_map_params = world.get('tZoneMapParams')
    zone_art_center = zone_map_params.get('vecZoneArtCenter')
    zone_art_scale = zone_map_params.get('flZoneArtScale')
    grid_size = world.get('flGridSize')
    
    return {
        "x": -1 * zone_art_center.get('x') / zone_art_scale,
        "y": -1 * zone_art_center.get('y') / zone_art_scale,
        "w": zone_map_params.get('nGridSystemZoneMapFieldWidth') * grid_size, 
        "h": zone_map_params.get('nGridSystemZoneMapFieldHeight') * grid_size
    }

def write_atlas_html(borders, markers, zone_art):

    markers = sorted(markers.values(), reverse=True)

    html = f"""<!DOCTYPE html>
    <html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
              rel="stylesheet">

        <script src="https://unpkg.com/panzoom@9.4.0/dist/panzoom.min.js"></script>

        <link href="atlas.css" rel="stylesheet">

        <style id="dynamic-css"></style>
    </head>

    <body>

    <div class="search-input">
        <input
            type="search"
            id="search-input"
            class="form-control"
            placeholder="Search..."
            value="dungeon location">
    </div>

    <svg
        viewBox="-1284 -2618 3564 3564"
        xmlns="http://www.w3.org/2000/svg"
        style="width:100%;height:100%;">

        <g
            id="atlas-group"
            transform="matrix(3.6466190067585558 0 0 3.6466190067585558 -3030 3625)">

            <image
                href="{IMAGE_URL}"
                 preserveAspectRatio="none" 
                 x="{zone_art.get("x")}" 
                 y="{zone_art.get("y")}" 
                 width="{zone_art.get("w")}" 
                 height="{zone_art.get("h")}">


                <title>Sanctuary Eastern Continent</title>

            </image>

            <g transform="scale(-1,1) rotate(45)">

    {"".join("            " + b + "\n" for b in borders)}

    {"".join("            " + m + "\n" for m in markers)}

            </g>

        </g>

    </svg>

    <script src="atlas.js"></script>

    </body>
    </html>
    """

    try: 
        script_parent_dir = Path(__file__).parent
    except (NameError, TypeError):
        script_parent_dir = Path(os.getcwd())

    output_dir = script_parent_dir.parent / 'docs' / 'atlas.html'

    output_dir.write_text(html, encoding="utf-8")

    return


