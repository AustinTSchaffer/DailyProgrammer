#%%

from ticket_info import station_info, my_ticket, nearby_tickets

def ticket_property_valid_for_station_property(ticket_prop, station_prop):
    return (
        (station_prop[0][0] <= ticket_prop <= station_prop[0][1]) or
        (station_prop[1][0] <= ticket_prop <= station_prop[1][1])
    )

#%% Part 1

good_tickets = []
bad_properties = []
for ticket in nearby_tickets:
    invalid_property = next(
        (
            ticket_property
            for ticket_property in ticket
            if not any(
                True
                for station_property in station_info.values()
                if ticket_property_valid_for_station_property(ticket_property, station_property)
            )
            for station_property in station_info.values()
        ),
        None
    )

    if invalid_property is not None:
        bad_properties.append(invalid_property)
    else:
        good_tickets.append(ticket)

print("Part 1:", sum(bad_properties))

# %% Part 2

# Generate a list of sets, mapping ticket indexes to all station info properties.
ticket_property_map = [set(station_info.keys())] * len(my_ticket)

# Filter the "ticket_property_map" by removing station properties from each index if there are any tickets
# that . This is performed using set intersections.
for ticket in good_tickets + [my_ticket]:
    for ticket_prop_index, ticket_property in enumerate(ticket):
        station_info_key_set = ticket_property_map[ticket_prop_index]

        ticket_property_valid_for_keys = [
            station_info_key for station_info_key in station_info_key_set
            if ticket_property_valid_for_station_property(ticket_property, station_info[station_info_key])
        ]

        ticket_property_map[ticket_prop_index] = station_info_key_set.intersection(ticket_property_valid_for_keys)

# Any entries in "ticket_property_map" that have only one station property remaining, that station property
# must be correct for that index and should be removed from all other indexes.
changes_made = True
while changes_made and any(entry for entry in ticket_property_map if len(entry) > 1):
    changes_made = False
    for index, entry in enumerate(ticket_property_map):
        if len(entry) == 1:
            for _index, _entry in enumerate(ticket_property_map):
                if _index != index:
                    ticket_property_map[_index] = _entry.difference(entry)
                    changes_made |= (len(_entry) != len(ticket_property_map[_index]))

# Reverse the map, asserting that all ticket properties map to exactly one station property.
reverse_property_map = {}
for index, entry in enumerate(ticket_property_map):
    assert len(entry) == 1
    reverse_property_map[next(iter(entry))] = index

# Calculations for part 2
part_2 = 1
for property_, index in reverse_property_map.items():
    if property_.startswith("departure"):
        part_2 *= my_ticket[index]

print("Part 2:", part_2)

# %%
