import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_name TEXT UNIQUE,

        wave_type TEXT,

        sample_size INTEGER,

        survey_file TEXT,

        quota_file TEXT,

        created_date TEXT

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS question_mapping(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_name TEXT,

        awareness_question TEXT,

        consideration_question TEXT,

        purchase_question TEXT,

        usage_question TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uploads(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_name TEXT,

        upload_name TEXT,

        upload_date TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_project(project_name,
                wave_type,
                sample_size,
                survey_file,
                quota_file,
                created_date):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO projects

    (project_name,
    wave_type,
    sample_size,
    survey_file,
    quota_file,
    created_date)

    VALUES(?,?,?,?,?,?)

    """,(project_name,
         wave_type,
         sample_size,
         survey_file,
         quota_file,
         created_date))

    conn.commit()

    conn.close()


def get_projects():

    conn=get_connection()

    cursor=conn.cursor()

    cursor.execute("""

    SELECT project_name

    FROM projects

    ORDER BY project_name

    """)

    data=cursor.fetchall()

    conn.close()

    return [x[0] for x in data]

def save_question_mapping(project_name,
                          respondent_id,
                          duration,
                          awareness,
                          consideration,
                          purchase):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO question_mapping

    (
        project_name,
        awareness_question,
        consideration_question,
        purchase_question,
        usage_question
    )

    VALUES(?,?,?,?,?)

    """,(project_name,
         awareness,
         consideration,
         purchase,
         duration))

    conn.commit()

    conn.close()


def get_project(project_name):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM projects

    WHERE project_name=?

    """,(project_name,))

    row=cursor.fetchone()

    conn.close()

    return row