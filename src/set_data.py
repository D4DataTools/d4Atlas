import json
from global_values import VERBOSE

# In JS these are all frozen. 
# I'm wondering if we can build this to be more scalable rather than hardcoded lists

ACTOR_TYPE_ENUM = {
  "Invalid": 0,
  "Monster": 1,
  "Gizmo": 2,
  "Client Effect": 3,
  "Server Prop": 4,
  "Environment": 5,
  "Critter": 6,
  "Player": 7,
  "Item": 8,
  "Axe Symbol": 9,
  "Projectile": 10,
  "Custom Brain": 11,
  "Foliage": 12,
  "Minimap Secret": 13,
  "Mount": 14,
  "ACTORTYPE_COUNT": 15,  
}

ACTOR_TYPE_ENUM_LABELS = {v: k for k, v in ACTOR_TYPE_ENUM.items()}

GIZMO_TYPE_ENUM = {
  "Door": 0,
  "Chest": 1,
  "Portal": 2,
  "Waypoint": 4,
  "Checkpoint": 7,
  "Shrine": 11,
  "Headstone": 18,
  "Event Reward Chest": 19,
  "Portal Destination": 20,
  "Breakable Container": 23,
  "Hidden Cache": 24,
  "Shared Stash": 25,
  "Spawner": 28,
  "POI Camera": 29,
  "Traversal": 30,
  "Trigger": 44,
  "Destroyable Object": 48,
  "Switch": 57,
  "Destroy Self When Near": 60,
  "Return Town Portal": 85,
  "Graveyard": 86,
  "Boss Door": 87,
  "PVP Chest": 88,
  "PVP Obelisk": 89,
  "Breakable Container Arrangement": 91,
  "Destroyable Arrangement": 92,
  "Necro Corpse": 93,
  "Carryable": 94,
  "Carryable Receptacle": 95,
  "Chargeable": 96,
  "DEPRECATED__DO_NOT_USE": 97,
  "Sign": 98,
  "Tracked Checkpoint": 99,
  "Quest Switch": 100,
  "Wardrobe": 101,
  "Paragon Glyph Upgrade": 102,
  "World Tier Select": 103,
  "Mount Summon Post": 104,
  "Quest Chest": 105,
  "Unique Operator Chest": 106,
  "Chair": 107,
  "Party Member Portal": 108,
  "Participant Timer": 109,
  "Recipe Event": 110,
  "Event Select Portal": 112,
  "Raid Banner": 113,
  "Armory": 114
}

GIZMO_TYPE_ENUM_LABELS = {v: k for k, v in GIZMO_TYPE_ENUM.items()}
