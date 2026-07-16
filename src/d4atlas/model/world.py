from d4atlas.processing.markers import _process_maker_set
from d4atlas.processing.boundries import get_boundries_for_static_camp
from d4atlas.data.loader import load_data, load_strings, load_json
from d4atlas.config import CONFIG

#' @title Word as a Class
#' @name: world_class
#' @description A collection of data and methods that help with mapping the world
class World:
    # Intitalize the class
    def __init__(self, name):
        if CONFIG.verbose: print(f'- Intializing `{name}`.')
        self.name = name
        # Raw d4Data JSON
        self.data = {}
        self.markers = {}
        self.region_boundaries = []
        # Prevent recursive marker set loops
        self.processed_marker_sets = set()

    @property
    def zone_art(self): 
        params = self.data.get('tZoneMapParams')
        center = params.get('vecZoneArtCenter')
        scale = params.get('flZoneArtScale')
        grid_size = self.data.get('flGridSize')

        return {
            "x": -1 * center.get('x') / scale,
            "y": -1 * center.get('y') / scale,
            "w": params.get('nGridSystemZoneMapFieldWidth') * grid_size, 
            "h": params.get('nGridSystemZoneMapFieldHeight') * grid_size
        }    

    #' @name = world_class
    #' @param cls Class
    #' @param name A `str` with the name of the world from D4Data
    #' @examples
    #' # Load A world 
    #' d4atlas.World.Load('Sanctuary_Eastern_Continent')
    #' @return an object of type `World`
    @classmethod
    def load(cls, name):
        if CONFIG.verbose: print(f'Loading the world `{name}`...')
        world = cls(name)

        if CONFIG.verbose: print(f'- Setting `World.data` for `{name}`.')
        world.data = load_data("World", name)

        # Set Boundries
        if CONFIG.verbose: print(f'- Setting `World.region_boundries` `{name}`.')
        world.process_region_boundaries()

        #Set markers
        if CONFIG.verbose: print(f'- Setting `World.markers` `{name}`.')
        world.process_global_markers()
        world.process_world_server_data()

        return world

    #' @name = world_class
    #' @param self requires an object of type `World` with a non empty `self.data` and `self.name`
    #' @retrun None
    #' @details Updates `self.region_boundaries` using `self.data`
    def process_region_boundaries(self):
        if CONFIG.verbose: print(f'  - Processing Region Boundries.')
        # null list skips the loop but silenetly fails. 
        # Not sure if I want it to be explicit / warn when it fails
        for camp in self.data.get("arRegionBoundaries", []):
            boundary = get_boundries_for_static_camp(camp)
            if boundary: self.region_boundaries.append(boundary)

    #' @name = world_class
    #' @param self requires an object of type `World` with a non empty `self.data` and `self.name`
    #' @retrun None
    #' @details Updates `self.markers` using `self.data` with global markers.
    def process_global_markers(self):
        if CONFIG.verbose: print(f'  - Processing global_markers for {self.name}')
        get_global_marker_sets(self)
    
    #' @name = world_class
    #' @param self requires an object of type `World` with a non empty `self.data` and `self.name`
    #' @retrun None
    #' @details Updates `self.markers` using `self.data` with server markers.
    def process_world_server_data(self):
        if CONFIG.verbose: print(f'  - Processing world server data for {self.name}')
        for world_server_entry in self.data.get('ptServerData', []):
            self.process_world_server_entry(world_server_entry)

    def process_world_server_entry(self, world_server_entry):
        for scene_chunk in world_server_entry.get('ptSceneChunks', []): 
            self.process_scene_chunk(scene_chunk)

    def process_scene_chunk(self, scene_chunk): 
        scene_spec = scene_chunk.get('tSceneSpec')
        if not scene_spec: return
        
        for subzone_relation in scene_spec.get('arSubzones', []): 
            self.process_scene_subzone_relation(subzone_relation)

    def process_scene_subzone_relation(self, subzone_relation): 
        subzone_ref = subzone_relation.get('snoSubzone')
        if not subzone_ref: return
        subzone = load_data(subzone_ref.get('groupName'), subzone_ref.get('name'))
        self.process_scene_subzone(subzone)

    def process_scene_subzone(self, subzone):
        for world_marker_set in subzone.get('arWorldMarkerSets', []):
            self.process_world_marker_set(world_marker_set)

    def process_world_marker_set(self, world_marker_set):
        sno_marker_set = world_marker_set.get('snoMarkerSet')
        if sno_marker_set and sno_marker_set.get('groupName') == 'MarkerSet': 
            self._load_marker_set(sno_marker_set)

    def _load_marker_set(self, sno_marker_set):

        key = (
            sno_marker_set.get("groupName"),
            sno_marker_set.get("name")
        )

        if key in self.processed_marker_sets: return

        self.processed_marker_sets.add(key)

        marker_set = load_data(
            sno_marker_set.get("groupName"),
            sno_marker_set.get("name")
        )

        if not marker_set: return

        _process_maker_set(self, marker_set)

#' Get Global Marker Sets  from data_root
#' @param world an object of type `World`
#' @return None
#' @details Loads the global marker sets and loops through them.
#' Calling `extract_marker_sets()` for each entry loaded.
def get_global_marker_sets(world: World):
    if CONFIG.verbose: print(f'    - Loading global markers from file for {world.name}')
    global_markers = load_data('Global', 'global_markers')
    for entry in global_markers.get('ptContent', []):
        extract_marker_sets(world, entry) 

#' Extract the Global Marker Sets 
#' @param world an object of type `World`
#' @param global_marker_entry a `dict` from a Global Marker Set Entry
#' @return None
#' @details Loads the global marker sets entry and loops through the actors.
#' Calling `process_global_marker_actor()` for each actor.
def extract_marker_sets(world: World, global_marker_entry: dict): 
    if CONFIG.verbose: print('    - Extracting Actors from `arGlobalMarkerActors` in `global_marker_entry')
    global_marker_actors = global_marker_entry.get('arGlobalMarkerActors')
    if not isinstance(global_marker_actors, list): return
    for actor in global_marker_entry.get('arGlobalMarkerActors', []):
        process_global_marker_actor(world, actor)


#' Process the Global Marker Sets 
#' @param world an object of type `World`
#' @param actor a `dict` from a Global Marker Actors entry
#' @return None
#' @details Loads the global marker actor nd loops through the actors.
#' Must have a `snoWorld` or `snoSet`
#' Calling `_process_maker_set()` for the loaded marker.   
def process_global_marker_actor(world: World, actor):
    if CONFIG.verbose: print('    - Processing Actor Markers.')
    sno_world = actor.get('snoWorld')
    sno_world_name = sno_world.get('name')
    sno_marker_set = actor.get('snoMarkerSet')
    sno_marker_set_name = sno_marker_set.get('name')

    if not sno_world or not sno_marker_set: return
    if sno_world.get('name') != world.name: return

    if CONFIG.verbose: print(f'    - Loading Data for Markers group: {sno_marker_set.get("groupName")} name: {sno_marker_set_name}')
    marker_set = load_data(sno_marker_set.get('groupName'), sno_marker_set_name)

    _process_maker_set(world, marker_set)