from dataclasses import dataclass, field


@dataclass
class AgentState:

    cv_text: str = ""

    detected_major: str = ""

    best_job: str = ""

    best_score: float = 0

    local_matches: list = field(
        default_factory=list
    )

    remote_matches: list = field(
        default_factory=list
    )

    missing_skills: list = field(
        default_factory=list
    )

    career_analysis: str = ""