"""
app.py - Placement Readiness Assistant (Advanced Streamlit Web App)
-------------------------------------------------------------------
A comprehensive, transparent web application for university students to
evaluate their campus placement preparation and audit their resumes.

Features:
1. 6-Factor Placement Readiness Predictor + Company Tier Simulator + 4-Week Roadmap
2. Role-Based Smart Resume Analyzer + Section & Impact Scanner
3. Downloadable Assessment Reports
4. Transparent Scoring Documentation & 3-Member Team Matrix
"""

import streamlit as st
from predictor import calculate_placement_readiness, CLASSROOM_DISCLAIMER
from resume_analyzer import (
    analyze_resume,
    parse_skills_input,
    ROLE_SKILL_PRESETS,
    RESUME_DISCLAIMER,
)

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Placement Readiness Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# Sidebar: Project Info & Quick Navigation
# ---------------------------------------------------------
with st.sidebar:
    st.title("🎓 Placement Assistant")
    st.markdown(
        """
        **Advanced Classroom Project Demo**

        **What's Inside:**
        - 📊 **6-Factor Readiness Engine**
        - 🏢 **Company Tier Eligibility Simulator**
        - 🗓️ **Personalized 4-Week Study Plan**
        - 📄 **Role-Based Resume & ATS Auditor**
        - ⚡ **Action Verb & Impact Metric Scanner**
        - 📥 **Downloadable Student Reports**

        ---
        **Core Principles:**
        - 🔍 **100% Transparent Rules**
        - 🚫 **Zero Personal Data Stored**
        - ⚠️ **Educational Simulation Only**
        """
    )
    st.info("💡 **Demo Tip:** Try changing the Job Role Preset and clicking 'Load Sample Resume' in Tab 2!")

# ---------------------------------------------------------
# Main Header
# ---------------------------------------------------------
st.title("🎓 Placement Readiness Assistant")
st.caption(
    "An interactive, rule-based self-assessment and resume auditing platform "
    "for campus placement preparation."
)

st.warning(CLASSROOM_DISCLAIMER)

# ---------------------------------------------------------
# Tabs
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Placement Readiness Predictor",
    "📄 Smart Resume & ATS Analyzer",
    "ℹ️ Scoring Rules & Architecture",
    "👥 Team & Contributions",
])

