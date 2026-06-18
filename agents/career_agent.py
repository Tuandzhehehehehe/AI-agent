from parser.cv_parser import read_cv

from ai.embedder import embedding
from ai.scorer import score

from ai.career_detector import detect_major
from ai.skill_gap import analyze_skill_gap
from ai.gemini_analyzer import analyze_career

from data.job_pool import JOB_POOL

from core.agent_state import AgentState


class CareerAgent:

    def run(
        self,
        cv_path
    ):

        state = AgentState()

        # =====================
        # READ CV
        # =====================

        state.cv_text = read_cv(
            cv_path
        )

        # =====================
        # CAREER DETECTION
        # =====================

        career_results = detect_major(
            state.cv_text
        )

        state.detected_major = (
            career_results[0]["field"]
        )

        state.career_candidates = (
            career_results[:3]
        )

        # =====================
        # LOCAL JOB MATCHING
        # =====================

        sample_jobs = JOB_POOL.get(
            state.detected_major,
            JOB_POOL["Business"]
        )

        cv_emb = embedding(
            state.cv_text
        )

        results = []

        for job in sample_jobs:

            try:

                job_emb = embedding(
                    job["description"]
                )

                sim = score(
                    cv_emb,
                    job_emb
                )

                results.append({

                    "title":
                        job["title"],

                    "score":
                        round(
                            sim * 100,
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

        state.local_matches = (
            results
        )

        # =====================
        # BEST JOB
        # =====================

        if results:

            state.best_job = (
                results[0]["title"]
            )

            state.best_score = (
                results[0]["score"]
            )

        # =====================
        # SKILL GAP
        # =====================

        gap = analyze_skill_gap(
            state.cv_text,
            state.best_job
        )

        state.skill_gap = gap

        state.missing_skills = (
            gap["missing"]
        )

        # =====================
        # GEMINI ANALYSIS
        # =====================

        try:

            analysis = analyze_career(

                cv_text=
                    state.cv_text,

                target_job=
                    state.best_job,

                skill_gap=
                    gap
            )

            state.career_analysis = (
                analysis
            )

        except Exception as e:

            state.career_analysis = (
                f"Analysis Error: {e}"
            )

        return state