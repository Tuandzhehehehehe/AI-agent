import requests

def get_jobs():

    url = "https://remoteok.com/api"

    data = requests.get(
        url,
        headers={
            "User-Agent":"Mozilla/5.0"
        }
    ).json()

    return data[:50]