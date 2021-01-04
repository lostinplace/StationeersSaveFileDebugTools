from collections import namedtuple

AtmoFile = namedtuple('AtmoFile', 'atmo_by_thing_id atmo_by_position, atmo_by_network room_by_id room_by_position things')

RestoredAtmoData = namedtuple('RestoredAtmoData', 'Atmospheres Rooms')