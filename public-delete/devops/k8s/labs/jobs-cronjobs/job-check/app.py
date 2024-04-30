import os
import sys
import requests

APP_URL=os.getenv('URL', 'https://google.com')

def check_http_status(url):
    try:
        response = requests.get(url)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return "Error: Invalid URL or the request was not successful. Details: " + str(e)

status_code = check_http_status(APP_URL)
print('Status Code:', status_code)

# Finish the app
if status_code == 200:
    sys.exit(0) # Success!
else:
    sys.exit(1) # Failed!
