import pymysql
from config.settings import DB_CONFIG
from database.models import UserData

def create_connection(db=None):
    config = DB_CONFIG.copy()
    if db:
        config['database'] = db
    return pymysql.connect(**config)

def initialize_database():
    try:
        # Step 1: Connect WITHOUT a database to create it
        connection = create_connection()
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS CV;")
        connection.commit()
        connection.close()

        # Step 2: Now connect TO the created database
        connection = create_connection(db='CV')
        with connection.cursor() as cursor:
            table_sql = """
            CREATE TABLE IF NOT EXISTS user_data (
                ID INT NOT NULL AUTO_INCREMENT,
                Name VARCHAR(500) NOT NULL,
                Email_ID VARCHAR(500) NOT NULL,
                resume_score VARCHAR(8) NOT NULL,
                Timestamp DATETIME NOT NULL,
                Page_no VARCHAR(5) NOT NULL,
                Predicted_Field TEXT NOT NULL,
                User_level TEXT NOT NULL,
                Actual_skills TEXT NOT NULL,
                Recommended_skills TEXT NOT NULL,
                Recommended_courses TEXT NOT NULL,
                PRIMARY KEY (ID)
            );
            """
            cursor.execute(table_sql)
        connection.commit()
    except Exception as e:
        print(f"Database Initialization Failed: {e}")
    finally:
        if connection:
            connection.close()

def insert_user_data(user_data: UserData):
    connection = create_connection(db='CV')
    try:
        with connection.cursor() as cursor:
            insert_sql = """
            INSERT INTO user_data 
            (Name, Email_ID, resume_score, Timestamp, Page_no, Predicted_Field, User_level, Actual_skills, Recommended_skills, Recommended_courses) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
    connection = create_connection(db='CV')
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_data")
            return cursor.fetchall()
    finally:
        connection.close()
