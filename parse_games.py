from collections import defaultdict
import itertools
import os

collection = os.path.dirname(os.path.realpath(__file__))
dirof_game_collection = collection + "/" + "game_collection.txt"
with open(dirof_game_collection, "r") as f:
    game_list = f.read().splitlines()


game_collection = defaultdict(list)
reach_system = False

# exclude keyword in searches
# gameList = ["Super Mario 64 -(DS, kart)", "Donkey Kong 64"]
for game in game_list:
    # After we parse system line, then we add system combinations
    game_split = game.split("-")
    if game == "[System]":
        reach_system = True
    elif reach_system:
        game_collection[game_split[0].strip()].append(
            game.strip() + " System" + " vga -(50, 55, 60, 65, 70, 75, 80)"
        )

        game_collection[game_split[0].strip()].append(
            game.strip()
            + " System"
            + " wata -(3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5)"
        )
    else:
        game_collection[game_split[0].strip()].append(
            game.strip()
            + " wata -(3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5)"
        )
        game_collection[game_split[0].strip()].append(
            game.strip() + " vga -(50, 55, 60, 65, 70, 75, 80)"
        )
# Strips should be good

# Game, itemURL, title, itemId in another file
# System with or without system

# Make chose number of combinations of each game and append to full list
# Change range based on number of combinations
# numCombinations = 1  ###################
# for index, subset in zip(
#         range(numCombinations), itertools.permutations(gameSplit, len(gameSplit))
#     ):
