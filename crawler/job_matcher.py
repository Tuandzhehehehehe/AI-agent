import pandas as pd

from ai.embedder import embedding
from ai.scorer import score


def rank_jobs(
    cv_text,
    jobs,
    top_k=20
):
    """
    Rank jobs by similarity score
    between CV and Job Description.
    """

    if not cv_text:
        return pd.DataFrame()

    if not jobs:
        return pd.DataFrame()

    cv_emb = embedding(cv_text)

    results = []

    for job in jobs:

        description = job.get(
            "description",
            ""
        )

        if not description:
            continue

        try:

            job_emb = embedding(
                description
            )

            similarity = score(
                cv_emb,
                job_emb
            )

            results.append({

                "title":
                    job.get(
                        "title",
                        ""
                    ),

                "company":
                    job.get(
                        "company",
                        ""
                    ),

                "score":
                    round(
                        similarity * 100,
                        2
                    ),

                "description":
                    description,

                "url":
                    job.get(
                        "url",
                        ""
                    )
            })

        except Exception as e:

            print(
                f"Error ranking job: {e}"
            )

    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(
        results
    )

    df = df.sort_values(
        by="score",
        ascending=False
    )

    return df.head(top_k)