import requests
import json
import time
import datetime

TCIN = 52375339 #Target 'TCIN' product id. Can be found in the details page of the product page. Or the URL
ZIPCODE = 98004
RADIUS = 8 #miles around your zipcode to look for
sleepsec = 14400 #How long before it checks the stores for stock
ifttURL = 'https://maker.ifttt.com/trigger/' #IFTT Trigger goes here.


targetURL = 'https://api.target.com/available_to_promise/v2/' + str(TCIN) + '/search?key=eb2551e4accc14f38cc42d32fbc2b2ea&nearby=' + str(ZIPCODE) + '&inventory_type=stores&multichannel_option=none&field_groups=location_summary&requested_quantity=1&radius=' + str(RADIUS)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

inStock = False
while not inStock:
    response = requests.get(targetURL, headers=headers)
    
    js = response.json()
    js = js['products'][0]
    locations = js['locations']
    
    for loc in locations:
        statusStr = "Checking " + loc['store_name']
        if loc['location_available_to_promise_quantity'] > 0.0 or loc['location_available_to_release_quantity'] > 0.0:
            inStock = True
            statusStr += " ..... YUP!"
        else:
            statusStr += " ..... Nope."
        print statusStr
    
    
    if not inStock:
        print "Not in stock. Sleeping. Will check again in " + str(sleepsec) + " seconds. " + str(datetime.datetime.now())
        time.sleep(sleepsec)
    else:
        print "IN STOCK! Pinging IFTT."
        r = requests.post(ifttURL)

print "Job Done. \n TERMINATED."
    

