from typing import List, Tuple
import random
import streamlit as st
import time

# Define skill categories
SKILL_CATEGORIES = {
    'Data Science': {
        'keywords': ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit'],
        'recommended_skills': [
            'Data Visualization', 'Predictive Analysis', 'Statistical Modeling','eda', 
            'Data Mining', 'Clustering & Classification', 'Data Analytics',
            'Quantitative Analysis', 'Web Scraping', 'ML Algorithms', 'Keras',
            'Pytorch', 'Probability', 'Scikit-learn', 'Tensorflow', 'Flask', 'Streamlit'
        ]
    },
    'Web Development': {
        'keywords': ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                    'javascript', 'angular js', 'c#', 'flask'],
        'recommended_skills': [
            'React', 'Django', 'Node JS', 'React JS', 'php', 'laravel', 
            'Magento', 'wordpress', 'Javascript', 'Angular JS', 'c#', 'Flask', 'SDK'
        ]
    },
    'Android Development': {
        'keywords': ['android','android development','flutter','kotlin','xml','kivy'],
        'recommended_skills': [
            'Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite'
        ]
    },
    'IOS app Development': {
        'keywords': ['ios','ios development','swift','cocoa','cocoa touch','xcode'],
        'recommended_skills': [
            'IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout'
        ]
    },
    'UI UX': {
        'keywords': ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience'],
        'recommended_skills': [
            'UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research'
        ]
    }
}

def analyze_skills(skills: List[str]) -> Tuple[str, List[str]]:
    """
    Analyze skills and return recommended field and skills
    
    Args:
        skills: List of skills from the resume
    
    Returns:
        Tuple of (recommended_field, recommended_skills)
    """
    user_skills_lower = [skill.lower() for skill in skills]
    
    for field, data in SKILL_CATEGORIES.items():
        # Check if any of the field's keywords are in the user's skills
        if any(keyword in user_skills_lower for keyword in data['keywords']):
            return field, data.get('recommended_skills', [])
    
    return "General", []

def determine_experience_level(resume_text: str) -> str:
    text = resume_text.lower()
    
    if any(keyword in text for keyword in ["intern", "fresher", "entry level", "beginner"]):
        return "Fresher"
    elif any(keyword in text for keyword in ["1 year", "2 years", "junior developer", "associate"]):
        return "Intermediate"
    elif any(keyword in text for keyword in ["3 years", "4 years", "5 years", "senior", "lead", "manager", "architect"]):
        return "Experienced"
    else:
        return "Unknown"


def analyze_resume(resume_text, resume_data, reco_field, cand_level, recommended_skills, rec_course, timestamp):
    """Analyze resume content and provide recommendations"""
    
    st.subheader("**Resume Tips & Ideas💡**")
    
    # Initialize resume score
    resume_score = 0
    
    # Check for Objective
    if 'Objective' in resume_text:
        resume_score += 20
        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Objective</h5>''', unsafe_allow_html=True)
    else:
        st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add your career objective</h5>''', unsafe_allow_html=True)

    # Check for Declaration
    if 'Experience' in resume_text:
        resume_score += 20
        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Declaration</h5>''', unsafe_allow_html=True)
    else:
        st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Declaration</h5>''', unsafe_allow_html=True)

    # Check for Hobbies or Interests (fixed the condition)
    if ('Hobbies' in resume_text) or ('Interests' in resume_text):
        resume_score += 20
        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Hobbies/Interests</h5>''', unsafe_allow_html=True)
    else:
        st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Hobbies/Interests</h5>''', unsafe_allow_html=True)

    # Check for Certifications
    if 'Certifications' in resume_text:
        resume_score += 20
        st.markdown('''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Achievements</h5>''', unsafe_allow_html=True)
    else:
        st.markdown('''<h5 style='text-align: left; color: #000000;'>[-] Please add Achievements</h5>''', unsafe_allow_html=True)

    # Check for Projects
    project_keywords = ["project", "projects", "project work", "personal project", "academic project"]
    if any(keyword.lower() in resume_text.lower() for keyword in project_keywords):
        resume_score += 20
        st.markdown(
        '''<h5 style='text-align: left; color: #1ed760;'>[+] Awesome! You have added Projects</h5>''',
        unsafe_allow_html=True
    )
    else:
        st.markdown(
        '''<h5 style='text-align: left; color: #e60000;'>[-] Projects section is missing. Try adding 1–2 projects with impact!</h5>''',
        unsafe_allow_html=True
    )

    # Display resume score with progress bar
    st.subheader("**Resume Score📝**")
    st.markdown(
        """
        <style>
            .stProgress > div > div > div > div {
                background-color: #d73b5c;
            }
        </style>""",
        unsafe_allow_html=True,
    )
    
    my_bar = st.progress(0)
    for percent_complete in range(resume_score):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)
    
    st.success(f'** Your Resume Writing Score: {resume_score}**')
    st.warning("** Note: This score is calculated based on the content that you have in your Resume. **")
    st.balloons()