"""
resume_analyzer.py - Advanced Resume Keyword, Structure & Impact Analyzer
-------------------------------------------------------------------------
This module provides transparent text analysis to evaluate pasted resume text:
1. Role-Based Target Skill Matching (Technical vs. Soft Skills).
2. Essential Resume Section Detection (Education, Projects, Experience, Skills, Achievements).
3. Contact & Portfolio Link Verification (Email, GitHub, LinkedIn).
4. Action Verb & Quantifiable Metric Detection (e.g., '20%', '100+ users').
5. Overall Resume Completeness & Match Score.

NOTE: This performs lexical pattern matching on the provided text. It does NOT
claim to verify experience authenticity or deep coding competency.
"""

import re
from typing import List, Dict

# Role-based skill presets for targeted resume screening
ROLE_SKILL_PRESETS = {
    "General Software Engineer (Default)": [
        "Python", "Java", "C++", "SQL", "Git", "Data Structures",
        "Algorithms", "Web Development", "Machine Learning", "REST APIs",
        "Communication", "Teamwork", "Problem Solving", "Leadership"
    ],
    "Full-Stack Web Developer": [
        "HTML", "CSS", "JavaScript", "React", "Node.js", "Python",
        "SQL", "MongoDB", "REST APIs", "Git", "Docker", "Responsive Design",
        "Communication", "Teamwork", "Agile", "Problem Solving"
    ],
    "Data Science & AI/ML Intern": [
        "Python", "SQL", "Machine Learning", "Pandas", "NumPy",
        "Scikit-Learn", "Data Visualization", "Statistics", "Deep Learning",
        "Git", "Jupyter", "Problem Solving", "Communication", "Analytical Thinking"
    ],
    "Core Backend & Systems Developer": [
        "Java", "C++", "Python", "Data Structures", "Algorithms", "SQL",
        "DBMS", "Operating Systems", "Computer Networks", "REST APIs",
        "Git", "Linux", "System Design", "Problem Solving", "Teamwork"
    ],
    "Cloud & DevOps Fresher": [
        "Linux", "AWS", "Docker", "Kubernetes", "Git", "CI/CD",
        "Python", "Bash", "Networking", "SQL", "Terraform",
        "Problem Solving", "Teamwork", "Communication"
    ]
}

DEFAULT_SKILLS = ROLE_SKILL_PRESETS["General Software Engineer (Default)"]

# Known soft skills for categorizing matched/missing skills
KNOWN_SOFT_SKILLS = {
    "communication", "teamwork", "problem solving", "leadership",
    "time management", "adaptability", "collaboration", "agile",
    "critical thinking", "analytical thinking", "presentation", "mentoring"
}

# Strong action verbs recommended for technical resumes
STRONG_ACTION_VERBS = [
    "architected", "automated", "built", "created", "deployed", "designed",
    "developed", "engineered", "enhanced", "established", "implemented",
    "improved", "integrated", "launched", "led", "migrated", "optimized",
    "reduced", "refactored", "resolved", "scaled", "spearheaded", "streamlined"
]

# Mandatory Resume Disclaimer
RESUME_DISCLAIMER = (
    "⚠️ Scope & Limitations Notice: This tool performs keyword, section, and pattern "
    "matching within the pasted text. It does NOT evaluate the depth of your knowledge, "
    "the truthfulness of your resume, or qualitative work experience."
)


def parse_skills_input(raw_skills_input: str) -> List[str]:
    """
    Parses a comma-separated or newline-separated string into a clean list of unique skills.
    Preserves original casing for display, trimmed of extra whitespace.
    """
    if not raw_skills_input or not raw_skills_input.strip():
        return []
    tokens = re.split(r"[,\n]+", raw_skills_input)
    seen = set()
    cleaned = []
    for token in tokens:
        item = token.strip()
        if item and item.lower() not in seen:
            seen.add(item.lower())
            cleaned.append(item)
    return cleaned


