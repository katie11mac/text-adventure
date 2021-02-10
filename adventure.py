import json

# This global dictionary stores the name of the room as the key and the dictionary describing the room as the value.
GAME = {
    '__metadata__': {
        'title': 'Adventure',
        'start': 'kitchen'
    }
}

def create_room(name, description, ends_game=False):
    """
    Create a dictionary that represents a room in our game.

    INPUTS:
     name: string used to identify the room; think of this as a variable name.
     description: string used to describe the room to the user.
     ends_game: boolean, True if arriving in this room ends the game.
    
    RETURNS:
     the dictionary describing the room; also adds it to GAME!
    """
    assert (name not in GAME)
    room = {
        'name': name,
        'description': description,
        'exits': [],
        'items': [],
    }
    # Does this end the game?
    if ends_game:
        room['ends_game'] = ends_game

    # Stick it into our big dictionary of all the rooms.
    GAME[name] = room
    return room

def create_exit(source, destination, description, required_key=None, hidden=False):
    """
    Rooms are useless if you can't get to them! This function connects source to destination (in one direction only.)

    INPUTS:
     source: which room to put this exit into (or its name)
     destination: where this exit goes (or its name)
     description: how to show this exit to the user (ex: "There is a red door.")
     required_key (optional): string of an item that is needed to open/reveal this door.
     hidden (optional): set this to True if you want this exit to be hidden initially; until the user types 'search' in the source room.
    """
    # Make sure source is our room!
    if isinstance(source, str):
        source = GAME[source]
    # Make sure destination is a room-name!
    if isinstance(destination, dict):
        destination = destination['name']
    # Create the "exit":
    exit = {
        'destination': destination,
        'description': description
    }
    # Is it locked?
    if required_key:
        exit['required_key'] = required_key
    # Do we need to search for this?
    if hidden:
        exit['hidden'] = hidden
    source['exits'].append(exit)
    return exit
        


kitchen = create_room("kitchen", "You're in a kitchen. It smells a little off...")
kitchen["items"].append("key") 
create_exit(kitchen, "hallway", "A door leads into the hall.")
create_exit(kitchen, "locked_door", "You turn around and see that the door is wide open...", hidden = True)
create_exit(kitchen, "dishwasher", "There is something leaking through this doorway...")

locked_door = create_room("locked_door", "You're at another door.")
create_exit(locked_door, kitchen, "Let's go back to the kitchen.")
create_exit(locked_door, 'outside', "Door with a card scanner on the wall next to it.", required_key = "ID card")

hallway = create_room("hallway", "Hmm... where to go... ")
create_exit(hallway, kitchen, "Go back into the kitchen.")
create_exit(hallway, 'staircase', "A door with the words STAIRS was covered by all these boxes.", hidden = True, required_key = "knife")
create_exit(hallway, 'freezer', "Bright silver door labeled FREEZER.", required_key = "key")
create_exit(hallway, "dishwasher", "There is something leaking under this door...") 

freezer = create_room("freezer", "You hope the door doesn't close ... It's really cold in there.")
freezer["items"].append("ice cream")
freezer["items"].append("ID card")
create_exit(freezer, 'hallway', "Go back into the hallway.")

dishwasher = create_room("dishwasher", "This place is a mess. You hope you just stepped in water...")
dishwasher["items"].append("spatual")
dishwasher["items"].append("knife") 
create_exit(dishwasher, hallway, "Let's go back into the hallway.")
create_exit(dishwasher, kitchen, "Let's go back to where we started: the kitchen.") 

staircase = create_room("staircase", "Just looking at these stairs makes you out of breath.")
create_exit(staircase, hallway, "Nevermind; go back to the hallway.")
create_exit(staircase, "pickup", "Pick up area for food.", required_key = "ID card")
create_exit(staircase, "market", "Mini market where fresh produce was sold.") 

market = create_room("market", "Someone really messed up this place... There is stuff everywhere...")
market["items"].append("cash")
market["items"].append("old food") 
create_exit(market, staircase, "Let's go back to that stairway.")
create_exit(market, "outside", "Oh a door. Maybe we can leave?", required_key = "ID card")

pickup = create_room("pickup", "There sure are a lot of boxes out here...")
create_exit(pickup, staircase, "Go back to the stairs")
create_exit(pickup, 'outside', """Oh my... is that light?! The garage for pickup is slightly cracked open...
You're going to find a way to make the gap wider if you want to get out... """, required_key = "spatual")

outside = create_room("outside", "You've escaped! HEHEHE", ends_game=True)


##
# Save our text-adventure to a file:
##
with open('adventure.json', 'w') as out:
    json.dump(GAME, out, indent=2)
