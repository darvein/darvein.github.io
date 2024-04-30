import os
import sys
import random
import string
import requests

APP_URL=os.getenv('URL', 'https://google.com/')

def check_http_status(url):
    status_code = -1

    try:
        response = requests.get(url)
        status_code = response.status_code
    except requests.exceptions.RequestException as e:
        pass

    return status_code

def generate_random_string(max_length=2):
    length = random.randint(0, max_length)
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

domain = generate_random_string()
urlpath = generate_random_string()
url = APP_URL.replace('http', 'http' + domain) + urlpath

print("Querying URL: {}".format(url))
status_code = check_http_status(url)
print('Status Code:', status_code)

# Finish the app
if status_code == 200:
    sys.exit(0) # Success!
elif status_code == 404:
    sys.exit(2)
else:
    sys.exit(3)
