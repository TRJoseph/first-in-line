import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import sys
import selenium.common.exceptions as selexcept
from twilio.rest import Client
import random

# Imports config file and assigns to variables
with open('config.json', 'r') as info:
    settings = json.load(info)
    link = settings['MAINDATA']["ITEMLINK"]
    lessThanPrice = int(settings["MAINDATA"]["LESSTHANPRICE"])
    emailLogin = settings["MAINDATA"]["LOGINEMAIL"]
    passwordLogin = settings["MAINDATA"]["LOGINPASSWORD"]
    TwilioSID = settings["TWILIODATA"]["ACCOUNT_SID"]
    TwilioAUTH = settings["TWILIODATA"]["ACCOUNT_AUTH_TOKEN"]
    phoneNum = settings["TWILIODATA"]["YOURPHONENUMBER"]
    TwilioPhoneNum = settings["TWILIODATA"]["TWILIOGIVENPHONENUMBER"]


client = Client(TwilioSID, TwilioAUTH) # sets info for twilio API functionality (check config file to edit)
browser = webdriver.Chrome(ChromeDriverManager.install()) # sets chromedriver application path (check config file to edit)

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

        if price < lessThanPrice:  # if card price is optimal, clicks buy now (set this to preferred purchase condition in config file)
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
                    email.send_keys(emailLogin)
                    email.send_keys(Keys.RETURN)
                    continueButton = addButton = browser.find_element_by_id("continue")
                    continueButton.click()
                    time.sleep(0.2)

                except:
                    pass

                try:
                    password = browser.find_element_by_id("ap_password")  # inputs password and signs in
                    password.clear()
                    password.send_keys(passwordLogin)
                    print("Inputting Password...")
                    password.send_keys(Keys.ENTER)
                    signInButton = addButton = browser.find_element_by_id('signInSubmit')
                    signInButton.click()
                    time.sleep(0.2)

                    loginInfo = True

                except:
                    pass

                placeOrder = False
                placeAttempt = 0
                while not placeOrder:
                    placeAttempt += 1
                    try:
                        placeOrderButton = addButton = browser.find_element_by_class_name('place-your-order-button')
                        placeOrderButton.click()

                        # Notifies user of their purchase (check config file to enter phone numbers)
                        client.messages.create(to=phoneNum,
                                                from_=TwilioPhoneNum,
                                                body="You purchased " + productname + " for " + str(price) + " dollars.")
                        placeOrder = True
                        buyingOptions = True
                        loginInfo = True
                    except:
                        loginInfo = True
                        time.sleep(random.randrange(1, 3))
                        if placeAttempt == 2: # After second buy attempt on placeOrder screen, restarts item check (handles bot being late to getting item if out of stock)
                            placeOrder = True
                            browser.close()
                            browser.get(link)

        else:
            buyingOptions = False
            time.sleep(random.randrange(2, 11))
            browser.refresh()

    except selexcept.NoSuchElementException: # handles button missing; website format changes depending on item availability
        buyingOptions = False
        print("Button is not ready yet")
        browser.refresh()
        time.sleep(random.randrange(2, 11))
browser.close()
sys.exit("Process complete.")
