from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

import requests
import sys
import time
from time import sleep

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

if(len(sys.argv) < 2):
    print("Usage: python main.py <page_url>")
    exit()

#Get Program Args
page_url = sys.argv[1]

print("Loading Ads Servers List...")
ADS_LIST_URL = "https://pgl.yoyo.org/as/serverlist.php?hostformat=adblockplus;showintro=0"

#Get Ads Servers
ads_list_page = requests.get(ADS_LIST_URL)
ads_list = ads_list_page.text.splitlines()
#Remove lines that are not ads servers
ads_list = [x for x in ads_list if x.startswith('||')]
#Remove the || from the beginning of the line
ads_list = [x.replace('||', '') for x in ads_list]
#Remove the ^ from the end of the line
ads_list = [x.replace('^', '') for x in ads_list]
print("Ads Servers List Loaded!")

def start_driver():
    # Create a new instance of the Chrome driver
    options = ChromeOptions()
    options.add_argument("--headless")
    #options.add_extension("uBlock_extension.crx")
    driver = webdriver.Chrome(
        options = options
    )
    #delete_cache(driver)
    # driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
    # "origin": '*',
    # "storageTypes": 'all',
    # })

    return driver

def delete_cache(driver):
    driver.execute_script("window.open('')")  # Create a separate tab than the main one
    driver.switch_to.window(driver.window_handles[-1])  # Switch window to the second tab
    driver.get('chrome://settings/clearBrowserData')  # Open your chrome settings.
    perform_actions(driver, Keys.TAB * 2 + Keys.DOWN * 4 + Keys.TAB * 5 )#+ Keys.ENTER)  # Tab to the time select and key down to say "All Time" then go to the Confirm button and press Enter
    driver.close()  # Close that window
    driver.switch_to.window(driver.window_handles[0])  # Switch Selenium controls to the original tab to continue normal functionality.
    print("Cache&Cookies Deleted!")
    
def perform_actions(driver, keys):
    actions = ActionChains(driver)
    actions.send_keys(keys)
    time.sleep(2)
    print('Performing Actions!')
    actions.perform()

# Go to the url page
driver = start_driver()
driver.get(page_url)
print("=====================================")
print("Loading page: ",page_url)

total_downloaded_bytes = 0
total_ads_bytes = 0
total_requests_number = 0
total_ads_number = 0

def is_ad_request(request):
    request_url = request.url

    # Check if the request URL contains any of the ad server names
    for ad_server in ads_list:
        if ad_server in request_url:
            #print(request.date," | ",request.response.status_code," | ",request.url,)
            return True
        
    return False

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response and request.response.status_code == 200:
        response_size = 0
        try:
            response_size = int(request.response.headers['content-length'])
        except:
            pass

        total_downloaded_bytes += int(response_size)
        total_requests_number += 1
        if is_ad_request(request):
            #print(request.date," | ",request.response.status_code," | ",request.url,)
            total_ads_bytes += int(response_size)
            total_ads_number += 1

total_downloaded_mb = total_downloaded_bytes / 1024 / 1024
total_ads_mb = total_ads_bytes / 1024 / 1024
percentage_of_ads = total_ads_bytes / total_downloaded_bytes * 100

print('Total downloaded: %.2f MB' % total_downloaded_mb)
print('Total ads: %.2f MB (%.2f%%)' % (total_ads_mb, percentage_of_ads))
print('Total requests: %d' % total_requests_number)
print('Total ads requests: %d' % total_ads_number)

driver.close()