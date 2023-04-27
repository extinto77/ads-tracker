from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import requests
import sys

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

dialog_selector = '#dialogOverlay-0 > groupbox:nth-child(1) > browser:nth-child(2)'

accept_dialog_script = (
    f"const browser = document.querySelector('{dialog_selector}');" +
    "browser.contentDocument.documentElement.querySelector('#clearButton').click();"
)

def get_clear_site_data_button(driver):
    return driver.find_element_by_css_selector('#clearSiteDataButton')

def get_clear_site_data_dialog(driver):
    return driver.find_element_by_css_selector(dialog_selector)

def get_clear_site_data_confirmation_button(driver):
    return driver.find_element_by_css_selector('#clearButton')

def clear_firefox_cache(driver, timeout=10):
    driver.get('about:preferences#privacy')
    wait = WebDriverWait(driver, timeout)

    # Click the "Clear Data..." button under "Cookies and Site Data".
    wait.until(get_clear_site_data_button)
    get_clear_site_data_button(driver).click()

    # Accept the "Clear Data" dialog by clicking on the "Clear" button.
    wait.until(get_clear_site_data_dialog)
    driver.execute_script(accept_dialog_script)

    # Accept the confirmation alert.
    wait.until(EC.alert_is_present())
    alert = Alert(driver)
    alert.accept()

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

# Create a new instance of the Firefox driver
options = ChromeOptions()
options.add_argument("--headless")
options.add_extension("uBlock_extension.crx")
driver = webdriver.Chrome(
    options = options
)
driver.delete_all_cookies()

# Go to the url page
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