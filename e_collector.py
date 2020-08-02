from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from collections import defaultdict
from os.path import exists
from pathlib import Path
from shutil import copy
import json
import itertools
import pickle
import os
import parse_games

site_list = [
    "EBAY-US",
    "EBAY-GB",
    "EBAY-AT",
    "EBAY-AU",
    "EBAY-CH",
    "EBAY-DE",
    "EBAY-ENCA",
    "EBAY-ES",
    "EBAY-FR",
    "EBAY-FRBE",
    "EBAY-FRCA",
    "EBAY-HK",
    "EBAY-IE",
    "EBAY-IN",
    "EBAY-IT",
    "EBAY-MOTOR",
    "EBAY-MY",
    "EBAY-NL",
    "EBAY-NLBE",
    "EBAY-PH",
    "EBAY-PL",
    "EBAY-SG",
]
# site_list = ["EBAY-PL", "EBAY-SG"]
# site_list = ["EBAY-US"]
# EBAY-US	     United States
# EBAY-AT	     Austria
# EBAY-AU	     Australia
# EBAY-CH	     Switzerland
# EBAY-DE        Germany
# EBAY-ENCA	     Canada (English)
# EBAY-ES	     Spain
# EBAY-FR	     France
# EBAY-FRBE	     Belgium (French)
# EBAY-FRCA	     Canada (French)
# EBAY-GB	     UK
# EBAY-HK	     Hong Kong
# EBAY-IE	     Ireland
# EBAY-IN	     India
# EBAY-IT	     Italy
# EBAY-MOTOR	 US Motors
# EBAY-MY	     Malaysia
# EBAY-NL	     Netherlands
# EBAY-NLBE	     Belgium (Dutch)
# EBAY-PH	     Philippines
# EBAY-PL	     Poland
# EBAY-SG		 Singapore


class Item:
    def __init__(
        self,
        condition,
        country,
        startTime,
        endTime,
        watchCount,
        location,
        returns,
        price,
        currency,
        sellingState,
        title,
        item_url,
        image_url,
        item_id,
        game_name,
        site,
    ):
        self.condition = condition
        self.country = country
        self.startTime = startTime
        self.endTime = endTime
        self.watchCount = watchCount
        self.location = location
        self.returns = returns
        self.price = price
        self.currency = currency
        self.sellingState = sellingState
        self.title = title
        self.item_url = item_url
        self.image_url = image_url
        self.item_id = item_id
        self.game_name = game_name
        self.site = site

    def __eq__(self, other):
        return self.item_id == other.item_id

    def __hash__(self):
        return hash(self.item_id)

    def items_file(self):
        attr = vars(self)
        return "".join("%s: %s\n" % item for item in attr.items())


# Search through all words, maybe paralell
# If item expired, then remove from item_results and append new
# display image of each item with clickable url and price
# list comprehension


# 1000 is New, 1500 is New Other, 3000 is Used

# For quotes within quote: \"     \"
# Other keywords gold near mint sealed factory sealed

# for idx, item in enumerate(logList):
#      print(idx + 1)
#      print(item)


def check_attributes(item):
    for attr in [
        "country",
        "location",
        "returnsAccepted",
        "title",
        "galleryURL",
    ]:
        if not hasattr(item, attr):
            setattr(item, attr, "N/A")
    for attr in ["startTime", "endTime", "watchCount"]:
        if not hasattr(item.listingInfo, attr):
            setattr(item.listingInfo, attr, "N/A")
    for attr in ["value", "_currencyId"]:
        if not hasattr(item.sellingStatus.currentPrice, attr):
            setattr(item.listingInfo, attr, "N/A")

    if not hasattr(item.sellingStatus, "sellingState"):
        setattr(item.listingInfo, "sellingState", "N/A")
    if not hasattr(item.condition, "conditionDisplayName"):
        setattr(item.condition, "conditionDisplayName", "N/A")


# A = {10, 20, 30, 40, 80}
# B = {100, 30, 80, 40, 60}
# print (A.difference(B))
# print (B.difference(A))
# {10, 20}
# {100, 60}
# every game has a set
# Change w to a


