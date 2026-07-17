
from pathlib import Path
from d4atlas.config import CONFIG
from d4atlas import World

#' Render the atlas.html for the d4 Atlas Website
#'
#' @param world an object of type `World`
#' @param output a `Path` to a directory to write the site. if unspecified defaults to creating relative to the script in `/docs/atlas.html`
#' @param image_url a 'str' with a link to the hosted image URL for the background
def render_atlas_html (world: World, output: Path = None, image_url: str = CONFIG.image_url): 
    html_template = (
        Path(__file__).parent 
        / 'templates'
        / 'atlas.html'
    ).read_text()

    html = html_template.format(
        image_url = image_url, 
        joined_markers = "".join("            " + m + "\n" for m in world.markers.values()), 
        joined_region_boundries =  "".join("            " + b + "\n" for b in world.region_boundaries),
        zone_x = world.zone_art.get('x'),
        zone_y = world.zone_art.get('y'),
        zone_w = world.zone_art.get('w'),
        zone_h = world.zone_art.get('h'),
    ) 

    if not output: 
        raise Warning('output not specified defaulting to `/docs/atlas.html')
        try: 
            script_parent_dir = Path(__file__).parent
        except (NameError, TypeError):
            script_parent_dir = Path(os.getcwd())
            output = script_parent_dir.parent / 'docs' 

    output = output / 'atlas.html'
    output.parent.mkdir(parents=True, exist_ok=True) 
    output.write_text(html, encoding="utf-8")

#' Render the atlas.css file for the d4Atlas Website
#'
#' @param world an object of type `World`
#' @param output a `Path` to a directory to write the site. if unspecified defaults to creating relative to the script in `/docs/atlas.css`
#' @param image_url a 'str' with a link to the hosted image URL for the background
def render_atlas_css(output: Path = None): 

    css_template = (
        Path(__file__).parent 
        / 'templates'
        / 'atlas.css'
    ).read_text()

    if not output: 
        raise Warning('output not specified defaulting to `/docs/atlas.html')
        try: 
            script_parent_dir = Path(__file__).parent
        except (NameError, TypeError):
            script_parent_dir = Path(os.getcwd())
            output = script_parent_dir.parent / 'docs'

    output = output /  'atlas.css'
    output.parent.mkdir(parents=True, exist_ok=True) 
    output.write_text(css_template, encoding="utf-8")

#' Render the atlas.js file for the d4Atlas Website
#'
#' @param world an object of type `World`
#' @param output a `Path` to a directory to write the site. if unspecified defaults to creating relative to the script in `/docs/atlas.js`
#' @param image_url a 'str' with a link to the hosted image URL for the background
def render_atlas_js(output: Path = None): 
    js_template = (
        Path(__file__).parent 
        / 'templates'
        / 'atlas.js'
    ).read_text()

    if not output: 
        raise Warning('output not specified defaulting to `/docs/atlas.html')
        try: 
            script_parent_dir = Path(__file__).parent
        except (NameError, TypeError):
            script_parent_dir = Path(os.getcwd())
            output = script_parent_dir.parent / 'docs' 

    output = output / 'atlas.js'
    output.parent.mkdir(parents=True, exist_ok=True) 
    output.write_text(js_template, encoding="utf-8")

#' Render the d4Atlas Website
#'
#' @param world an object of type `World`
#' @param output a `Path` to a directory to write the site. if unspecified defaults to creating relative to the script in `/docs/
#' @param image_url a 'str' with a link to the hosted image URL for the background
def render_atlas_site(world: World, output: Path = None, image_url: str = CONFIG.image_url): 
    render_atlas_html(world, output, image_url)
    render_atlas_css(output)
    render_atlas_js(output)
