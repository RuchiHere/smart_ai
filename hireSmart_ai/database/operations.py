import pymysql
from config.settings import DB_CONFIG
from database.models import UserData

def create_connection():
    return pymysql.connect(**DB_CONFIG)

def initialize_database():
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # Create DB if not exists
            cursor.execute("CREATE DATABASE IF NOT EXISTS CV;")
            
            # Create table
            table_sql = """
            CREATE TABLE IF NOT EXISTS user_data (
                ID INT NOT NULL AUTO_INCREMENT,
                Name varchar(500) NOT NULL,
                Email_ID VARCHAR(500) NOT NULL,
                resume_score VARCHAR(8) NOT NULL,
                Timestamp VARCHAR(50) NOT NULL,
                Page_no VARCHAR(5) NOT NULL,
                Predicted_Field BLOB NOT NULL,
                User_level BLOB NOT NULL,
                Actual_skills BLOB NOT NULL,
                Recommended_skills BLOB NOT NULL,
                Recommended_courses BLOB NOT NULL,
                PRIMARY KEY (ID)
            );
            """
            cursor.execute(table_sql)
        connection.commit()
    finally:
        connection.close()

def insert_user_data(user_data: UserData):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            insert_sql = """
            INSERT INTO user_data 
            VALUES (0, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_sql, (
                user_data.name,
                user_data.email,
                user_data.resume_score,
                user_data.timestamp,
                user_data.no_of_pages,
                user_data.predicted_field,
                user_data.user_level,
                user_data.actual_skills,
                user_data.recommended_skills,
                user_data.recommended_courses
            ))
        connection.commit()
    finally:
        connection.close()

def get_all_user_data():
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_data")
            return cursor.fetchall()
    finally:
        connection.close()