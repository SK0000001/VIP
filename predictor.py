"""
predictor.py - Advanced Placement Readiness Calculation Engine
--------------------------------------------------------------
This module implements a transparent, multi-dimensional rule-based scoring
mechanism for assessing a student's campus placement readiness.

Features:
1. 6-Factor Readiness Rubric (CGPA, Projects, Internships, DSA Problems,
   Certifications/Hackathons, Core CS & Aptitude Readiness).
2. Company Tier Readiness Estimator (Service-Based, Mid-Tier Product, Top-Tier Product).
3. Personalized 4-Week Preparation Roadmap & Actionable Feedback.

NOTE: This is an educational classroom model designed to teach transparent heuristic
evaluation. It is not a scientifically validated hiring guarantee.
"""

from typing import Dict, List

# Mandatory Classroom Demo Disclaimer
CLASSROOM_DISCLAIMER = (
    "⚠️ Classroom Demo Notice: This readiness score and tier evaluation are educational "
    "simulations calculated using transparent classroom rules. They are not scientifically "
    "validated predictions and provide no guarantee of employment or placement."
)


def calculate_placement_readiness(
    cgpa: float,
    internships: int,
    projects: int,
    dsa_problems: int = 75,
    certifications: int = 1,
    aptitude_level: int = 3,
) -> Dict:
    """
    Calculate comprehensive placement readiness score out of 100 points.

    Weightage Breakdown (Total 100 points):
    1. Academic Foundation (CGPA): Up to 25 points ((cgpa / 10.0) * 25)
    2. Hands-on Projects: Up to 20 points (10 pts per project, max 2 major projects)
    3. Internship Experience: Up to 20 points (10 points per internship, max 2 internships)
    4. DSA & Problem Solving: Up to 15 points (scaled up to 150 problems solved)
    5. Certifications & Hackathons: Up to 10 points (5 points each, max 2)
    6. Core CS & Aptitude Prep (1-5 scale): Up to 10 points (aptitude_level * 2)
    """
    # 1. Clean & validate inputs within realistic bounds
    safe_cgpa = max(0.0, min(10.0, float(cgpa)))
    safe_internships = max(0, int(internships))
    safe_projects = max(0, int(projects))
    safe_dsa = max(0, int(dsa_problems))
    safe_certs = max(0, int(certifications))
    safe_aptitude = max(1, min(5, int(aptitude_level)))

    # 2. Calculate component scores (Total = 100 max)
    # Academic score: Max 25 points
    cgpa_score = round((safe_cgpa / 10.0) * 25.0, 1)

    # Project score: 10 points per project, capped at 20 points (2 major projects)
    project_score = float(min(20, safe_projects * 10))

    # Internship score: 10 points per internship, capped at 20 points (2 internships)
    internship_score = float(min(20, safe_internships * 10))

    # DSA / Coding problems solved: Scaled out of 150 problems for max 15 points
    dsa_score = round(min(15.0, (safe_dsa / 150.0) * 15.0), 1)

    # Certifications & Hackathons: 5 points each, capped at 10 points
    cert_score = float(min(10, safe_certs * 5))

    # Core CS (OS, DBMS, CN) & Aptitude Readiness: 2 points per level (1-5), max 10 points
    aptitude_score = float(safe_aptitude * 2)

    # Total score (capped at 100)
    total_score = round(
        min(
            100.0,
            cgpa_score + project_score + internship_score + dsa_score + cert_score + aptitude_score,
        ),
        1,
    )

    # 3. Categorize readiness level
    if total_score >= 80:
        readiness_level = "High Placement Readiness"
        level_color = "green"
        summary = "Strong multi-dimensional profile across academics, coding, projects, and practical experience."
    elif total_score >= 60:
        readiness_level = "Moderate Placement Readiness"
        level_color = "orange"
        summary = "Solid baseline profile. Targeted improvements in weak areas will significantly boost your readiness."
    else:
        readiness_level = "Developing Placement Readiness"
        level_color = "red"
        summary = "Early-stage preparation profile. Focus on building projects, solving DSA problems, and core fundamentals."

    # 4. Evaluate Company Tier Readiness (Educational Simulation)
    company_tiers = _evaluate_company_tiers(
        safe_cgpa, safe_projects, safe_internships, safe_dsa, safe_aptitude
    )

    # 5. Generate actionable suggestions
    suggestions = []

    if safe_cgpa < 6.5:
        suggestions.append(
            "📚 Academic Alert: Many campus drives enforce a 6.5 or 7.0 CGPA eligibility cutoff. "
            "Prioritize upcoming semester exams and emphasize strong project skills."
        )
    elif safe_cgpa < 7.5:
        suggestions.append(
            "📈 Good CGPA Baseline: You clear standard 6.5/7.0 cutoffs. Offset higher CGPA cutoffs by showcasing "
            "deployed projects and strong coding contest profiles."
        )
    else:
        suggestions.append(
            "⭐ Strong Academic Standing: Your CGPA clears initial screening filters for almost all campus recruiters."
        )

    if safe_projects < 2:
        suggestions.append(
            "🛠️ Portfolio Gap: Build at least 2 end-to-end projects (e.g., Full-Stack Web App, ML Pipeline, or API) "
            "hosted on GitHub with a live demo link."
        )
    else:
        suggestions.append(
            "🚀 Solid Project Count: Ensure you can explain system architecture, database schemas, and challenges "
            "for each project during technical interviews."
        )

    if safe_internships == 0:
        suggestions.append(
            "💼 Experience Gap: Pursue at least 1 internship, open-source program (GSoC, GirlScript, Hacktoberfest), "
            "or verified virtual internship to demonstrate industry workflow."
        )
    else:
        suggestions.append(
            "🏆 Industry Exposure: Prepare structured STAR (Situation, Task, Action, Result) stories highlighting "
            "your internship impact and team collaboration."
        )

    if safe_dsa < 50:
        suggestions.append(
            "💻 Coding Practice Needed: Aim to solve at least 100–150 curated problems covering Arrays, Strings, "
            "Trees, Graphs, and Dynamic Programming for online assessments (OAs)."
        )
    elif safe_dsa < 150:
        suggestions.append(
            "⚡ Good Coding Momentum: You have a foundation in DSA. Focus on timed mock Online Assessments "
            "and medium-level tree/graph/DP problems."
        )
    else:
        suggestions.append(
            "🔥 Strong DSA Practice: Great problem-solving volume! Focus on explaining time/space complexity "
            "(Big-O) out loud during mock interviews."
        )

    if safe_aptitude <= 2:
        suggestions.append(
            "🧠 Core CS & Aptitude: Dedicate daily time to Quantitative Aptitude, Logical Reasoning, and Core CS "
            "subjects (DBMS, Operating Systems, Computer Networks, OOPs)."
        )

    # 6. Generate 4-Week Personalized Study Plan
    roadmap = _generate_study_roadmap(safe_projects, safe_dsa, safe_internships, safe_aptitude)

    return {
        "total_score": total_score,
        "readiness_level": readiness_level,
        "level_color": level_color,
        "summary": summary,
        "breakdown": {
            "cgpa_points": cgpa_score,
            "max_cgpa_points": 25,
            "project_points": project_score,
            "max_project_points": 20,
            "internship_points": internship_score,
            "max_internship_points": 20,
            "dsa_points": dsa_score,
            "max_dsa_points": 15,
            "cert_points": cert_score,
            "max_cert_points": 10,
            "aptitude_points": aptitude_score,
            "max_aptitude_points": 10,
        },
        "company_tiers": company_tiers,
        "roadmap": roadmap,
        "suggestions": suggestions,
        "disclaimer": CLASSROOM_DISCLAIMER,
    }


