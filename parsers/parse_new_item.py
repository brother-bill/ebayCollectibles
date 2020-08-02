from ebaysdk.shopping import Connection as Shopping
from ebaysdk.exception import ConnectionError
import json
from e_collector import Item
        # write to new file new listings to parse
        # for z in new_listings:
        #   print("New Listing: " + str(z))
# Finish with taking item set and finding all items with ids
try:
    api = Shopping(config_file="ebay.yaml")
    response = api.execute("GetSingleItem", {"ItemID": 202855239800})
    if response.reply.Ack == "Success":
        curr = Item(
            response.reply.Item.ConditionDisplayName,
            response.reply.Item.Country,
            "No Start Time",
            response.reply.Item.EndTime,
            "No Watch Count",
            response.reply.Item.Location,
            "Returns Accepted N/A",
            response.reply.Item.ConvertedCurrentPrice.value,
            response.reply.Item.ConvertedCurrentPrice._currencyID,
            response.reply.Item.ListingStatus,
            response.reply.Item.Title,
            response.reply.Item.ViewItemURLForNaturalSearch,
            response.reply.Item.GalleryURL,
            response.reply.Item.ItemID,
            "No Original Name",
            "No Server Name",
        )

except ConnectionError as e:
    print(e)
    print(e.response.dict())
