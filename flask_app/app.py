from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import sys
import os
from psycopg2 import errors

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DAO.flask_dao import FlaskDAO

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

@cross_origin()
@app.route("/", methods=["GET", "POST"])
def index():
    instructors = []
    is_sample = False
    matched_course = None

    # Mapping semester selections to course tables
    semester_to_table = {
        'Spring 2025': 'courses',
        'Fall 2025': 'courses_fall_2025'
    }

    if request.method == "POST":
        # Get the semester from the form (use 'Fall 2025' only if not present)
        selected_semester = request.form.get('semester')
        if selected_semester not in semester_to_table:
            selected_semester = 'Fall 2025'

        selected_course_table = semester_to_table[selected_semester]
        class_number = request.form.get("class_number")
        print(f"Class number: {class_number}")

        try:
            instructors = FlaskDAO.get_frontend_teachers(class_number, selected_course_table)
            instructors = sorted(
                instructors,
                key=lambda x: float(x['would_take_again'].replace('%', '').strip()) if x['would_take_again'] not in [None, ''] else 0,
                reverse=True
            )

            if instructors:
                matched_course = instructors[0].get("course_name")

        except LookupError as e:
            print(f"No instructor found: {e}")
        except errors.DatabaseError as e:
            print(f"Database error: {e}")

    else:
        # First page load — show Spring 2025 sample, but default dropdown to Fall 2025
        selected_semester = 'Fall 2025'  # dropdown default
        sample_semester = 'Spring 2025'  # sample data source
        sample_table = semester_to_table[sample_semester]
        instructors = FlaskDAO.get_frontend_teachers("CS 122", sample_table)
        is_sample = True

        instructors = sorted(
            instructors,
            key=lambda x: float(x['would_take_again'].replace('%', '').strip()) if x['would_take_again'] not in [None, ''] else 0,
            reverse=True
        )

        if instructors:
            matched_course = instructors[0].get("course_name")

    return render_template("index.html",
                           instructors=instructors,
                           matched_course=matched_course,
                           is_sample=is_sample,
                           selected_semester=selected_semester,
                           semester_to_table=semester_to_table)



# @app.route("/test-frontend", methods=['GET'])
# def test_frontend():
#     results = [
#     {
#         "course": "CS 122 - Intro to Programming",
#         "section": "Section 01 • MWF 9:00–10:00AM • ENG 105",
#         "instructor": "Dr. Alice Smith",
#         "email": "alice.smith@sjsu.edu",
#         "rating": 4.7,
#         "take_again": "91%",
#         "difficulty": 2.3,
#         "tags": ["Caring", "Tough Grader"],
#         "comment": "Supportive and clear, but expects students to stay on top of assignments.",
#         "rmp_link": "https://ratemyprofessors.com/"
#     },
#     {
#         "course": "CS 146 - Data Structures & Algorithms",
#         "section": "Section 02 • TuTh 1:30–2:45PM • MH 225",
#         "instructor": "Prof. Brian Chen",
#         "email": "brian.chen@sjsu.edu",
#         "rating": 4.2,
#         "take_again": "88%",
#         "difficulty": 3.1,
#         "tags": ["Gives Good Feedback", "Lots of Homework"],
#         "comment": "Explains things well but workload is heavy.",
#         "rmp_link": "https://ratemyprofessors.com/"
#     },
#     {
#         "course": "CS 157A - Intro to Databases",
#         "section": "Section 03 • MW 10:30–11:45AM • ENG 210",
#         "instructor": "Dr. Kavita Rao",
#         "email": "kavita.rao@sjsu.edu",
#         "rating": 4.9,
#         "take_again": "97%",
#         "difficulty": 2.1,
#         "tags": ["Inspirational", "Amazing Lectures"],
#         "comment": "Makes databases fun! One of the best profs I've had.",
#         "rmp_link": "https://ratemyprofessors.com/"
#     },
#     {
#         "course": "CS 166 - Information Security",
#         "section": "Section 01 • F 12:00–2:45PM • ENG 140",
#         "instructor": "Prof. Michael Reyes",
#         "email": "michael.reyes@sjsu.edu",
#         "rating": 3.8,
#         "take_again": "74%",
#         "difficulty": 3.9,
#         "tags": ["Tough Grader", "Lecture Heavy"],
#         "comment": "Lectures are dense, but exams are fair if you keep up.",
#         "rmp_link": "https://ratemyprofessors.com/"
#     },
#     {
#         "course": "CS 185C - Machine Learning",
#         "section": "Section 01 • TuTh 3:00–4:15PM • BBC 302",
#         "instructor": "Dr. Priya Mehta",
#         "email": "priya.mehta@sjsu.edu",
#         "rating": 4.6,
#         "take_again": "89%",
#         "difficulty": 3.2,
#         "tags": ["Challenging", "Very Helpful"],
#         "comment": "Challenging course but incredibly rewarding with her guidance.",
#         "rmp_link": "https://ratemyprofessors.com/"
#     }
# ]
#
#     return render_template("index.html", posts=results)


# Flask app driver
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
