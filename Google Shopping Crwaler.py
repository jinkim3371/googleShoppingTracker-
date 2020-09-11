from selenium import webdriver
import csv
import time
import pprint
import os
import pyautogui
import argparse


# parser = argparse.ArgumentParser(description='Crawl google shopping page and compare price with the target price.')
# parser.add_argument('TargetPrice', metavar='-pr', type=str, nargs='+',
#                    help='Target price in string (ex."$199.99)')
# parser.add_argument('Address', metavar='-adr', type=str, nargs='+',
#                    help='Web address for the target product')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')
# args = parser.parse_args()

SETTING_PATH = os.path.realpath(os.path.dirname(__file__)) + "/"

def get_prices():
    product_name = driver.find_element_by_xpath("//div[@class='f0t7kf']").text
    product_name = product_name.split("\n")

    id1 = driver.find_elements_by_class_name("sh-osd__seller-link")
    ids = driver.find_elements_by_class_name("sh-osd__total-price")

    # get address for the seller
    addrList = []
    for elem in id1:
        address = elem.get_attribute('href')
        siteName = elem.text
        addrList.append((siteName, address))

    # get prices
    price_list = []
    for ii in ids:
        idx = ii.text
        price_list.append(idx)

    if len(price_list) > len(addrList):
        price_list.pop(0)

    return product_name[0], addrList, price_list


def email_alert(subject, body, to):
    #  code from @ClarityCoders
    #  https://www.youtube.com/watch?v=B1IsCbXp0uE&feature=youtu.be&ab_channel=ClarityCoders

    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "Type_your_email@gmail.com"
    msg['from'] = user
    password = "Get This Password.(Refer to youtube link above)"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()



## ____ Main ____

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)          # running silent-mode ( no browser )
# driver = webdriver.Chrome('./chromedriver')              # Uncomment to see browser
driver.implicitly_wait(3)

with open('googleShoppingList.csv', 'rt') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    line_count = 0
    for row in csv_reader:
        threshold = row[0]
        googleAddr = row[1]

        driver.get(googleAddr)
        product_name, addrList, price_list = get_prices()
   #     googleAddr = str(args.accumulate(args.Address))
   #     threshold = args.accumulate(args.TargetPrice)
        good_prices = []

        for i in range(0,len(price_list)):
            if price_list[i] < threshold:
                good_prices.append((product_name, price_list[i], addrList[i][0], addrList[i][1]))

        print(" Product Name : ", product_name)
        for j in good_prices:
            print(j[1], "    \t Site: ", j[2])

        email_alert("**Deal Alert** ", str(j[0] + "\n" + j[1] + "\nSite: " + j[2] + "\nAddr: " + j[3]),
                    "#########@tmomail.net")

        # Store result in a spreadsheet
        with open('goodPrices.csv', 'a', newline='') as csvfile:
            priceWriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in good_prices:
                priceWriter.writerow(row)

email_alert("PyGoogleShopping Tracker", "Ran", "##########@tmomail.net")
