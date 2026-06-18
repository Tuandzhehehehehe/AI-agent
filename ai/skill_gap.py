from data.skills_catalog import (
    SKILLS_CATALOG
)


def analyze_skill_gap(
    cv_text,
    job_title
):

    required_skills = (
        SKILLS_CATALOG.get(
            job_title,
            []
        )
    )

    cv_text = cv_text.lower()

    matched = []

    missing = []

    for skill in required_skills:

        if skill.lower() in cv_text:

            matched.append(
                skill
            )

        else:

            missing.append(
                skill
            )

    coverage = 0

    if required_skills:

        coverage = round(

            len(matched)
            /
            len(required_skills)

            * 100,

            2
        )

    return {

        "job_title":
            job_title,

        "coverage":
            coverage,

        "matched":
            matched,

        "missing":
            missing
    }