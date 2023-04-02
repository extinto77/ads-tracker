
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json


def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response



caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(desired_capabilities=caps)
driver.get('http://jn.pt')

browser_log = driver.get_log('performance') 
events = [process_browser_log_entry(entry) for entry in browser_log]
events = [event for event in events if 'Network.response' in event['method']]

#inisert the output in a file
with open('output.txt', 'w') as f:
    #for item in events:
    output = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': events[0]['params']['requestId']}) 
    for k,item in output.items():
        f.write(k+':'+str(item)+'\n')

#for i in range(len(events)):
#    print(driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': events[i]['params']['requestId']}))
#    # driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': events["params"]["requestId"]})



# browser = webdriver.Firefox()
# info = browser.get("http://jn.pt")
# info = browser.find_elements(By.CLASS_NAME,"fc-button fc-cta-consent fc-primary-button")[0]
# info.click()
# print(info)


# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button__acceptAll > span.baseText"))).click()