def _evaluate_company_tiers(
    cgpa: float, projects: int, internships: int, dsa: int, aptitude: int
) -> List[Dict]:
    """
    Simulates readiness across 3 typical campus placement drive categories.
    """
    tiers = []

    # Tier 1: Mass / IT Service Recruiters
    if cgpa >= 6.0 and aptitude >= 3 and projects >= 1:
        t1_status = "✅ Ready"
        t1_note = "Meets typical CGPA (6.0+), aptitude, and foundational project expectations."
    elif cgpa >= 6.0:
        t1_status = "⚠️ Borderline"
        t1_note = "CGPA is eligible, but strengthen aptitude speed and finish at least 1 project."
    else:
        t1_status = "❌ Needs Work"
        t1_note = "Focus on raising CGPA toward 6.0+ and practicing aptitude tests."
    tiers.append({
        "tier": "🏢 IT Services & Mass Recruiters",
        "status": t1_status,
        "criteria": "CGPA ≥ 6.0 | Strong Aptitude | 1+ Project | Basic Coding",
        "note": t1_note,
    })

    # Tier 2: Mid-Tier Product & FinTech Companies
    if cgpa >= 7.0 and projects >= 2 and dsa >= 75 and aptitude >= 3:
        t2_status = "✅ Ready"
        t2_note = "Good balance of CGPA, DSA problem solving, and project portfolio."
    elif cgpa >= 6.5 and projects >= 1 and dsa >= 40:
        t2_status = "⚠️ Borderline"
        t2_note = "Push DSA count above 75+ problems and ensure 2 solid projects are deployed."
    else:
        t2_status = "❌ Needs Work"
        t2_note = "Requires stronger DSA practice (75+ problems), 2+ projects, and ~7.0+ CGPA."
    tiers.append({
        "tier": "🚀 Mid-Tier Product & FinTech",
        "status": t2_status,
        "criteria": "CGPA ≥ 7.0 | 75+ DSA Problems | 2+ Projects | Core CS",
        "note": t2_note,
    })

    # Tier 3: Top-Tier Product Companies
    if cgpa >= 7.5 and projects >= 2 and internships >= 1 and dsa >= 150 and aptitude >= 4:
        t3_status = "✅ Ready"
        t3_note = "Competitive profile for top product drives! Focus on mock interviews and system design."
    elif cgpa >= 7.0 and projects >= 2 and dsa >= 100:
        t3_status = "⚠️ Borderline"
        t3_note = "Close! Aim for 150+ DSA problems and highlight internship or open-source impact."
    else:
        t3_status = "❌ Needs Work"
        t3_note = "Typically expects 150+ DSA problems, 1+ internship, 2+ deep projects, and strong CS fundamentals."
    tiers.append({
        "tier": "🌟 Top-Tier Product Companies",
        "status": t3_status,
        "criteria": "CGPA ≥ 7.5 | 150+ DSA Problems | 1+ Internship | 2+ Projects",
        "note": t3_note,
    })

    return tiers


