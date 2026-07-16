from d4atlas.geometry import translate
from d4atlas.enums import *
from d4atlas.data.loader import load_data


# process_maker_set written for a class: world compatability
def _process_maker_set(world, marker_set, offset = None):
    if offset is None: offset = {"x": 0, "y": 0, "z": 0}

    marker_set_key = (
        f"{marker_set['__snoID__']}|"
        f"{offset['x']}|{offset['y']}|{offset['z']}"
    )

    if marker_set_key in world.processed_marker_sets: return
    world.processed_marker_sets.add(marker_set_key)
    if not isinstance(marker_set.get('tMarkerSet'), list): return

    for marker in marker_set.get('tMarkerSet'):
        _process_marker(world, marker, offset)

# rocess_marker written for class: world compatability 
def _process_marker(world, marker, offset ):
    if marker.get("__type__") != "Marker": return None
    sno_reference = marker["snoname"]
    if sno_reference is None: return None


    # if a marker has a 'name' it is either a nested marker, a sybol, or an actor
    if sno_reference.get("name"):
        # Nested MarkerSet
        if sno_reference["groupName"] == "MarkerSet":
            new_marker_set = load_data(sno_reference.get('groupName'), sno_reference.get('name'))
            _process_marker(world, new_marker_set, translate(marker["transform"]["wp"], offset) )
            return None

        # Encounter -> Symbol
        if sno_reference["groupName"] == "Encounter":
            encounter = load_data(sno_reference.get('groupName'), sno_reference.get('name'))
            if encounter.get("snoSymbol", {}).get("name"): sno_reference = encounter["snoSymbol"]

        # Early Exit if not an actor 
        if sno_reference["groupName"] != "Actor": return None
        if _process_marker_actor(world, marker, offset): return True

    elif any(
        base.get("__type__") == "MarkerSpawnLocData"
        for base in marker.get("ptBase", [])
    ): 
     if _process_marker_spawn(world, marker, offset): return True

# process_marker_actor for class: world compatability 

def _process_marker_actor(world, marker, offset): 
    sno_reference = marker.get('snoname')
    e_actor_type = None
    e_gizmo_type = None

    for base_data in marker.get("ptBase", []):

        if base_data.get("__type__") == "MarkerActorData":
            e_actor_type = base_data.get("eActorType")
            e_gizmo_type = base_data.get("eGizmoType")
            break

    actor = load_data(sno_reference.get('groupName'), sno_reference.get('name'))

    if e_actor_type is None:
        e_actor_type = actor.get("eType")
        e_gizmo_type = actor.get("eActorGizmoType")

    if e_actor_type not in ACTOR_TYPE_ENUM.values(): return None
    if (e_actor_type == ACTOR_TYPE_ENUM["Gizmo"] and e_gizmo_type not in GIZMO_TYPE_ENUM.values()): return None

    strings = load_data(sno_reference.get('groupName'), sno_reference.get('name'))
    adjusted = translate(marker["transform"]["wp"], offset)

    tooltip = make_tool_tip(strings, sno_reference, e_actor_type, e_gizmo_type, adjusted)

    key = "|".join([
        "actor",
        str(e_actor_type),
        str(e_gizmo_type),
        str(adjusted["x"]),
        str(adjusted["y"])
    ])

    search_text = " ".join(filter(None, [
        "actor",
        ACTOR_TYPE_ENUM_LABELS.get(e_actor_type),
        GIZMO_TYPE_ENUM_LABELS.get(e_gizmo_type),
        strings.get("Name"),
        sno_reference.get("name")
    ]))

    css = (
        f"searchable actor "
        f"actor-type-{e_actor_type} "
        f"gizmo-type-{e_gizmo_type}"
    )

    if sno_reference.get("name"):
        css += (
            " sno-name-" + sno_reference["name"].replace(" ", "-").replace("_", "-")
        )

    world.markers[key] = make_marker_generic(
        search_text, 
        css, e_actor_type,
        e_gizmo_type,
        adjusted,
        tooltip
    )

    return True

# process_marker_spawn for class: world compatability 

def _process_marker_spawn(world, marker, offset): 
    sno_reference = marker["snoname"]
    spawn_type = None

    for base in marker["ptBase"]:
        if base.get("__type__") == "MarkerSpawnLocData":
            spawn_type = (base["gbidSpawnLocType"]["name"])
            break

        adjusted = translate( marker["transform"]["wp"], offset )

        tooltip = "\n".join(filter(None, [
            (
                f"gbidSpawnLocType: {spawn_type}"
                if spawn_type else None
            ),
            (
                f"Coordinates: "
                f"{adjusted['x']}, {adjusted['y']}"
            )
        ]))

        key = "|".join([
            "spawn",
            str(spawn_type),
            str(adjusted["x"]),
            str(adjusted["y"])
        ])

        class_css = (
            f'searchable spawn '
            f'pawn-type-{spawn_type}'
        )

        world.markers[key] = make_marker_generic(
            f'{spawn_type or ""}',
            class_css,
            None,
            None, 
            adjusted, 
            tooltip
        )




def make_marker_generic(
    search_text,
    class_css,
    e_actor_type = None, 
    e_gizmo_type = None, 
    adjusted = None, 
    tooltip = None
):
    return (
        f'<path '
        f'data-search-text="{search_text}" '
        f'class="{class_css}"'
        f'data-actor-type="{e_actor_type or ""}" '
        f'data-gizmo-type="{e_gizmo_type or ""}" '
        f'vector-effect="non-scaling-stroke" '
        f'stroke-linecap="round" '
        f'd="M {adjusted["x"]} {adjusted["y"]} l 0.0001 0">'
        f'<title>{tooltip}</title>'
        f'</path>'
    )

def make_tool_tip(strings, sno_reference, e_actor_type, e_gizmo_type, adjusted): 
    lines = []

    if strings.get("Name"): lines.append(f"Name: {strings['Name']}")
    if sno_reference.get("groupName"): lines.append( f"SNO Group: {sno_reference['groupName']}" )
    if sno_reference.get("name"): lines.append( f"SNO Name: {sno_reference['name']}" )
    if e_actor_type is not None: lines.append(f"eActorType: {e_actor_type}")
    if e_gizmo_type is not None: lines.append(f"eGizmoType: {e_gizmo_type}")

    lines.append( f"Coordinates: {adjusted['x']}, {adjusted['y']}" )

    return "\n".join(lines)