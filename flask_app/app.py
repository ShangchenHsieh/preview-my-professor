from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import sys
import os
from psycopg2 import errors

from DAO import flask_dao

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DAO.flask_dao import FlaskDAO

import util
import db_config
import dotenv

#################
### Flask App ###
#################

# This is where we define the endpoints for our Flask application 
dotenv.load_dotenv()
# initialize the Flask app
app = Flask(__name__)
# enable CORS
CORS(app)  
app.secret_key = os.urandom(24)


user_data = {}

def load_default_prompt():
    try:
        with open("default_prompt.txt") as file:
            return file.read()
    except Exception:
        return "Please provide a prompt."

# @cross_origin()
# @app.route("/", methods=["GET", "POST"])
# def index():
#     test = os.environ.get("TEST")
#     if request.method == "POST":
#         class_number = request.form.get("class_number")
#         print(f"Class number: {class_number}")
#         try:
#             # 1st part
#             # get a list of professors teaching this class from the professor table
#             prof_list = FlaskDAO.get_professor_list(class_number)
#             print(prof_list) # returns [('Prof. A',), ('Prof. B',)]
#
#             # 2nd part
#             res = FlaskDAO.get_reviews(prof_list)
#             print(res)
#
#             # TODO: render to the frontend
#
#         except LookupError as e:
#             print(f"No instructor found: {e}")
#         except errors.DatabaseError as e:
#             print(f"Database error: {e}")
#         return render_template("index.html", data=user_data)
#     else: # GET request
#         return render_template("index.html", data=user_data)
@cross_origin()
@app.route("/", methods=["GET", "POST"])
def index():
    instructors = []  # Default to an empty list in case no instructors are found.

    if request.method == "POST":
        class_number = request.form.get("class_number")
        print(f"Class number: {class_number}")
        try:
            # Get instructors for the given class
            instructors = FlaskDAO.get_frontend_teachers(class_number)
            print(instructors)  # Will contain the instructors' data to be displayed

        except LookupError as e:
            print(f"No instructor found: {e}")
        except errors.DatabaseError as e:
            print(f"Database error: {e}")

    # Pass the instructors (even if it's an empty list) to the template
    return render_template("index.html", instructors=instructors)


@app.route("/test-db", methods=["GET"])
def test_db_connection():
    try:
        cur, conn = db_config.get_cursor_and_connection()
        cur.execute("""SELECT * FROM rmp_professor_info""")  # simple query to test connection
        result = cur.fetchall()
        print(result)
        return render_template("index.html", data={"test": result})
    except Exception as e:
        print("Database connection failed:", e)
        return render_template("index.html", data={"test": "Database connection failed"})
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

@app.route("/test-frontend", methods=['GET'])
def test_frontend():
    results = [
    {
        "course": "CS 122 - Intro to Programming",
        "section": "Section 01 • MWF 9:00–10:00AM • ENG 105",
        "instructor": "Dr. Alice Smith",
        "email": "alice.smith@sjsu.edu",
        "rating": 4.7,
        "take_again": "91%",
        "difficulty": 2.3,
        "tags": ["Caring", "Tough Grader"],
        "comment": "Supportive and clear, but expects students to stay on top of assignments.",
        "rmp_link": "https://ratemyprofessors.com/"
    },
    {
        "course": "CS 146 - Data Structures & Algorithms",
        "section": "Section 02 • TuTh 1:30–2:45PM • MH 225",
        "instructor": "Prof. Brian Chen",
        "email": "brian.chen@sjsu.edu",
        "rating": 4.2,
        "take_again": "88%",
        "difficulty": 3.1,
        "tags": ["Gives Good Feedback", "Lots of Homework"],
        "comment": "Explains things well but workload is heavy.",
        "rmp_link": "https://ratemyprofessors.com/"
    },
    {
        "course": "CS 157A - Intro to Databases",
        "section": "Section 03 • MW 10:30–11:45AM • ENG 210",
        "instructor": "Dr. Kavita Rao",
        "email": "kavita.rao@sjsu.edu",
        "rating": 4.9,
        "take_again": "97%",
        "difficulty": 2.1,
        "tags": ["Inspirational", "Amazing Lectures"],
        "comment": "Makes databases fun! One of the best profs I've had.",
        "rmp_link": "https://ratemyprofessors.com/"
    },
    {
        "course": "CS 166 - Information Security",
        "section": "Section 01 • F 12:00–2:45PM • ENG 140",
        "instructor": "Prof. Michael Reyes",
        "email": "michael.reyes@sjsu.edu",
        "rating": 3.8,
        "take_again": "74%",
        "difficulty": 3.9,
        "tags": ["Tough Grader", "Lecture Heavy"],
        "comment": "Lectures are dense, but exams are fair if you keep up.",
        "rmp_link": "https://ratemyprofessors.com/"
    },
    {
        "course": "CS 185C - Machine Learning",
        "section": "Section 01 • TuTh 3:00–4:15PM • BBC 302",
        "instructor": "Dr. Priya Mehta",
        "email": "priya.mehta@sjsu.edu",
        "rating": 4.6,
        "take_again": "89%",
        "difficulty": 3.2,
        "tags": ["Challenging", "Very Helpful"],
        "comment": "Challenging course but incredibly rewarding with her guidance.",
        "rmp_link": "https://ratemyprofessors.com/"
    }
]

    return render_template("index.html", posts=results)

@app.route("/api/teachers", methods=["GET"])
def get_teachers():
    course = request.args.get("course")
    if not course:
        return jsonify({"error": "Missing course parameter"}), 400

    try:
        teachers = flask_dao.FlaskDAO.get_frontend_teachers(course)
        return jsonify(teachers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask app driver
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
