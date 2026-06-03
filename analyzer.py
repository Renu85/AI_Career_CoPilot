import re

def analyze_resume(resume_text):
    score = 0
    feedback = []

    # Check length
    if len(resume_text) > 500:
        score += 20
    else:
        feedback.append("Resume is too short.")

    # Check skills section
    if "skills" in resume_text.lower():
        score += 20
    else:
        feedback.append("Add a Skills section.")

    # Check education section
    if "education" in resume_text.lower():
        score += 20
    else:
        feedback.append("Add an Education section.")

    # Check experience section
    if "experience" in resume_text.lower():
        score += 20
    else:
        feedback.append("Add an Experience section.")

    # Check email
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    if re.search(email_pattern, resume_text):
        score += 20
    else:
        feedback.append("Add a valid email address.")

    return {
        "score": score,
        "feedback": feedback
    }