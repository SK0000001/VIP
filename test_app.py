"""
test_app.py - Automated Verification Test Suite
----------------------------------------------
Tests the 6-factor calculation logic in predictor.py and the multi-layered
resume audit in resume_analyzer.py.
"""

from predictor import calculate_placement_readiness
from resume_analyzer import analyze_resume, parse_skills_input, ROLE_SKILL_PRESETS


def test_predictor():
    print("Testing advanced calculate_placement_readiness...")
    # Case 1: Perfect 100-point student profile
    res1 = calculate_placement_readiness(
        cgpa=10.0,
        internships=2,
        projects=2,
        dsa_problems=150,
        certifications=2,
        aptitude_level=5,
    )
    assert res1["total_score"] == 100.0, f"Expected 100.0, got {res1['total_score']}"
    assert res1["readiness_level"] == "High Placement Readiness"
    assert len(res1["company_tiers"]) == 3
    assert len(res1["roadmap"]) == 4

    # Case 2: Moderate student profile
    res2 = calculate_placement_readiness(
        cgpa=8.0,
        internships=1,
        projects=2,
        dsa_problems=75,
        certifications=1,
        aptitude_level=3,
    )
    assert res2["total_score"] == 68.5, f"Expected 68.5, got {res2['total_score']}"
    assert res2["readiness_level"] == "Moderate Placement Readiness"

    # Case 3: Beginner profile
    res3 = calculate_placement_readiness(
        cgpa=6.0, internships=0, projects=0, dsa_problems=0, certifications=0, aptitude_level=1
    )
    assert res3["total_score"] == 17.0, f"Expected 17.0, got {res3['total_score']}"
    assert res3["readiness_level"] == "Developing Placement Readiness"
    print("[OK] Advanced predictor tests passed successfully!")


def test_resume_analyzer():
    print("Testing advanced analyze_resume and role presets...")
    assert len(ROLE_SKILL_PRESETS) >= 5

    skills_str = "Python, Java, C++, SQL, Teamwork"
    parsed = parse_skills_input(skills_str)
    assert parsed == ["Python", "Java", "C++", "SQL", "Teamwork"]

    sample_text = """
    Alex Kumar
    Email: alex@university.edu | github.com/alex | linkedin.com/in/alex
    EDUCATION: B.Tech CS, CGPA 8.5
    SKILLS: Python, SQL, Git, Teamwork
    EXPERIENCE: Software Intern — Developed REST APIs and reduced latency by 30%.
    PROJECTS: Built a web application for 200+ users.
    ACHIEVEMENTS: Winner at Hackathon.
    """
    targets = ["Python", "Java", "SQL", "Git", "Teamwork", "Kubernetes"]
    result = analyze_resume(sample_text, targets)

    assert "Python" in result["matched_technical"]
    assert "Teamwork" in result["matched_soft"]
    assert "Java" in result["missing_technical"]
    assert result["matched_count"] == 4
    assert result["missing_count"] == 2
    assert result["sections_audit"]["Education"] is True
    assert result["sections_audit"]["Projects"] is True
    assert result["links_audit"]["Email Address"] is True
    assert result["links_audit"]["GitHub / Portfolio"] is True
    assert "Developed" in result["impact_audit"]["verbs_found"]
    assert len(result["impact_audit"]["metrics_found"]) >= 1
    print("[OK] Advanced resume analyzer tests passed successfully!")


if __name__ == "__main__":
    test_predictor()
    test_resume_analyzer()
    print("\n[SUCCESS] ALL ADVANCED TESTS PASSED SUCCESSFULLY!")