def analyze_resume(resume_text: str, target_skills: List[str]) -> Dict:
    """
    Performs a comprehensive multi-part audit of the pasted resume text.
    """
    if not resume_text or not resume_text.strip():
        return {
            "error": "Resume text is empty. Please paste your resume text to begin analysis."
        }

    if not target_skills:
        return {
            "error": "The skill list is empty. Please provide at least one target skill."
        }

    matched_skills = []
    missing_skills = []
    matched_technical = []
    matched_soft = []
    missing_technical = []
    missing_soft = []

    text_content = resume_text

    # 1. Match target skills using safe word-boundary regex
    for skill in target_skills:
        clean_skill = skill.strip()
        if not clean_skill:
            continue

        escaped_skill = re.escape(clean_skill)
        prefix = r"\b" if re.match(r"^\w", clean_skill) else r""
        suffix = r"\b" if re.search(r"\w$", clean_skill) else r""
        pattern = rf"{prefix}{escaped_skill}{suffix}"

        is_soft = clean_skill.lower() in KNOWN_SOFT_SKILLS

        if re.search(pattern, text_content, re.IGNORECASE):
            matched_skills.append(clean_skill)
            if is_soft:
                matched_soft.append(clean_skill)
            else:
                matched_technical.append(clean_skill)
        else:
            missing_skills.append(clean_skill)
            if is_soft:
                missing_soft.append(clean_skill)
            else:
                missing_technical.append(clean_skill)

    total_target = len(target_skills)
    matched_count = len(matched_skills)
    match_percentage = round((matched_count / total_target) * 100, 1) if total_target > 0 else 0.0

    # 2. Audit essential resume sections
    sections_audit = _audit_sections(text_content)
    sections_found_count = sum(1 for v in sections_audit.values() if v)
    section_score = round((sections_found_count / len(sections_audit)) * 100, 1)

    # 3. Audit contact & portfolio links
    links_audit = _audit_contact_and_links(text_content)

    # 4. Audit action verbs & measurable metrics
    impact_audit = _audit_impact_and_verbs(text_content)

    # 5. Calculate Overall Resume Readiness Score (Weighted heuristic)
    # 50% Skill Match + 25% Section Completeness + 25% Impact/Verbs
    impact_score = min(
        100.0,
        (min(5, len(impact_audit["verbs_found"])) / 5.0) * 60.0
        + (min(2, len(impact_audit["metrics_found"])) / 2.0) * 40.0,
    )
    overall_resume_score = round(
        (match_percentage * 0.50) + (section_score * 0.25) + (impact_score * 0.25), 1
    )

    # 6. Build tailored, actionable recommendations
    suggestions = []

    if match_percentage >= 75:
        suggestions.append(
            "🌟 Strong Keyword Alignment: Your resume covers most of the target skills for this role."
        )
    elif match_percentage >= 50:
        suggestions.append(
            "👍 Moderate Keyword Alignment: Over half of the target skills are present. "
            "Incorporate any missing technical skills into your project bullet points if you have used them."
        )
    else:
        suggestions.append(
            "⚠️ Low Keyword Coverage: Several key skills for this role were not found. "
            "Tailor your Skills and Projects sections to explicitly mention the tools and technologies you know."
        )

    missing_secs = [sec for sec, present in sections_audit.items() if not present]
    if missing_secs:
        suggestions.append(
            f"📑 Missing Standard Sections: Could not detect clear headings for: {', '.join(missing_secs)}. "
            "Adding standard section headers helps Applicant Tracking Systems (ATS) parse your resume."
        )

    if not links_audit["GitHub / Portfolio"]:
        suggestions.append(
            "🔗 Add GitHub / Portfolio Link: Include your GitHub profile or live project links so recruiters "
            "can verify your code."
        )

    if len(impact_audit["verbs_found"]) < 3:
        suggestions.append(
            "🎯 Strengthen Action Verbs: Start project bullets with strong verbs like 'Developed', 'Implemented', "
            "'Optimized', 'Automated', or 'Architected' instead of passive phrasing."
        )

    if len(impact_audit["metrics_found"]) == 0:
        suggestions.append(
            "📊 Quantify Your Impact: No measurable numbers or percentages were detected. Add concrete metrics "
            "(e.g., 'Reduced API response time by 25%', 'Built dataset of 1,000+ records', '92% accuracy')."
        )

    word_count = len(re.findall(r"\b\w+\b", text_content))
    if word_count < 80:
        suggestions.append(
            f"📝 Expand Content Depth: Your pasted text is quite brief ({word_count} words). A typical 1-page "
            "fresher resume contains 250–450 words detailing projects, tech stack, and outcomes."
        )

    return {
        "total_target_count": total_target,
        "matched_count": matched_count,
        "missing_count": len(missing_skills),
        "match_percentage": match_percentage,
        "overall_resume_score": overall_resume_score,
        "word_count": word_count,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_technical": matched_technical,
        "matched_soft": matched_soft,
        "missing_technical": missing_technical,
        "missing_soft": missing_soft,
        "sections_audit": sections_audit,
        "links_audit": links_audit,
        "impact_audit": impact_audit,
        "suggestions": suggestions,
        "disclaimer": RESUME_DISCLAIMER,
    }


def _audit_sections(text: str) -> Dict[str, bool]:
    """Checks for the presence of 5 essential resume sections."""
    return {
        "Education": bool(re.search(r"\b(education|university|college|b\.?tech|b\.?e|degree|cgpa|gpa)\b", text, re.I)),
        "Skills": bool(re.search(r"\b(skills|technologies|technical skills|languages|tools|frameworks)\b", text, re.I)),
        "Projects": bool(re.search(r"\b(projects|academic projects|personal projects|portfolio)\b", text, re.I)),
        "Experience / Internships": bool(re.search(r"\b(experience|internship|internships|intern|work history|employment)\b", text, re.I)),
        "Achievements / Certifications": bool(re.search(r"\b(achievements|certifications|certificates|awards|hackathon|honors)\b", text, re.I)),
    }


def _audit_contact_and_links(text: str) -> Dict[str, bool]:
    """Checks for email, phone, LinkedIn, and GitHub presence."""
    return {
        "Email Address": bool(re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)),
        "GitHub / Portfolio": bool(re.search(r"\b(github\.com|github|gitlab|portfolio|vercel\.app|netlify\.app|streamlit\.app)\b", text, re.I)),
        "LinkedIn Profile": bool(re.search(r"\b(linkedin\.com|linkedin)\b", text, re.I)),
    }


def _audit_impact_and_verbs(text: str) -> Dict[str, List[str]]:
    """Extracts strong action verbs and quantified numeric impact statements."""
    verbs_found = []
    for verb in STRONG_ACTION_VERBS:
        if re.search(rf"\b{re.escape(verb)}\b", text, re.IGNORECASE):
            verbs_found.append(verb.capitalize())

    # Find measurable metrics like "30%", "3x", "150+", "50ms", "500+ users"
    metrics_matches = re.findall(
        r"\b\d+(?:\.\d+)?\s*(?:%\s*|\+\s*(?:users|teams|records|queries|requests|projects|clients)?|(?:x|ms|users|records|queries|requests|hours|teams)\b)",
        text,
        re.IGNORECASE,
    )
    unique_metrics = list(dict.fromkeys([m.strip() for m in metrics_matches if m.strip()]))

    return {
        "verbs_found": verbs_found,
        "metrics_found": unique_metrics,
    }
