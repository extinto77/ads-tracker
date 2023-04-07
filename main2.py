from seleniumwire import webdriver

# Create a new instance of the Chrome driver
driver = webdriver.Firefox()

# Go to the Google home page
driver.get('http://jn.pt')

total_downloaded_bytes = 0
total_ads_bytes = 0

def is_ad_request(request):
    return True

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        print(
            request.date,
            " | ",
            request.response.status_code,
            " | ",
            request.url,
        )

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