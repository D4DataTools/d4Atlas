from d4atlas.data.loader import load_strings


def get_boundries_for_static_camp(camp): 
    if camp.get('__type__') != 'TerritoryRegionBoundary': return None 
    sno_territory = camp.get('snoTerritory')
    if not sno_territory: return None 

    strings = load_strings(sno_territory)
    points = format_ar_points(camp.get('arPoints', []))

    return (
        f'<path class="subzone-border" '
        f'd="M {points} z">'
        f'<title>{strings.get("Name", "")}</title></path>'
    )

def format_ar_points(ar_points):
    return ' L '.join( p for point in ar_points if (p := format_ar_point(point)))

def format_ar_point(point):
    x = point.get('x')
    y = point.get('y')
    if x is None or y is None: return None
    return(f'{x} {y}')