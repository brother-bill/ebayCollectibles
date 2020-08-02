import pickle

from e_collector import Item
from collections import defaultdict


#75 VGA to Wata 90
#80 VGA to Wata 92
#85-90 or 9.4-9.6 and under is store bought
#85 to 9.4
#90 to 9.6
#95 to 9.8
#100 to 10.0
#wata over vga
#certified link and heritage auctions instead of ebay, ebay good for buying
#distributor channels
#circulars shopping nintendo games
curr = "items/new_items.pkl"
whole = "items/items.pkl"
with open(whole, "rb") as items_file:
    # full_list = defaultdict(set)
    # pickle.dump(full_list, items_file, -1)
    full_list = pickle.load(items_file)

# print(full_list["Pokemon Emerald"]) gives items
for z in full_list:
    # print(len(full_list[z]))
    #print(z)
    for item in full_list[z]:

        if item.game_name == "Super Mario 64":
            print(item.title)
            # print(item.item_url)
# any() function short-circuits and returns True as soon as a match has been found.
# if not any(x.item_id == i.item_id for x in itemList)

# for item in read_items('item_objects.pkl'):
#     for i in item:
#         print('  name: {}, value: {}'.format(i.site, i.title))

# write to new file new listings to parse
# for z in new_listings:
#   print("New Listing: " + str(z))

# item no results doesnt get anything in list

