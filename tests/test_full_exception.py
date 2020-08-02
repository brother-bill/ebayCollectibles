from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

siteList = [
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

counter = 0
with open("test.txt", "w", encoding="utf-8") as test_file:
    for i in range(20):
        for site in siteList:
            try:
                api_request = {
                    "keywords": "Nintendo Wii",
                    "itemFilter": [{"name": "Condition", "value": "1000"}],
                }
                api = Finding(
                    domain="svcs.ebay.com",
                    config_file="ebay.yaml",
                    https=True,
                    siteid=site,
                )
                response = api.execute("findItemsAdvanced", api_request)
                if response.status_code == 404:
                    print("WE BROKE IN IF")
                    test_file.write("WE BROKE IN IF\n")
                else:
                    print(response.status_code)
                    test_file.write(str(response.status_code) + "\n")
                print("Finished server: " + str(counter))
                counter += 1
            except AttributeError as e:
                print(e)
                # print(e.response.dict())
                print("WE BROKE IN ATTRIBUTE ERROR")
                test_file.write("WE BROKE IN ATTRIBUTE\n")
                test_file.write(str(e) + "\n")
            except ConnectionError as e:
                print(e)
                print("WE BROKE IN CONNECTION ERROR")
                test_file.write("WE BROKE IN CONNECTION\n")
                test_file.write(str(e) + "\n")
            except Exception as e:
                print(e)
                print("WE SIMPLY BROKE")
                test_file.write("WE SIMPLY BROKE\n")
                test_file.write(str(e) + "\n")
