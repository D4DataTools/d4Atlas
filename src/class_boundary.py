from dataclasses import dataclass

@dataclass 
class Boundary: 
    title: str
    points: list[tuple[float, float]]

def load_boundary(boundary: Boundary) -> Boundary:
    

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
