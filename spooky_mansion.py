import json

# This global dictionary stores the name of the room as the key and the dictionary describing the room as the value.
GAME = {
    '__metadata__': {
        'title': 'Spooky Mansion',
        'start': 'entranceHall'
    }
}

def create_room(name, description, ends_game=False, first_time=None):
    assert (name not in GAME)
    room = {
        'name': name,
        'description': description,
        'exits': [],
        'items': []
    }
    # Is there a special message for the first visit?
    if first_time:
        exit['first_time'] = first_time
    # Does this end the game?
    if ends_game:
        room['ends_game'] = ends_game

    # Stick it into our big dictionary of all the rooms.
    GAME[name] = room
    return room

def create_exit(source, destination, description, required_key=None, hidden=False):
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

front_door_key = "Mansion Key"
    
entranceHall = create_room("entranceHall", """You are in the grand entrance hall of a large building.
How did you get here?""")
create_exit(entranceHall, "basement", "There are stairs leading down.")
create_exit(entranceHall, "attic", "There are stairs leading up.")
create_exit(entranceHall, "kitchen", "There is a red door.")
create_exit(entranceHall, "outside", "The front door.", required_key=front_door_key)

basement = create_room("basement", """You have found the basement of the mansion.
It is darker down here.
You get the sense a secret is nearby, but you only see the stairs you came from.""")
create_exit(basement, entranceHall, "There are stairs leading up.")
create_exit(basement, "secretRoom", "A trapdoor was hidden amongst the dust.", hidden=True)

attic = create_room("attic", """Something rustles in the rafters as you enter the attic. Creepy.
It's big and dark up here.""")
create_exit(attic, entranceHall, "There are stairs leading down.")
create_exit(attic, "attic2", "There is an archway.")

attic2 = create_room("attic2", """There's definitely a bat in here somewhere.
This part of the attic is brighter, so maybe you're safe here.""")
create_exit(attic2, attic, "There is an archway.")
create_exit(attic2, "balcony", "A small door rattles in the wind.")
create_exit(attic2, "dumbwaiter", "There is a dumbwaiter near the chimney.")

balcony = create_room("balcony", """There's a strange light here on the balcony.""")
balcony["items"].append(front_door_key)
create_exit(balcony, "aliens", "Step into the light.")
create_exit(balcony, "attic2", "Go back inside.")

create_room("aliens", """The aliens take you aboard their spaceship.
...
I guess you escaped.""", ends_game=True)

kitchen = create_room("kitchen", """You've found the kitchen. You smell moldy food and some kind of animal.""")
create_exit(kitchen, entranceHall, "There is a red door.")
create_exit(kitchen, "dumbwaiter", "There is a dumbwaiter.")

dumbwaiter = create_room("dumbwaiter", """You crawl into the dumbwaiter. What are you doing?""")
create_exit(dumbwaiter, attic2, "Exit at the top.")
create_exit(dumbwaiter, kitchen, "Exit on the first-floor.")
create_exit(dumbwaiter, "secretRoom", "Exit at the bottom.")

secretRoom = create_room("secretRoom", """You have found the secret room.
Who thought a green rug was a good idea?""")
create_exit(secretRoom, "hallway0", "A long hallway leads away.")
create_exit(secretRoom, basement, "You see a trapdoor with a spider crawling on it.")
create_exit(secretRoom, dumbwaiter, "Get back in the dumbwaiter.")

crypt = create_room("crypt", """You've found your way into a crypt. You smell dirt.""")
create_exit(crypt, "outside", "There are stairs leading up.")
outside = create_room("outside", """You step out into the night.

It smells like freedom.
""", ends_game=True)

hallway_length = 3
for i in range(hallway_length):
    here = "hallway{}".format(i)
    forward = "hallway{}".format(i+1)
    backward = "hallway{}".format(i-1)
    if i == 0:
        backward = "secretRoom"
    elif i == hallway_length - 1:
        forward = "crypt"
    create_room(here, """This is a very long hallway.""")
    create_exit(here, backward, """Go back.""")
    create_exit(here, forward, """Go forward.""")

##
# Save our text-adventure to a file:
##
with open('spooky_mansion.json', 'w') as out:
    json.dump(GAME, out, indent=2)

