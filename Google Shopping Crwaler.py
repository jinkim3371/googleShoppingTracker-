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
MOVIE_LIST_FILE = SETTING_PATH + "movie_list.txt"

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


def txt_editor(data_idx):
    f = open(MOVIE_LIST_FILE, "r", encoding="utf-8")
    lines = f.readlines()
    print("data_idx : ", data_idx)
    buffer = ""
    for line in lines:
        buffer = line
        fileName = getName(data_idx)
        print(" Line :: " , line, " data_idx ::", data_idx, "  Name :: ", fileName)
        if int(line) < int(data_idx):
            print( " ------->> Update file from ", line, " to ", data_idx)
            print()
            buffer = str(data_idx)
    f = open(MOVIE_LIST_FILE, "w", encoding="utf-8")
    f.write(buffer)
    f.close()

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)



with open('googleShoppingList.csv', 'rt') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # print("row:", row)
        # print(" 0, 0 ", row[0])
        # print(" 0, 1 ", row[1])

        threshold = row[0]
        googleAddr = row[1]

   #     googleAddr = str(args.accumulate(args.Address))
        driver.get(googleAddr)

        #___main___
        # if len(driver.find_elements_by_class_name("sh-btn__background")) > 0:
        #     driver.find_element_by_xpath("//*[@class ='sh-btn__background']").click()

        product_name, addrList, price_list = get_prices()
   #     threshold = args.accumulate(args.TargetPrice)
        good_prices = []

        for i in range(0,len(price_list)):
            if price_list[i] < threshold:
                good_prices.append((product_name, price_list[i], addrList[i][0], addrList[i][1]))

        print(" Product Name : ", product_name)
        for j in good_prices:
            print(j[1], "    \t Site: ", j[2])

        with open('goodPrices.csv', 'a', newline='') as csvfile:
            priceWriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in good_prices:
                priceWriter.writerow(row)