# =========================================================
# TAB 1: ADVANCED PLACEMENT READINESS PREDICTOR
# =========================================================
with tab1:
    st.subheader("📊 Multi-Dimensional Placement Readiness Predictor")
    st.markdown(
        "Enter your academic, coding, project, and internship details below to compute "
        "your **100-point readiness score**, check **company tier eligibility**, and generate "
        "a **personalized 4-week preparation roadmap**."
    )

    col_input, col_output = st.columns([1, 1.3], gap="large")

    with col_input:
        st.markdown("### 📝 Student Profile Inputs")

        cgpa_val = st.slider(
            "1. Cumulative Grade Point Average (CGPA)",
            min_value=0.0,
            max_value=10.0,
            value=7.8,
            step=0.1,
            help="Contributes up to 25 points. Scaled directly out of 10.0.",
        )

        c1, c2 = st.columns(2)
        with c1:
            projects_val = st.number_input(
                "2. Technical Projects Built",
                min_value=0,
                max_value=25,
                value=2,
                step=1,
                help="Contributes up to 20 points (10 pts per major project, capped at 2).",
            )
        with c2:
            internships_val = st.number_input(
                "3. Internships Completed",
                min_value=0,
                max_value=10,
                value=1,
                step=1,
                help="Contributes up to 20 points (10 pts per internship, capped at 2).",
            )

        c3, c4 = st.columns(2)
        with c3:
            dsa_val = st.number_input(
                "4. DSA / Coding Problems Solved",
                min_value=0,
                max_value=1500,
                value=90,
                step=10,
                help="Problems solved on LeetCode/GFG/HackerRank. Up to 15 points (150+ problems = full 15 pts).",
            )
        with c4:
            certs_val = st.number_input(
                "5. Certifications / Hackathons",
                min_value=0,
                max_value=20,
                value=1,
                step=1,
                help="Contributes up to 10 points (5 pts each, capped at 2).",
            )

        aptitude_val = st.slider(
            "6. Core CS (DBMS, OS, CN) & Aptitude Preparation Level (1 = Beginner, 5 = Strong)",
            min_value=1,
            max_value=5,
            value=3,
            step=1,
            help="Self-rating of Core CS subjects and Quantitative Aptitude. Contributes up to 10 points (2 pts per level).",
        )

        st.button("🔄 Recalculate Readiness Profile", type="primary", use_container_width=True)

    with col_output:
        results = calculate_placement_readiness(
            cgpa=cgpa_val,
            internships=internships_val,
            projects=projects_val,
            dsa_problems=dsa_val,
            certifications=certs_val,
            aptitude_level=aptitude_val,
        )
        bd = results["breakdown"]

        st.markdown("### 🎯 Readiness Assessment Dashboard")

        mcol1, mcol2 = st.columns([1, 1.4])
        with mcol1:
            st.metric("Overall Readiness Score", f"{results['total_score']} / 100")
        with mcol2:
            st.metric("Readiness Classification", results["readiness_level"])

        st.progress(results["total_score"] / 100.0)
        st.caption(f"**Summary:** {results['summary']}")

        # Visual Category Breakdown
        with st.expander("🔍 Detailed 6-Factor Point Breakdown (Out of 100)", expanded=True):
            b1, b2 = st.columns(2)
            with b1:
                st.write(f"**📚 Academics (CGPA):** `{bd['cgpa_points']} / {bd['max_cgpa_points']} pts`")
                st.progress(bd["cgpa_points"] / bd["max_cgpa_points"])

                st.write(f"**🛠️ Technical Projects:** `{bd['project_points']} / {bd['max_project_points']} pts`")
                st.progress(bd["project_points"] / bd["max_project_points"])

                st.write(f"**💼 Internships:** `{bd['internship_points']} / {bd['max_internship_points']} pts`")
                st.progress(bd["internship_points"] / bd["max_internship_points"])

            with b2:
                st.write(f"**💻 DSA Problem Solving:** `{bd['dsa_points']} / {bd['max_dsa_points']} pts`")
                st.progress(bd["dsa_points"] / bd["max_dsa_points"])

                st.write(f"**🏅 Certs & Hackathons:** `{bd['cert_points']} / {bd['max_cert_points']} pts`")
                st.progress(bd["cert_points"] / bd["max_cert_points"])

                st.write(f"**🧠 Core CS & Aptitude:** `{bd['aptitude_points']} / {bd['max_aptitude_points']} pts`")
                st.progress(bd["aptitude_points"] / bd["max_aptitude_points"])

    st.divider()

    # Company Tier Readiness & 4-Week Roadmap side-by-side
    bot_col1, bot_col2 = st.columns([1, 1], gap="large")

    with bot_col1:
        st.markdown("### 🏢 Company Tier Eligibility Simulator")
        st.caption("Simulated readiness across common campus recruitment drive categories:")
        for tier_info in results["company_tiers"]:
            with st.container(border=True):
                st.markdown(f"**{tier_info['tier']}** — {tier_info['status']}")
                st.caption(f"*Typical Criteria:* {tier_info['criteria']}")
                st.write(tier_info["note"])

    with bot_col2:
        st.markdown("### 🗓️ Personalized 4-Week Action Plan")
        st.caption("Suggested weekly sprint based on your current profile inputs:")
        for step in results["roadmap"]:
            with st.container(border=True):
                st.markdown(f"**{step['week']}**")
                st.write(step["task"])

    st.markdown("### 💡 Key Recommendations for Improvement")
    for sug in results["suggestions"]:
        st.info(sug)

    # Downloadable Report
    report_text = (
        f"PLACEMENT READINESS ASSESSMENT REPORT\n"
        f"=====================================\n"
        f"Overall Score: {results['total_score']} / 100 ({results['readiness_level']})\n\n"
        f"INPUT PROFILE:\n"
        f"- CGPA: {cgpa_val} ({bd['cgpa_points']}/25 pts)\n"
        f"- Projects: {projects_val} ({bd['project_points']}/20 pts)\n"
        f"- Internships: {internships_val} ({bd['internship_points']}/20 pts)\n"
        f"- DSA Problems Solved: {dsa_val} ({bd['dsa_points']}/15 pts)\n"
        f"- Certifications/Hackathons: {certs_val} ({bd['cert_points']}/10 pts)\n"
        f"- Core CS & Aptitude Level: {aptitude_val}/5 ({bd['aptitude_points']}/10 pts)\n\n"
        f"RECOMMENDATIONS:\n"
        + "\n".join([f"* {s}" for s in results["suggestions"]])
        + f"\n\nDISCLAIMER:\n{CLASSROOM_DISCLAIMER}\n"
    )
    st.download_button(
        label="📥 Download Readiness Report (.txt)",
        data=report_text,
        file_name="placement_readiness_report.txt",
        mime="text/plain",
    )


