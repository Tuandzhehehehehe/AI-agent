import requests

def get_remote_jobs():

    try:

        response = requests.get(
            "https://remoteok.com/api",
            headers={
                "User-Agent":"Mozilla/5.0"
            },
            timeout=10
        )

        jobs = response.json()

        results = []

        for job in jobs[1:]:

            results.append({
                "title": job.get("position",""),
                "company": job.get("company",""),
                "description": " ".join(
                    job.get("tags",[])
                ),
                "url": job.get("url","")
            })

        return results

    except Exception as e:

        print(e)

        return []