def _generate_study_roadmap(
    projects: int, dsa: int, internships: int, aptitude: int
) -> List[Dict]:
    """
    Creates a structured 4-week preparation plan tailored to the student's current profile.
    """
    week1 = (
        "Revise Arrays, Strings, HashMaps, and Two-Pointers (aim for 25 problems)."
        if dsa < 100
        else "Practice timed Medium/Hard Graph and Dynamic Programming problems."
    )
    week2 = (
        "Build and deploy a complete project on GitHub with README and live demo link."
        if projects < 2
        else "Refactor existing projects: add unit tests, architecture diagram, and performance metrics."
    )
    week3 = (
        "Master Core CS subjects (DBMS SQL queries, OS processes/threads, OOP principles) & daily aptitude tests."
        if aptitude <= 3
        else "Take 3 full-length timed Online Assessment (OA) mock tests (Aptitude + Coding)."
    )
    week4 = (
        "Apply to virtual internships / open-source issues and conduct 2 peer mock interviews."
        if internships == 0
        else "Prepare behavioral STAR stories for your internships and do 2 technical mock interviews."
    )

    return [
        {"week": "Week 1: Coding & DSA Sprint", "task": week1},
        {"week": "Week 2: Project & Portfolio Polish", "task": week2},
        {"week": "Week 3: Core CS & Aptitude Mastery", "task": week3},
        {"week": "Week 4: Mock Interviews & Applications", "task": week4},
    ]