# =========================================================
# TAB 2: SMART RESUME & ATS ANALYZER
# =========================================================
with tab2:
    st.subheader("📄 Smart Resume Keyword, Structure & Impact Analyzer")
    st.markdown(
        "Select a target job role (or customize the skill list), paste your resume text, "
        "and run a multi-layered check for **skills, standard sections, portfolio links, "
        "action verbs, and measurable metrics**."
    )
    st.caption(f"*{RESUME_DISCLAIMER}*")

    # Role Preset & Custom Skill Selector
    rcol1, rcol2 = st.columns([1, 2], gap="medium")
    with rcol1:
        selected_role = st.selectbox(
            "🎯 Select Target Job Role Preset:",
            options=list(ROLE_SKILL_PRESETS.keys()),
            index=0,
            help="Loads standard technical and soft skills for the chosen role.",
        )
    with rcol2:
        custom_skills_input = st.text_area(
            "✏️ Target Skills List (Editable — add or remove any skills):",
            value=", ".join(ROLE_SKILL_PRESETS[selected_role]),
            height=90,
        )

    SAMPLE_RESUME = (
        "Alex Kumar\n"
        "Email: alex.kumar@university.edu | GitHub: github.com/alexkumar | LinkedIn: linkedin.com/in/alexkumar\n\n"
        "EDUCATION\n"
        "B.Tech in Computer Science and Engineering — CGPA: 8.4 / 10.0 (2022 - 2026)\n\n"
        "TECHNICAL SKILLS\n"
        "Languages & Databases: Python, Java, C++, SQL, JavaScript, HTML, CSS\n"
        "Frameworks & Tools: React, Node.js, Git, Docker, REST APIs, Linux\n"
        "Core & Soft Skills: Data Structures, Algorithms, Problem Solving, Teamwork, Communication\n\n"
        "EXPERIENCE\n"
        "Software Engineering Intern | CloudTech Solutions (May 2025 - July 2025)\n"
        "- Developed and deployed REST APIs using Python and SQL, reducing query latency by 30%.\n"
        "- Collaborated with a cross-functional team of 6 engineers using Git and Agile workflows.\n\n"
        "PROJECTS\n"
        "1. Smart Campus Portal: Built a full-stack web application serving 500+ student users.\n"
        "2. Automated Resume Parser: Implemented regex and NLP pipelines achieving 92% accuracy.\n\n"
        "ACHIEVEMENTS & CERTIFICATIONS\n"
        "- Winner at Smart India College Hackathon 2025 (Top 1% among 150+ teams).\n"
        "- AWS Cloud Practitioner Certified."
    )

    btn_col1, btn_col2 = st.columns([1, 4])
    with btn_col1:
        load_sample = st.button("📋 Load Sample Resume")

    if "resume_text" not in st.session_state:
        st.session_state.resume_text = ""
    if load_sample:
        st.session_state.resume_text = SAMPLE_RESUME

    resume_text_input = st.text_area(
        "Paste Your Resume Text Below:",
        value=st.session_state.resume_text,
        height=230,
        placeholder="Paste the full plain text of your resume here (Contact info, Education, Skills, Projects, Internships, Achievements)...",
    )
    st.session_state.resume_text = resume_text_input

    analyze_btn = st.button("🔍 Run Full Resume Audit", type="primary")

    if analyze_btn or (load_sample and resume_text_input):
        target_skills_list = parse_skills_input(custom_skills_input)
        analysis = analyze_resume(resume_text_input, target_skills_list)

        if "error" in analysis:
            st.error(analysis["error"])
        else:
            st.markdown("### 📊 Comprehensive Resume Audit Results")

            # Top KPI row
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Overall Resume Score", f"{analysis['overall_resume_score']} / 100")
            k2.metric("Skill Match Rate", f"{analysis['match_percentage']}%")
            k3.metric("Skills Matched", f"{analysis['matched_count']} / {analysis['total_target_count']}")
            k4.metric("Resume Word Count", f"{analysis['word_count']} words")

            st.progress(analysis["overall_resume_score"] / 100.0)

            # Matched vs Missing Skills (Categorized)
            col_match, col_miss = st.columns(2, gap="medium")

            with col_match:
                st.markdown("#### ✅ Matched Skills Found")
                if analysis["matched_skills"]:
                    if analysis["matched_technical"]:
                        st.caption("**Technical & Domain Skills:**")
                        tech_html = " ".join([
                            f"<span style='background-color:#d4edda; color:#155724; padding:4px 10px; border-radius:15px; margin:3px; display:inline-block; font-weight:500;'>✓ {s}</span>"
                            for s in analysis["matched_technical"]
                        ])
                        st.markdown(tech_html, unsafe_allow_html=True)
                    if analysis["matched_soft"]:
                        st.caption("**Soft & Professional Skills:**")
                        soft_html = " ".join([
                            f"<span style='background-color:#cce5ff; color:#004085; padding:4px 10px; border-radius:15px; margin:3px; display:inline-block; font-weight:500;'>✓ {s}</span>"
                            for s in analysis["matched_soft"]
                        ])
                        st.markdown(soft_html, unsafe_allow_html=True)
                else:
                    st.warning("No target skills matched in the provided text.")

            with col_miss:
                st.markdown("#### ⚠️ Missing Target Skills")
                if analysis["missing_skills"]:
                    if analysis["missing_technical"]:
                        st.caption("**Missing Technical Skills:**")
                        mtech_html = " ".join([
                            f"<span style='background-color:#f8d7da; color:#721c24; padding:4px 10px; border-radius:15px; margin:3px; display:inline-block; font-weight:500;'>✗ {s}</span>"
                            for s in analysis["missing_technical"]
                        ])
                        st.markdown(mtech_html, unsafe_allow_html=True)
                    if analysis["missing_soft"]:
                        st.caption("**Missing Soft Skills:**")
                        msoft_html = " ".join([
                            f"<span style='background-color:#fff3cd; color:#856404; padding:4px 10px; border-radius:15px; margin:3px; display:inline-block; font-weight:500;'>✗ {s}</span>"
                            for s in analysis["missing_soft"]
                        ])
                        st.markdown(msoft_html, unsafe_allow_html=True)
                else:
                    st.success("🎉 Every single target skill for this role was found in your resume!")

            st.divider()

            # Structure, Links & Impact Audit
            scol1, scol2, scol3 = st.columns(3, gap="medium")

            with scol1:
                st.markdown("#### 📑 Essential Sections Check")
                for sec_name, is_present in analysis["sections_audit"].items():
                    icon = "✅" if is_present else "❌"
                    status_txt = "Detected" if is_present else "Not Found"
                    st.write(f"{icon} **{sec_name}:** _{status_txt}_")

            with scol2:
                st.markdown("#### 🔗 Contact & Portfolio Links")
                for link_name, is_present in analysis["links_audit"].items():
                    icon = "✅" if is_present else "⚠️"
                    status_txt = "Included" if is_present else "Missing"
                    st.write(f"{icon} **{link_name}:** _{status_txt}_")

            with scol3:
                st.markdown("#### ⚡ Action Verbs & Metrics")
                verbs = analysis["impact_audit"]["verbs_found"]
                metrics = analysis["impact_audit"]["metrics_found"]
                st.write(f"**Strong Action Verbs ({len(verbs)}):**")
                st.caption(", ".join(verbs) if verbs else "None detected (add verbs like Built, Developed, Optimized)")
                st.write(f"**Quantified Metrics ({len(metrics)}):**")
                st.caption(", ".join(metrics) if metrics else "None detected (add numbers like 25%, 100+ users)")

            st.markdown("#### 💡 Tailored Resume Improvement Suggestions")
            for sug in analysis["suggestions"]:
                st.info(sug)

            # Download Resume Audit Report
            res_report = (
                f"SMART RESUME AUDIT REPORT ({selected_role})\n"
                f"==================================================\n"
                f"Overall Resume Score: {analysis['overall_resume_score']} / 100\n"
                f"Skill Match Percentage: {analysis['match_percentage']}% ({analysis['matched_count']}/{analysis['total_target_count']})\n"
                f"Word Count: {analysis['word_count']} words\n\n"
                f"MATCHED SKILLS:\n{', '.join(analysis['matched_skills']) or 'None'}\n\n"
                f"MISSING SKILLS:\n{', '.join(analysis['missing_skills']) or 'None'}\n\n"
                f"ACTION VERBS FOUND:\n{', '.join(verbs) or 'None'}\n\n"
                f"QUANTIFIED METRICS FOUND:\n{', '.join(metrics) or 'None'}\n\n"
                f"SUGGESTIONS:\n"
                + "\n".join([f"* {s}" for s in analysis["suggestions"]])
                + f"\n\nDISCLAIMER:\n{RESUME_DISCLAIMER}\n"
            )
            st.download_button(
                label="📥 Download Resume Audit Report (.txt)",
                data=res_report,
                file_name="resume_audit_report.txt",
                mime="text/plain",
            )


