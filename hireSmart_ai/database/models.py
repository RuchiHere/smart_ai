from dataclasses import dataclass
from datetime import datetime

@dataclass
class UserData:
    name: str
    email: str
    resume_score: str
    timestamp: str
    no_of_pages: str
    predicted_field: str
    user_level: str
    actual_skills: str
    recommended_skills: str
    recommended_courses: str