def main():
    # Get real path to file and then append new directory name
    fold_items = os.path.dirname(os.path.realpath(__file__)) + "/" + "items"
    new_logs = os.path.dirname(os.path.realpath(__file__)) + "/" + "logs"
    # Make new directory
    Path(fold_items).mkdir(parents=True, exist_ok=True)
    Path(new_logs).mkdir(parents=True, exist_ok=True)
    # Directory of pickle file
    dirof_item_results = fold_items + "/" + "items.pkl"
    dirof_new_items = fold_items + "/" + "new_items.pkl"
    dirof_history = new_logs + "/" + "history.txt"
    dirof_id = new_logs + "/" + "item_id.txt"
    dirof_log = new_logs + "/" + "log.txt"
    with open(dirof_id, "a+", encoding="utf-8") as ids_file, open(
        dirof_log, "w", encoding="utf-8"
    ) as log_file, open(dirof_history, "w", encoding="utf-8") as history_file:
        # Set file to search from beginning to add to set
        ids_file.seek(0)
        ids_set = set(line.strip() for line in ids_file)

        temp_ids_set = set(ids_set)  ############################
        request_counter = 0

        # If file of items to read exists, then open it and set the list to equal what's inside the file, also make a backup
        # Else create a new file and write a default dictionary of sets inside
        curr_results = defaultdict(set)
        item_results = defaultdict(set)
        if exists(dirof_item_results):
            with open(dirof_new_items, "wb") as new_items_file:
                pickle.dump(curr_results, new_items_file, -1)
            with open(dirof_item_results, "rb") as items_file:
                copy(dirof_item_results, fold_items + "/" + "items_copy.pkl")
                try:
                    print("PICKLE LOADED")
                    item_results = pickle.load(items_file)
                except EOFError:
                    print("PICKLE EMPTY")
                    log_file.write("PICKLE EMPTY")
                    item_results = defaultdict(set)
        else:
            with open(dirof_item_results, "wb") as items_file:
                print("PICKLE DOESNT EXIST")
                pickle.dump(item_results, items_file, -1)

        for site in site_list:
            history_file.write(
                "##################################     SERVER: "
                + str(site)
                + "     ##################################\n"
            )

            for game in parse_games.game_collection.items():
                game_name, keyword_combo = game
                history_file.write(
                    "##################################     GAME: "
                    + str(game_name)
                    + "     ##################################\n"
                )
                for keyword in keyword_combo:
                    # "paginationInput": {"pageNumber": "1"},
                    # "sortOrder": "Best Match"
                    # Best Match Default
                    # PricePlusShippingHighest Sorts items by the combined cost of the item price plus the shipping cost, with highest combined price items listed first.
                    # PricePlusShippingLowest Sorts items by the combined cost of the item price plus the shipping cost, with the lowest combined price items listed first.
                    # WatchCountDecreaseSort Sorts items by watch count in decreasing order for the given site
                    # EndTimeSoonest Sorts items by end time, with items ending soonest listed first.
                    try:
                        api_request = {
                            "keywords": keyword,
                            "itemFilter": [{"name": "Condition", "value": "1000"}],
                        }
                        api = Finding(
                            domain="svcs.ebay.com",
                            config_file="ebay.yaml",
                            https=True,
                            siteid=site,
                        )
                        response = api.execute("findItemsAdvanced", api_request)
                        request_counter += 1
                    except ConnectionError as e:
                        print(e)
                        print(e.response.dict())
                        log_file.write("CONNECTION ERROR: " + str(e) + "\n")
                        log_file.write(str(e.response.dict()) + "\n\n")
                        # response = {"reply":{"ack"}}
                        # response.reply.ack = "fail"
                    except AttributeError as e:
                        print(e)
                        log_file.write("ATTRIBUTE ERROR: " + str(e) + " for keyword \n")
                        log_file.write(
                            str(keyword) + "\n" + "Server: " + str(site) + "\n\n"
                        )
                    except Exception as e:
                        print(e)
                        print("WE SIMPLY BROKE")
                        log_file.write("WE SIMPLY BROKE: " + str(e) + "\n\n")
                    # x = json.dumps(response.dict(), sort_keys=True, indent=4)
                    else:
                        if (
                            response.reply.ack == "Success"
                            and response.reply.searchResult._count != "0"
                        ):
                            history_file.write(
                                "COUNT: "
                                + str(response.reply.searchResult._count)
                                + " for keyword: "
                                + str(keyword)
                                + "\n"
                            )
                            for item in response.reply.searchResult.item:
                                # if title contains 7.0, blah blah dont add
                                if not hasattr(item, "itemId"):
                                    setattr(item, "itemId", "N/A")
                                if not hasattr(item, "title"):
                                    setattr(item, "title", "N/A")

                                # import black list from file
                                black_list = [
                                    " 3.0 ",
                                    " 3.5 ",
                                    " 4.0 ",
                                    " 4.5 ",
                                    " 5.0 ",
                                    " 5.5",
                                    " 6.0 ",
                                    " 6.5 ",
                                    " 7.0 ",
                                    " 7.5 ",
                                    " 8.0 ",
                                    " 8.5 ",
                                    " 50 ",
                                    " 55 ",
                                    " 60 ",
                                    " 65 ",
                                    " 70 ",
                                    " 75 ",
                                    " 80 ",
                                    " 80+ "
                                ]
                                # Add item to set if there is no duplicate ID and if title isn't blacklisted
                                if item.itemId not in ids_set:
                                    if not any(x in item.title for x in black_list):
                                        check_attributes(item)

                                        curr_item = Item(
                                            item.condition.conditionDisplayName,
                                            item.country,
                                            item.listingInfo.startTime,
                                            item.listingInfo.endTime,
                                            item.listingInfo.watchCount,
                                            item.location,
                                            item.returnsAccepted,
                                            item.sellingStatus.currentPrice.value,
                                            item.sellingStatus.currentPrice._currencyId,
                                            item.sellingStatus.sellingState,
                                            item.title,
                                            item.viewItemURL,
                                            item.galleryURL,
                                            item.itemId,
                                            game_name,
                                            site,
                                        )
                                        item_results[game_name].add(curr_item)
                                        curr_results[game_name].add(curr_item)
                                        # maybe not open and close everytime
                                        with open(dirof_item_results, "wb") as f:
                                            pickle.dump(
                                                item_results,
                                                f,
                                                protocol=pickle.HIGHEST_PROTOCOL,
                                            )
                                        with open(
                                            dirof_new_items, "wb"
                                        ) as new_items_file:
                                            pickle.dump(
                                                curr_results, new_items_file, -1
                                            )
                                        ids_set.add(item.itemId)
                                        ids_file.write(item.itemId + "\n")
                                        history_file.write(
                                            "NEW GAME: "
                                            + str(game_name)
                                            + "\n"
                                            + str(item.title)
                                            + "\n"
                                            + str(item.viewItemURL)
                                            + "\n\n\n\n\n"
                                        )
                                    else:
                                        history_file.write(
                                            "Black Listed Item: "
                                            + str(item.title)
                                            + " in server "
                                            + str(site)
                                            + "\n\n"
                                        )
                                else:
                                    history_file.write(
                                        "Duplicate Found "
                                        + str(item.title)
                                        + " in server "
                                        + str(site)
                                        + "\n\n"
                                    )
                            history_file.write("\n")
                        else:
                            history_file.write(
                                "No results for server: "
                                + str(site)
                                + " for "
                                + str(game_name)
                                + "\n\n"
                            )
                print(
                    "Processed Game: %s in Server: %s, API Counter: %d"
                    % (str(game_name), str(site), request_counter)
                )
            history_file.write("NEXT SERVER\n\n\n")
        history_file.write("DONE\n")
        new_items = ids_set.difference(temp_ids_set)
        history_file.write("NEW LISTINGS\n")
        history_file.write(", ".join(str(s) for s in new_items))
        history_file.write("\n")


if __name__ == "__main__":
    main()