# =========================================================
# TAB 3: HOW IT WORKS & SCORING RULES
# =========================================================
with tab3:
    st.subheader("ℹ️ System Architecture & Transparent Scoring Rules")
    st.markdown(
        """
        ### 📐 1. Placement Readiness 100-Point Rubric
        Unlike opaque 'black-box' models, this assistant calculates scores using a **6-factor transparent rubric**:

        | Category | Max Points | Formula / Rule | Why It Matters |
        | :--- | :---: | :--- | :--- |
        | **1. Academic Foundation (CGPA)** | **25 pts** | `(CGPA / 10.0) * 25` | Clears initial campus placement eligibility cutoffs. |
        | **2. Technical Projects** | **20 pts** | `10 pts` per project (max 20 pts) | Proves hands-on software building and debugging ability. |
        | **3. Internship Experience** | **20 pts** | `10 pts` per internship (max 20 pts) | Demonstrates industry exposure, Git workflow, and teamwork. |
        | **4. DSA & Coding Practice** | **15 pts** | `(Problems / 150) * 15` (max 15 pts) | Essential for clearing Online Coding Assessments (OAs). |
        | **5. Certifications & Hackathons**| **10 pts** | `5 pts` each (max 10 pts) | Shows initiative, continuous learning, and competitive building. |
        | **6. Core CS & Aptitude Level** | **10 pts** | `Level (1-5) * 2` (max 10 pts) | Required for round-1 aptitude tests and technical interviews. |

        ---

        ### 📄 2. Smart Resume Analyzer Scoring Formula
        The **Overall Resume Score (out of 100)** combines three transparent checks:
        - **50% Weight — Target Skill Match Rate:** Percentage of role-specific technical and soft skills present.
        - **25% Weight — Essential Section Completeness:** Checks for *Education, Skills, Projects, Experience,* and *Achievements* headings.
        - **25% Weight — Impact & Action Verbs:** Checks for strong engineering verbs (*Developed, Optimized, Built*) and quantified metrics (*30%, 500+ users*).
        """
    )


