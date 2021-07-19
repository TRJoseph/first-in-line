import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import sys
import selenium.common.exceptions as selexcept
from twilio.rest import Client
import random

client = Client("", "") # Twilio client to send purchase notification through (Account SID, Auth Token)

browser = webdriver.Chrome('') # enter chrome driver local application path

# 3070 ti test case
#browser.get('https://www.amazon.com/EVGA-GeForce-12G-P5-3657-KR-Dual-Fan-Backplate/dp/B08WM28PVH/ref=sr_1_3?dchild=1&keywords=rtx&qid=1626317480&sr=8-3')

# main case
link = "https://www.amazon.com/ZOTAC-Graphics-IceStorm-Advanced-ZT-A30610H-10MLHR/dp/B097YW4FW9/ref=sr_1_6?dchild=1&keywords=rtx+3060+ti&qid=1626127266&sr=8-6" #change this link to a product you would like to buy
browser.get(link)
productname = browser.find_element_by_xpath("//*[@id='productTitle']").text # finds name of product item for twilio to forward to user's notifications
productname = productname[0:60]

buyingOptions = False

while not buyingOptions:
    try:
        price = browser.find_element_by_id('price_inside_buybox').text  # finds first available price
        price = price.replace("$", "")
        price = price.replace(",", "")
        price = int(price[:-3])
        print("Gathering lowest price...")
        print(price)
        buyingOptions = True

        if price < 750:  # if card price is optimal, clicks buy now (set this to preferred purchase condition)
            buyNow = addButton = browser.find_element_by_id("buy-now-button")
            print("Buying now...")
            buyNow.click()

            loginInfo = False

            while not loginInfo:
                try:
                    email = browser.find_element_by_id("ap_email")  # inputs email and clicks next
                    email.click()
                    email.clear()
                    print("Inputting Email...")
                    # email.send_keys("") # Uncomment and input email for login
                    email.send_keys(Keys.RETURN)
                    continueButton = addButton = browser.find_element_by_id("continue")
                    continueButton.click()
                    time.sleep(0.2)

                except:
                    pass

                try:
                    password = browser.find_element_by_id("ap_password")  # inputs password and signs in
                    password.clear()
                    #password.send_keys("") # Uncomment and input password for login
                    print("Inputting Password...")
                    password.send_keys(Keys.ENTER)
                    signInButton = addButton = browser.find_element_by_id('signInSubmit')
                    signInButton.click()
                    time.sleep(0.2)

                    loginInfo = True

                except:
                    pass

                placeOrder = False
                while not placeOrder:
                    try:
                        placeOrderButton = addButton = browser.find_element_by_class_name('place-your-order-button')
                        placeOrderButton.click()

                        # Notifies user of their purchase (Uncomment and enter your phone number into the 'to' spot and enter the twilio phone number into the 'from' spot
                        """client.messages.create(to="",
                                                from_="",
                                                body="You purchased " + productname + " for " + str(price) + " dollars.")"""
                        placeOrder = True
                        buyingOptions = True
                        loginInfo = True
                    except:
                        loginInfo = True
                        time.sleep(random.randrange(1, 3))
        else:
            buyingOptions = False
            time.sleep(random.randrange(2, 11))
            browser.refresh()

    except selexcept.NoSuchElementException:
        buyingOptions = False
        print("Button is not ready yet")
        browser.refresh()
        time.sleep(random.randrange(2, 11))
browser.close()
sys.exit("Process complete.")
