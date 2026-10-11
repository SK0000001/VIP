# 🎓 Placement Readiness Assistant (Advanced Edition)

A comprehensive, beginner-friendly web application built with **Python** and **Streamlit** for college students preparing for campus placement drives.

Designed as an academic classroom project, this tool provides **100% transparent, rule-based self-assessment** and **multi-layered resume auditing** without opaque "black-box" models or unverified claims.

---

## 🌟 Advanced Features Overview

### 1. 📊 Multi-Dimensional Placement Readiness Predictor
- **6-Factor Input Profile:**
  1. **CGPA** (0.0 to 10.0 scale)
  2. **Technical Projects Built**
  3. **Internships Completed**
  4. **DSA / Coding Problems Solved** (LeetCode / GFG / HackerRank)
  5. **Certifications & Hackathons**
  6. **Core CS (DBMS, OS, CN) & Aptitude Preparation Level** (1–5 scale)
- **Visual Point Breakdown:** Individual progress bars showing points earned in all 6 categories out of 100.
- **🏢 Company Tier Eligibility Simulator:**
  - Evaluates readiness across **3 campus recruitment categories**:
    - *IT Services & Mass Recruiters*
    - *Mid-Tier Product & FinTech Companies*
    - *Top-Tier Product Companies*
- **🗓️ Personalized 4-Week Action Plan:**
  - Automatically generates a customized 4-week study sprint targeting the student's specific gaps.
- **📥 Downloadable Readiness Report:**
  - Export a `.txt` summary of scores and recommendations in one click.

### 2. 📄 Smart Resume & ATS Analyzer
- **🎯 Role-Based Skill Presets (Editable):**
  - Switch between 5 industry presets (*General Software Engineer, Full-Stack Web Developer, Data Science & AI/ML, Core Backend & Systems, Cloud & DevOps*) or customize your own skill list.
- **Categorized Skill Matching:**
  - Separates matched and missing keywords into **Technical Skills** vs. **Soft & Professional Skills** using safe word-boundary regular expressions.
- **📑 Essential Resume Section Detector:**
  - Audits whether the resume includes *Education, Skills, Projects, Experience/Internships,* and *Achievements/Certifications*.
- **🔗 Contact & Portfolio Link Checker:**
  - Verifies presence of *Email Address, GitHub/Portfolio Link,* and *LinkedIn Profile*.
- **⚡ Action Verb & Quantified Impact Scanner:**
  - Detects strong engineering action verbs (*Developed, Implemented, Optimized, Built*) and measurable metrics (*30%, 500+ users*).
- **📥 Downloadable Resume Audit Report:**
  - Export the complete resume audit as a `.txt` file.

---

## 📐 Transparent Scoring Rules & Formulas

### 1. Placement Readiness Score (100 Points Total)

| Component | Max Points | Calculation Rule | Rationale |
| :--- | :---: | :--- | :--- |
| **1. Academic Foundation (CGPA)** | **25 pts** | `(CGPA / 10.0) * 25` | Clears initial campus eligibility screening cutoffs. |
| **2. Technical Projects** | **20 pts** | `10 pts` per project (max 20) | Demonstrates hands-on software building and problem-solving. |
| **3. Internship Experience** | **20 pts** | `10 pts` per internship (max 20) | Demonstrates real-world teamwork and industry workflows. |
| **4. DSA & Coding Practice** | **15 pts** | `(Problems / 150) * 15` (max 15) | Required for clearing Online Coding Assessments (OAs). |
| **5. Certifications & Hackathons**| **10 pts** | `5 pts` each (max 10) | Shows continuous learning and competitive building. |
| **6. Core CS & Aptitude Level** | **10 pts** | `Level (1–5) * 2` (max 10) | Essential for round-1 aptitude tests and technical interviews. |

### 2. Overall Resume Score (100 Points Total)
- **50% Weight:** Target Skill Match Percentage
- **25% Weight:** Standard Section Completeness (5 core sections)
- **25% Weight:** Action Verbs & Quantified Metrics Presence

---

## 🚀 Setup and Run Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
