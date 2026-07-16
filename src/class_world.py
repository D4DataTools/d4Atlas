
from dataclasses import dataclass, field

from class_boundary import Boundary


@dataclass
class World: 
    name: str
    world_data: dict
    region_boundaries: Boundary


    markers: list = field(default_factory=list)

    subzones: dict = field(default_factory=dict)

def load_world(name: str) -> World:
    world_data = load_data('World', name)

    world = World(
        name=name,
        world_data=world_data,
    )

    load_region_boundaries(world)
    load_global_markers(world)
    load_subzone_markers(world)

    return world
