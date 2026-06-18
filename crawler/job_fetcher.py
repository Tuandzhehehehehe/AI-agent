from crawler.remoteok import get_jobs

def fetch_remote_jobs():

    raw_jobs = get_jobs()

    jobs = []

    for job in raw_jobs:

        jobs.append({
            "title":
                job.get("position",""),

            "company":
                job.get("company",""),

            "description":
                " ".join(
                    job.get("tags",[])
                ),

            "url":
                job.get("url","")
        })

    return jobs