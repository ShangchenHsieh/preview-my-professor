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

def sort_instructors(instructors):
    return sorted(
        instructors,
        key=lambda x: float(x['would_take_again'].replace('%', '').strip()) if x['would_take_again'] not in [None, '', 'N/A'] else 0,
        reverse=True
    )

@cross_origin()
@app.route("/", methods=["GET", "POST"])
def index():
    try:
        instructors = [] # Unused?
        is_sample = False
        matched_course = None

        semester_to_table = {
            'Spring 2025': 'courses',
            'Fall 2025': 'courses_fall_2025'
        }

        if request.method == "POST":
            selected_semester = request.form.get('semester')
            if selected_semester not in semester_to_table:
                selected_semester = 'Fall 2025'

            selected_course_table = semester_to_table[selected_semester]
            class_number = request.form.get("class_number")
            print(f"Class number: {class_number}")

            try:
                # Run the query inside a try block so any query errors are handled
                instructors = FlaskDAO.get_frontend_teachers(class_number, selected_course_table)
            except Exception as query_error:
                print(f"Query failed: {query_error}")
                instructors = []  # If query fails, set to empty list (frontend will display a message saying we didn't find anything)

            # Sort instructors if the query did not fail
            instructors = sort_instructors(instructors)

            if instructors:
                matched_course = instructors[0].get("course_name")

        else:
            # This is when a search hasn't been entered and we are displaying the sample search (spring cs 122)
            selected_semester = 'Fall 2025'
            sample_semester = 'Spring 2025'
            sample_table = semester_to_table[sample_semester]
            try:
                # Run the query inside a try block for the sample case as well
                instructors = FlaskDAO.get_frontend_teachers("CS 122", sample_table)
            except Exception as query_error:
                print(f"Query failed: {query_error}")
                instructors = []  # If query fails, set to empty list
            is_sample = True

            # Sort instructors if the query did not fail
            instructors = sort_instructors(instructors)

            if instructors:
                matched_course = instructors[0].get("course_name")

        # If no instructors are found, set a flag to show the custom message
        return render_template("index.html",
                               instructors=instructors,
                               matched_course=matched_course,
                               is_sample=is_sample,
                               selected_semester=selected_semester,
                               semester_to_table=semester_to_table,
                               no_results=len(instructors) == 0)

    # We caught some random error, display the error page so people don't see our internal server errors (less ugly)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Could do error logging here if we want
        return render_template("error.html"), 500



# Flask app driver
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
