from ai.embedder import embedding
from ai.scorer import score

from data.career_profiles import (
    CAREER_PROFILES
)


def detect_major(text):

    cv_embedding = embedding(
        text
    )

    results = []

    for field, profile in (
        CAREER_PROFILES.items()
    ):

        try:

            profile_embedding = embedding(
                profile
            )

            similarity = score(
                cv_embedding,
                profile_embedding
            )

            results.append({

                "field":
                    field,

                "score":
                    round(
                        similarity * 100,
                        2
                    )
            })

        except Exception:
            pass

    results = sorted(
        results,
        key=lambda x:
            x["score"],
        reverse=True
    )

    return results