def process_marker_set(marker_set, offset=None):
    global markers, processed_marker_set

    if offset is None: offset = {"x": 0, "y": 0, "z": 0}

    marker_set_key = (
        f"{marker_set['__snoID__']}|"
        f"{offset['x']}|{offset['y']}|{offset['z']}"
    )

    if marker_set_key in processed_marker_set:
        return

    processed_marker_set[marker_set_key] = True

    if not isinstance(marker_set.get("tMarkerSet"), list): return

    for marker in marker_set["tMarkerSet"]:

        if process_marker(marker): continue

def process_marker_actor(marker): 
    # Early Exit if not an actor 
    if sno_reference["groupName"] != "Actor": return None

    e_actor_type = None
    e_gizmo_type = None

    for base_data in marker.get("ptBase", []):

        if base_data.get("__type__") == "MarkerActorData":
            e_actor_type = base_data.get("eActorType")
            e_gizmo_type = base_data.get("eGizmoType")
            break

    actor = load_data(sno_reference)

    if e_actor_type is None:
            e_actor_type = actor.get("eType")
            e_gizmo_type = actor.get("eActorGizmoType")

    if e_actor_type not in ActorTypeEnum.values(): return None
    if (e_actor_type == ActorTypeEnum["Gizmo"] and e_gizmo_type not in GizmoTypeEnum.values()): return None

    strings = load_strings(sno_reference)
    adjusted = translate(marker["transform"]["wp"], offset)
    tooltip = make_tool_tip(strings, sno_reference, e_actor_type, e_gizmo_type)

    key = "|".join([
        "actor",
        str(e_actor_type),
        str(e_gizmo_type),
        str(adjusted["x"]),
        str(adjusted["y"])
    ])

    search_text = " ".join(filter(None, [
        "actor",
        ActorTypeEnumLabels.get(e_actor_type),
        GizmoTypeEnumLabels.get(e_gizmo_type),
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

    markers[key] = make_marker_generic(search_text, css, e_actor_type, e_gizmo_type, adjusted, tooltip)
    return True

def process_marker_spawn(marker): 
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

        markers[key] = make_marker_generic(f'{spawn_type or ""}', class_css, None, None, adjusted, tooltip)

def process_marker(marker): 
    if marker.get("__type__") != "Marker": return None
    sno_reference = marker["snoname"]

    # Normal actor markers
    if sno_reference.get("name"):
        # Nested MarkerSet
        if sno_reference["groupName"] == "MarkerSet":
        new_marker_set = load_data(sno_reference)
        process_marker_set( new_marker_set, translate(marker["transform"]["wp"], offset) )
        return None

        # Encounter -> Symbol
        if sno_reference["groupName"] == "Encounter":
            encounter = load_data(sno_reference)
            if encounter.get("snoSymbol", {}).get("name"): sno_reference = encounter["snoSymbol"]

        # Early Exit if not an actor 
        if sno_reference["groupName"] != "Actor": return None
        if process_marker_actor(marker): return True

    elif any(
        base.get("__type__") == "MarkerSpawnLocData"
        for base in marker.get("ptBase", [])
    ): 
        process_marker_spawn(marker)


        

        

         


def make_marker_generic(
    search_text,
    class_css,
    e_actor_type = None, 
    e_gizmo_type = None, 
    adjusted, 
    tooltip
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

def make_tool_tip(strings, sno_reference, e_actor_type, e_gizmo_type): 
    lines = []

    if strings.get("Name"): lines.append(f"Name: {strings['Name']}")
    if sno_reference.get("groupName"): lines.append( f"SNO Group: {sno_reference['groupName']}" )
    if sno_reference.get("name"): lines.append( f"SNO Name: {sno_reference['name']}" )
    if e_actor_type is not None: lines.append(f"eActorType: {e_actor_type}")
    if e_gizmo_type is not None: lines.append(f"eGizmoType: {e_gizmo_type}")

    lines.append( f"Coordinates: {adjusted['x']}, {adjusted['y']}" )

    return "\n".join(lines)
