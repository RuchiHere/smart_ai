import streamlit as st
import pandas as pd
import random
from datetime import datetime
from database.operations import initialize_database, insert_user_data, get_all_user_data
from pipelines.resume_parser import parse_resume, pdf_reader
from pipelines.skill_analyzer import analyze_skills, determine_experience_level, analyze_resume
from utils.file_handlers import show_pdf, save_uploaded_file, display_image
from utils.helpers import get_table_download_link, fetch_yt_video, get_timestamp
from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
from config.settings import APP_CONFIG
from database.models import UserData

# Initialize database safely
try:
    initialize_database()
except Exception as db_err:
    st.error(f"Database Initialization Failed: {db_err}")

def course_recommender(course_list):
    st.subheader("**Courses & Certificates Recommendations 🎓**")
    no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 5)
    random.shuffle(course_list)
    for i, (c_name, c_link) in enumerate(course_list[:no_of_reco], 1):
        st.markdown(f"({i}) [{c_name}]({c_link})")
    return [c[0] for c in course_list[:no_of_reco]]

def user_pipeline():
    st.markdown('''<h5 style='text-align: left; color: #021659;'> Upload your resume, and get smart recommendations</h5>''', unsafe_allow_html=True)
    
    pdf_file = st.file_uploader("Choose your Resume", type=["pdf", "docx"])  # Use only supported types
    if pdf_file is not None:
        save_path = APP_CONFIG['upload_folder'] + pdf_file.name
        save_uploaded_file(pdf_file, save_path)
        show_pdf(save_path)

        try:
            resume_info = parse_resume(save_path)
            resume_data = resume_info['data']
            resume_text = resume_info['text']

            # Display user info
            st.header("**Resume Analysis**")
            user_name = resume_data.get('name', 'Guest')
            st.success(f"Hello {user_name}")
            st.subheader("**Your Basic info**")
            st.text(f'Name: {resume_data.get("name", "Not found")}')
            st.text(f'Email: {resume_data.get("email", "Not found")}')
            st.text(f'Contact: {resume_data.get("mobile_number", "Not found")}')
            st.text(f'Resume pages: {resume_data.get("no_of_pages", "N/A")}')

            # Analyze skills & recommend courses
            cand_level = determine_experience_level(resume_data.get('no_of_pages', 1))
            reco_field, recommended_skills = analyze_skills(resume_data.get('skills', []))

            course_mapping = {
                'Data Science': ds_course,
                'Web Development': web_course,
                'Android Development': android_course,
                'IOS Courses': ios_course,
                'UI UX ': uiux_course
            }
            rec_course = course_recommender(course_mapping.get(reco_field, []))

            # Calculate resume score
            resume_score = analyze_resume(resume_text, cand_level, resume_data, reco_field, recommended_skills, get_timestamp, rec_course)

            # Save user data to DB
            user_data = UserData(
                name=resume_data.get('name', ''),
                email=resume_data.get('email', ''),
                resume_score=str(resume_score),
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                no_of_pages=str(resume_data.get('no_of_pages', 'N/A')),
                predicted_field=reco_field,
                user_level=cand_level,
                actual_skills=str(resume_data.get('skills', [])),
                recommended_skills=str(recommended_skills),
                recommended_courses=str(rec_course)
            )
            insert_user_data(user_data)

        except Exception as e:
            st.error(f'Error processing resume: {str(e)}')

def admin_pipeline():
    st.success('Welcome to Admin Side')
    ad_user = st.text_input("Username")
    ad_password = st.text_input("Password", type='password')
    
    if st.button('Login'):
        if ad_user == 'addy' and ad_password == 'addy123':
            st.success("Welcome Buddy!")
            display_admin_data()
        else:
            st.error("Wrong ID & Password Provided")

def display_admin_data():
    data = get_all_user_data()
    st.header("**User's Data**")
    
    # Convert data to DataFrame and display
    df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                                    'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
                                    'Recommended Course'])
    st.dataframe(df)
    st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)
    
    # Add any visualization code here if needed

def main():
    st.set_page_config(
        page_title=APP_CONFIG.get('page_title', "Hire Smart AI"),
        page_icon=APP_CONFIG.get('page_icon', ":robot:")
    )
    
