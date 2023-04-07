from seleniumwire import webdriver
import requests

ads_list_url = "https://pgl.yoyo.org/as/serverlist.php?hostformat=adblockplus;showintro=0"

#Get Ads Servers
ads_list_page = requests.get(ads_list_url)
ads_list = ads_list_page.text.splitlines()
#Remove lines that are not ads servers
ads_list = [x for x in ads_list if x.startswith('||')]
#Remove the || from the beginning of the line
ads_list = [x.replace('||', '') for x in ads_list]
#Remove the ^ from the end of the line
ads_list = [x.replace('^', '') for x in ads_list]


# Create a new instance of the Chrome driver
driver = webdriver.Firefox()

# Go to the Google home page
driver.get('http://jn.pt')

total_downloaded_bytes = 0
total_ads_bytes = 0

def is_ad_request(request):
    request_url = request.url

    # Check if the request URL contains any of the ad server names
    for ad_server in ads_list:
        if ad_server in request_url:
            print(
            request.date,
            " | ",
            request.response.status_code,
            " | ",
            request.url,
            )
            
            return True
        
    return False

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        response_size = 0
        try:
            response_size = int(request.response.headers['content-length'])
        except:
            pass

        total_downloaded_bytes += int(response_size)
        if is_ad_request(request):
            total_ads_bytes += int(response_size)

total_downloaded_mb = total_downloaded_bytes / 1024 / 1024
total_ads_mb = total_ads_bytes / 1024 / 1024
percentage_of_ads = total_ads_bytes / total_downloaded_bytes * 100

print('Total downloaded: %.2f MB' % total_downloaded_mb)
print('Total ads: %.2f MB (%.2f%%)' % (total_ads_mb, percentage_of_ads))