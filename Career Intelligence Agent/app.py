import os
import streamlit as st
import pandas as pd

from parser.cv_parser import read_cv

from ai.embedder import embedding
from ai.scorer import score

from ai.career_detector import detect_major
from ai.skill_gap import find_missing_skills

from crawler.job_fetcher import get_remote_jobs

# ==========================
# CONFIG
# ==========================

os.makedirs("uploads", exist_ok=True)

st.set_page_config(
    page_title="Career Intelligence Agent",
    layout="wide"
)

st.title("🚀 Career Intelligence Agent")
st.caption(
    "Upload CV → Match Career → Find Real Jobs"
)

# ==========================
# UPLOAD CV
# ==========================

cv_file = st.file_uploader(
    "Upload CV PDF",
    type=["pdf"]
)

if cv_file is not None:

    save_path = "uploads/cv.pdf"

    with open(save_path, "wb") as f:
        f.write(cv_file.getbuffer())

    st.success("CV Uploaded")

    # ==========================
    # READ CV
    # ==========================

    cv_text = read_cv(save_path)

    st.subheader("📄 CV Preview")

    st.text_area(
        "Content",
        cv_text[:3000],
        height=250
    )

    # ==========================
    # DETECT CAREER
    # ==========================

    major = detect_major(
        cv_text
    )

    st.subheader(
        "🎯 Career Field"
    )

    st.info(
        f"Detected Field: {major}"
    )

    # ==========================
    # SAMPLE JOBS
    # ==========================

    sample_jobs = [

        {
            "title":"Java Backend Intern",
            "description":"Java Spring Boot REST API MySQL"
        },

        {
            "title":"AI Engineer Intern",
            "description":"Python Machine Learning RAG LangGraph"
        },

        {
            "title":"Business Analyst Intern",
            "description":"Excel Power BI SQL Requirement Gathering"
        },

        {
            "title":"Marketing Intern",
            "description":"SEO Content Marketing Social Media"
        },

        {
            "title":"Finance Intern",
            "description":"Financial Analysis Accounting Budget Forecast"
        }

    ]

    # ==========================
    # EMBEDDING MATCH
    # ==========================

    cv_emb = embedding(
        cv_text
    )

    results = []

    for job in sample_jobs:

        job_emb = embedding(
            job["description"]
        )

        similarity = score(
            cv_emb,
            job_emb
        )

        results.append(
            {
                "Job": job["title"],
                "Score": round(
                    similarity * 100,
                    2
                )
            }
        )

    df = pd.DataFrame(
        results
    )

    df = df.sort_values(
        "Score",
        ascending=False
    )

    st.subheader(
        "🏆 Career Match"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    best_job = df.iloc[0]

    st.success(
        f"Best Match: {best_job['Job']} ({best_job['Score']}%)"
    )

    # ==========================
    # SKILL GAP
    # ==========================

    missing_skills = find_missing_skills(
        cv_text,
        best_job["Job"]
    )

    st.subheader(
        "📚 Skill Gap Analysis"
    )

    if len(missing_skills) == 0:

        st.success(
            "CV already matches most required skills."
        )

    else:

        for skill in missing_skills:

            st.warning(
                f"Missing: {skill}"
            )

    # ==========================
    # ROADMAP
    # ==========================

    st.subheader(
        "🛣 Learning Roadmap"
    )

    if len(missing_skills):

        roadmap = []

        week = 1

        for skill in missing_skills:

            roadmap.append(
                {
                    "Week": week,
                    "Focus": skill
                }
            )

            week += 1

        roadmap_df = pd.DataFrame(
            roadmap
        )

        st.dataframe(
            roadmap_df,
            use_container_width=True
        )

    # ==========================
    # REAL JOB SEARCH
    # ==========================

    st.subheader(
        "🌍 Real Job Search"
    )

    if st.button(
        "Search Real Jobs"
    ):

        with st.spinner(
            "Searching jobs..."
        ):

            jobs = get_remote_jobs()

        if len(jobs) == 0:

            st.error(
                "Cannot fetch jobs."
            )

        else:

            rankings = []

            for job in jobs:

                try:

                    text = (
                        job["title"]
                        + " "
                        + job["description"]
                    )

                    job_emb = embedding(
                        text
                    )

                    sim = score(
                        cv_emb,
                        job_emb
                    )

                    rankings.append({

                        "Title":
                            job["title"],

                        "Company":
                            job["company"],

                        "Score":
                            round(
                                sim * 100,
                                2
                            ),

                        "URL":
                            job["url"]
                    })

                except:
                    pass

            real_df = pd.DataFrame(
                rankings
            )

            real_df = real_df.sort_values(
                "Score",
                ascending=False
            )

            st.dataframe(
                real_df.head(20),
                use_container_width=True
            )

            st.success(
                f"Found {len(real_df)} jobs"
            )
