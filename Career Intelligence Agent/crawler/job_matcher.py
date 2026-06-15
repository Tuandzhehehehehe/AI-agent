import pandas as pd

from ai.embedder import embedding
from ai.scorer import score

def rank_jobs(
        cv_text,
        jobs
):

    cv_emb = embedding(
        cv_text
    )

    results = []

    for job in jobs:

        job_emb = embedding(
            job["description"]
        )

        similarity = score(
            cv_emb,
            job_emb
        )

        results.append({

            "title":
                job["title"],

            "company":
                job["company"],

            "score":
                round(
                    similarity * 100,
                    2
                ),

            "url":
                job["url"]
        })

    return pd.DataFrame(
        results
    ).sort_values(
        "score",
        ascending=False
    )