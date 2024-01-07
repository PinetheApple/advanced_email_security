# script to check for malicious links by checking online databet of known malicious links
# url to check - https://urlhaus.abuse.ch/downloads/text/
# terms of use - limit to once in 5 minutes but probably only needs to be checked once in around 3 hours
import time
import requests
import os
from urllib.parse import unquote, urlsplit


def update_file(url, local_path):
    try:
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            # Save the file locally
            with open(local_path, 'w', encoding='utf-8') as local_file:
                local_file.write(response.text)
            print(f"File successfully retrieved and saved locally")
        else:
            print(
                f"Failed to retrieve the file. Status code: {response.status_code}")

    except Exception as e:
        print(f"An exception occurred: {e}")


def check_file(local_path):
    url = "https://urlhaus.abuse.ch/downloads/text/"

    if os.path.exists(local_path):
        # Get the last modified time of the local file
        last_modified_time = os.path.getmtime(local_path)
        current_time = time.time()

        # Check if 3 hours have passed since the last modified time and update if true
        if current_time - last_modified_time >= 3 * 60 * 60:
            update_file(url, local_path)

    else:
        update_file(url, local_path)


def check_link(link) -> int:
    # returns -1 for error, 0 for safe, 1 for malicious
    # return 2 for insecure
    local_path = "../datasets/maliciouslinks.txt"

    link = unquote(link)  # decode url if it's encoded
    scheme, netloc, path = separate_link(link)
    try:
        check_file(local_path)
        with open(local_path, 'r') as local_file:
            for line in local_file:
                if line.strip() == link:
                    return 1
                elif (netloc+path) in line:
                    # check for exact match between netloc and path of both links
                    mal_scheme, mal_netloc, mal_path = separate_link(
                        line.strip())
                    if (netloc == mal_netloc) and (path == mal_path):
                        return 1
            if scheme == 'http://':
                return 2
            return 0

    except Exception as e:
        print(f'An exception occured: {e}')
        return -1


def separate_link(link) -> list:
    if not (link.startswith('http://')):
        try:
            response = requests.head('http://'+link, allow_redirects=True)
            final_url = response.url
            # Check if the final URL it redirects to is secure
            if final_url.startswith('https://'):
                link += 'https://'

        except requests.RequestException:
            pass

    components = urlsplit(link)
    # can return query and fragment as well
    return [components.scheme, components.netloc, components.path]
