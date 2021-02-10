import json
import os
import time
import random

def main():
    #Filtering out the files that can be used as games (json) 
    json_games = []
    for file in os.listdir():
        if ".json" in file:
            json_games.append(file)
    
    #Allowing the player to pick which game they want to play
    #Just displays the json file and not the title of the game 
    print("Which game would you like to play?")
    for i, x in enumerate(json_games):
        print(str(i+1) + ". " + x)
    
    #Picking and running the game they selected 
    selected = int(input("Please enter a number. "))
    for i, x in enumerate(json_games):
        if i == (selected - 1):
            with open(json_games[i]) as fp:
                game = json.load(fp)
    print()
    
    #Making sure that all the exits in the selected game are valid 
    check_exits(game)
    
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
 
    play(game)




def check_exits(game):
    """
    Make sure that each exit in every room points to an exisiting room. 
    
    INPUTS:
    game - file being used for the game
    
    RETURNS: Nothing; will crash if an exit leads to a non-existent room
    """
    rooms = find_non_win_rooms(game) #list of the rooms 
    for room in rooms:
        # Checking each exit in the list of exits for each room 
        for e in ((game[room])['exits']):
            assert(e['destination'] in game) 


def play(rooms):
    # Going to keep track of the duration of the game 
    start_time = time.monotonic()
    
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start'] 
    
    # The things the player has collected.
    stuff = ['Cell Phone; no signal or battery...']
    visited = {}
    
    # Creating and randomly placing a cat
    cat_rooms = find_non_win_rooms(rooms)
    
    cat_place = random.choice(cat_rooms)
    ((rooms[cat_place])["items"]).append("Fish")

    while True:
        print()
        print()
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        
        # Print the description.
        print(here["description"])

        
        # Check and keep track of the rooms visited 
        if current_place in visited:
            print("... You've been in this room before.")
        visited[current_place] = True
        
# CAT ------------------------------------------------------------ 
        
        # Check if you're in the same room as the cat 
        if cat_place == here['name']:
            print("... and oh a cat is here. Weird.")
            # Do not know how to make it stay in one place throughout the loop
            if ("Fish" in stuff):
                print("The cat purrs. You have something it wants...")
            
        else: 
            # Changing the cat's location
            cat_exits = [] # Holds potential options for the cat's new place 
            # Going through each exit in the cat's current location 
            for d in ((rooms[cat_place])['exits']):
                # Adding potential destinations to the cat's exit
                # Going through each key in the exit
                for key in d:
                    # Want to make sure that the cat doesn't leave the game
                    if (key == 'destination') and (d['destination'] in cat_rooms):
                        cat_exits.append(d['destination'])
            # Cat will randomly choice an exit if there are options
            # Prevents the program from crashing if there are no viable exits 
            if len(cat_exits) > 0: 
                cat_place = random.choice(cat_exits)
            
            
            
#ITEMS IN ROOM ---------------------------------------------------
        # Listing items in the room (if there are any) 
        if len(here['items']) > 0: #goes to the room entry, checks if it's item list has something
            print()
            print("Oh look, you found ...")
            for i in here['items']: #should print all the keys in the list
                print("-", i)
            print("Type 'take' to grab these items.")
            print()
            

# CHECKING IF GAME IS OVER AND CHANGING ROOMS ---------------------
        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here, stuff)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        
        
# HELP --------------------------------------------------------------  
        # Print the instructions again 
        if action in ["help", "h"]:
            print()
            print("You asked for help. Here are the instructions.")
            print()
            print_instructions()
            continue
        
# STUFF -------------------------------------------------------------
        # Print the user's items 
        if action in ["stuff", "items", "things"]:
            print()
            if len(stuff) > 0:
                print("Here are the items you have...")
                for s in stuff:
                    print("-", s)
            else:
                print("You have nothing. :( ")
            continue

# TAKE --------------------------------------------------------------
        # Take the items in the room and put them in the player's

        if action in ["take", "grab", "t", "g"]:
            print()
            for i, x in enumerate(here['items']):
                if x not in stuff: # don't want to make duplicates
                    stuff.append(x) # want to add all the items to your stuff
                elif x in stuff:
                    print("You already have", i)
            here['items'] = [] # empty bc you're taking all the items in the room
            print("Type 'stuff' to see what you know have.")
            continue
        
# DROP --------------------------------------------------------------
        # Let's the user drop a specific item to their current location 
        if action in ["drop", "d"]:
            print()
            if len(stuff) > 0:
                print("Here are the items you have...")
                print()
                for i, x in enumerate(stuff):
                    print(str(i + 1) + ". " + str (x))
                print()
                dropped = int(input("Please enter the number item you would like to drop. "))
                for i, x in enumerate(stuff):
                    if (i + 1) == dropped:
                        here['items'].append(stuff.pop(i))
            else:
                print("You have no items to drop. :( ")
            print()
            continue
        
# SEARCH -------------------------------------------------------------
        # Make any hidden exits visible and selectable 
        if action in ["search", "find"]:
            print()
            print("All visable and hidden exits in this room have been added to the exits options.")
            for e in here['exits']:
                if (e.get('hidden', False) == True): # Use get bc not every room has hidden
                    e['hidden'] = False
            continue
        
        
# HANDLING RESPONSES --------------------------------------------------
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]

            # Only works on rooms with only 1 required keys
            if selected.get('required_key', False) == False:
                current_place = selected['destination']
            elif selected['required_key'] in stuff:
                    current_place = selected['destination']
            elif selected['required_key'] not in stuff:
                print()
                print("You try, but it's locked!")
                continue
                
            print("...")
            
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")
    
# TIME ------------------------------------------------------------------
    # Grabbed the start time in the beginning of this function 
    end_time = time.monotonic()
    total_time = end_time - start_time
    print("Duration of Game: ", str(int(total_time//60)), "mins", int(total_time%60), "secs")
    
    
def find_usable_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of all exits that are visible (not hidden) 
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        usable.append(exit)
    return usable


def find_non_win_rooms(game):
    """
    Create a list of all the rooms that do not end the game in a game
    
    INPUTS
    game - file of the game currently being played 
    
    RETURNS: List of all the rooms that do not end the game
    
    SOURCE: https://gist.github.com/jjfiv/3c06190fb569f547ea9d700d19635f40
            (by Professor Foley) 
    """
    keep = []
    for room_name in game.keys():
        # skip if it is the "fake" metadata room that has title & start
        if room_name == '__metadata__':
            continue
        # skip if it ends the game
        if game[room_name].get('ends_game', False):
            continue
        # keep everything else:
        keep.append(room_name)
    return keep


def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'drop' to drop an item in a room.") 
    print(" - Type 'search' to take a deeper look at a room.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'help' to view these instructions later.") 
    print("=== Instructions ===")
    print("")
    
if __name__ == '__main__':
    main()