# =========================================================
# TAB 4: TEAM & CONTRIBUTIONS
# =========================================================
with tab4:
    st.subheader("👥 Project Team & Contribution Matrix")
    st.markdown(
        "This project was collaboratively engineered by our 3-member team. Each member took "
        "ownership of specific modules and pushed their work to the repository."
    )

    tcol1, tcol2 = st.columns(2, gap="medium")

    with tcol1:
        st.markdown(
            """
            #### 🛠️ Module Breakdown & Responsibilities
            - **Team Member 1 (Project Setup & Predictor Engine):**
              - Initialized project dependencies (`requirements.txt`, `.gitignore`).
              - Developed the 6-factor scoring engine, company tier simulator, and 4-week study roadmap (`predictor.py`).

            - **Team Member 2 (Smart Resume Analyzer & QA Testing):**
              - Built role presets, regex skill matcher, section detector, and action verb/metric scanner (`resume_analyzer.py`).
              - Created the automated unit test suite (`test_app.py`).

            - **Team Member 3 (Streamlit Frontend UI & Documentation):**
              - Engineered the interactive Streamlit dashboard (`app.py`), progress visualizers, and downloadable reports.
              - Authored complete project documentation (`README.md`).
            """
        )

    with tcol2:
        st.markdown(
            """
            #### 📊 Collaboration Highlights
            - **Modular Architecture:** UI (`app.py`) is cleanly separated from core calculation modules (`predictor.py`, `resume_analyzer.py`).
            - **Automated Verification:** Unit tests verify boundary conditions and scoring accuracy.
            - **Ethical Design:** Zero personal data collection and clear educational disclaimers throughout.
            """
        )
        st.info("💡 **Presentation Tip:** Show this tab during your project viva to highlight each team member's exact module ownership!")
