def detect_major(text):

    text = text.lower()

    mapping = {
        "IT": [
            "java",
            "python",
            "spring",
            "developer",
            "software"
        ],

        "Business": [
            "business",
            "management",
            "operations"
        ],

        "Marketing": [
            "marketing",
            "seo",
            "branding",
            "content"
        ],

        "Finance": [
            "finance",
            "accounting",
            "investment"
        ]
    }

    scores = {}

    for field, keywords in mapping.items():

        scores[field] = sum(
            1 for k in keywords
            if k in text
        )

    best = max(
        scores,
        key=scores.get
    )

    return best