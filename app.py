import os
import streamlit as st
import pandas as pd

from agents.career_agent import CareerAgent

os.makedirs(
    "uploads",
    exist_ok=True
)

st.set_page_config(
    page_title="Career Intelligence Agent",
    layout="wide"
)

st.title(
    "🚀 Career Intelligence Agent"
)

st.caption(
    "Upload CV → Analyze → Match Jobs → Skill Gap → Career Roadmap"
)

agent = CareerAgent()

cv_file = st.file_uploader(
    "Upload CV PDF",
    type=["pdf"]
)

if cv_file:

    save_path = (
        "uploads/cv.pdf"
    )

    with open(
        save_path,
        "wb"
    ) as f:

        f.write(
            cv_file.getbuffer()
        )

    st.success(
        "CV Uploaded Successfully"
    )

    with st.spinner(
        "Analyzing CV..."
    ):

        state = agent.run(
            save_path
        )

    # ==========================
    # CV PREVIEW
    # ==========================

    st.subheader(
        "📄 CV Preview"
    )

    st.text_area(
        "Content",
        state.cv_text[:3000],
        height=250
    )

    # ==========================
    # CAREER DETECTION
    # ==========================

    st.subheader(
        "🎯 Detected Career Field"
    )

    st.success(
        state.detected_major
    )

    if state.career_candidates:

        st.subheader(
            "📊 Career Candidates"
        )

        st.dataframe(
            pd.DataFrame(
                state.career_candidates
            ),
            use_container_width=True
        )

    # ==========================
    # JOB MATCHING
    # ==========================

    st.subheader(
        "🏆 Career Match"
    )

    if state.local_matches:

        match_df = pd.DataFrame(
            state.local_matches
        )

        st.dataframe(
            match_df,
            use_container_width=True
        )

        st.success(
            f"Best Match: {state.best_job} ({state.best_score}%)"
        )

    # ==========================
    # SKILL GAP
    # ==========================

    st.subheader(
        "🧩 Skill Gap Analysis"
    )

    if state.skill_gap:

        col1, col2 = st.columns(
            2
        )

        with col1:

            st.metric(
                "Skill Coverage",
                f"{state.skill_gap['coverage']}%"
            )

        with col2:

            st.metric(
                "Missing Skills",
                len(
                    state.skill_gap[
                        "missing"
                    ]
                )
            )

        st.markdown(
            "### ✅ Matched Skills"
        )

        st.write(
            state.skill_gap[
                "matched"
            ]
        )

        st.markdown(
            "### ❌ Missing Skills"
        )

        st.write(
            state.skill_gap[
                "missing"
            ]
        )

    # ==========================
    # GEMINI REPORT
    # ==========================

    st.subheader(
        "🤖 Career Advisor Report"
    )

    if state.career_analysis:

        st.markdown(
            state.career_analysis
        )