import streamlit as st
from utils import (
    extract_text_from_pdf,
    clean_text,
    get_similarity,
    get_keywords,
    skill_match,
    calculate_score,
    common_words  
)

st.set_page_config(page_title="AI Resume Screener", layout="centered")

st.title("📄 AI Resume Screener")
st.write("Analyze your resume against job descriptions using AI")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if uploaded_file and job_desc:

        # Extract & clean
        resume_text = extract_text_from_pdf(uploaded_file)
        resume_clean = clean_text(resume_text)
        job_clean = clean_text(job_desc)

        # Similarity score
        score = get_similarity(resume_clean, job_clean)

        # Skills
        matched, missing = skill_match(resume_clean, job_clean)

        # Keywords
        keywords = get_keywords(resume_clean)

        # 🔥 Score calculation (NEW)
        skill_score, final_score = calculate_score(
            len(matched),
            len(matched) + len(missing),
            score
        )

        common = common_words(resume_clean, job_clean)

        

        # 🎯 FINAL OUTPUT
        st.subheader(f"🎯 Final Score: {final_score}%")
        st.progress(int(final_score))

        st.write(f"Skill Match Score: {skill_score}%")
        st.write(f"Text Similarity Score: {score}%")
        st.subheader("🔗 Common Keywords")
        st.write(", ".join(common))

        # Skills display
        st.subheader("✅ Matched Skills")
        if matched:
            for skill in matched:
                st.write(f"✔️ {skill}")
        else:
            st.write("No matching skills found")

        st.subheader("❌ Missing Skills (Improve this!)")
        if missing:
            for skill in missing:
                st.write(f"❌ {skill}")
        else:
            st.write("You're a perfect match!")

        # Suggestions (🔥 NEW FEATURE)
        if missing:
            st.subheader("💡 Suggestions to Improve")
            for skill in missing[:5]:
                st.write(f"👉 Consider adding: {skill}")

        # Keywords
        st.subheader("📌 Resume Keywords")
        st.write(", ".join(keywords))

    else:
        st.warning("Please upload resume and enter job description")