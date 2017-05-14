import requests
from bs4 import BeautifulSoup
import time
import datetime


sleepsec = 60

# Your IFTT Maker Trigger URL goes here:#
ifttURL = 'https://maker.ifttt.com/trigger/[triggernamegoeshere]/with/key/[keygoeshere]'
# Site URL:
url = "https://thepihut.com/products/the-magpi-57"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

while True:    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    textDump = soup.get_text()

    if "Default Title - Sold Out" in textDump:
        print "Not in stock. Sleeping. Will check again in " + str(sleepsec) + " seconds. " + str(datetime.datetime.now())
        time.sleep(sleepsec)
    else:
        print "IN STOCK! Sending SMS."
        r = requests.post(ifttURL)
        break

print "Job Done. \n TERMINATED."