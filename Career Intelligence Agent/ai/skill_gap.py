SKILLS = {

    "Business Analyst Intern":[
        "Excel",
        "Power BI",
        "SQL",
        "Requirement Gathering"
    ],

    "Java Backend Intern":[
        "Java",
        "Spring Boot",
        "REST API",
        "MySQL"
    ]
}


def find_missing_skills(
    cv_text,
    job_title
):

    required = SKILLS.get(
        job_title,
        []
    )

    cv_text = cv_text.lower()

    missing = []

    for skill in required:

        if skill.lower() not in cv_text:
            missing.append(skill)

    return missing