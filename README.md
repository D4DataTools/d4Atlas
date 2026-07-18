# D4Atlas

Check out the results [here](https://d4datatools.github.io/d4Atlas/atlas.html).

## Purpose

This has mostly been a learning process to get more familiar with Python while learning more about a game that I enjoy. This tool hopefully will be useful to someone when doing detective work on the mysteries of Sactuary. 

## What's in the box

d4atlas provides a python package to build maps using data from [d4Data](https://github.com/DiabloTools/d4Data)

### Classes 

#### `World`

Provides a class and methods to generate a map of the world of Sanctuary in d4. Collects region boundaries, markers, and scaling details for rendering your own interactive Atlas.

Usage: 

```py 
import d4atlas
# Load the d4 map 
sanctuary = d4atlas.World.Load('Sanctuary_Eastern_Continent')
```

Automatically scale the markers and points with the property zone_art!

Usage: 

```py 
import d4atlas
# Load the d4 map 
sanctuary = d4atlas.World.Load('Sanctuary_Eastern_Continent')
# Load the d4 map 
print(sanctuary.zone_art)
# {'x': -5000, 'y': -5000, 'w': 5000, 'h': 5000}
```

### Functions 

#### `set_data_root`

d4atlas checks for a `.env` file and the environment variable `DATA_ROOT`. If not found it will prompt you to set your data root. This will data a path or a string pointing to a folder with data formatted like [d4Data](https://github.com/DiabloTools)/d4Data)

Usage: 

```py 
# Set the directory of d4 data
set_data_root('/home/user/documents/path/to/d4data')
```

### `render_atlas_site`

render your own local copy of the d4 interactive website. This function calls 3 sub functions that are also exposed for use to create the entire site's contents. If you only need to regenerate the HTML you can simply call `render_atlas_html` on it's own. Or call `render_atlas_css` and `render_atlas_js` to generate the CSS and JavaScript files independently.

#### Usage 

```py 
import d4atlas
# Set the directory of d4 data
set_data_root('/home/user/documents/path/to/d4data')

# Load the d4 map 
sanctuary = d4atlas.World.Load('Sanctuary_Eastern_Continent')

# Render the site
render_atlas_site(sanctuary, 'path/to/write')
```


## Acknowledgements 

Based of the work on the [d4Data Atlas](https://github.com/blizzhackers/d4data/blob/master/build_atlas.js) as well as the updates by [DiabloTools](https://github.com/DiabloTools) who have taken over the project from blizzhackers




