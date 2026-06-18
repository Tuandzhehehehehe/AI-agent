import requests

def get_jobs(limit=50):

    response = requests.get(
        "https://remoteok.com/api",
        headers={
            "User-Agent":"Mozilla/5.0"
        },
        timeout=10
    )

    jobs = response.json()

    return jobs[1:limit]