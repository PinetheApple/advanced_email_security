# script to check for malicious links by checking online databet of known malicious links
# url to check - https://urlhaus.abuse.ch/downloads/text/
# terms of use - limit to once in 5 minutes but probably only needs to be checked once in around 3 hours
import time
import requests
import os


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
    local_path = "../datasets/maliciouslinks.txt"
    try:
        check_file(local_path)
        with open(local_path, 'r') as local_file:
            for line in local_file:
                if line.strip() == link:
                    return 1
            return 0

    except Exception as e:
        print(f'An exception occured: {e}')
        return -1


print(check_link('http://194.48.250.44/ar'))
