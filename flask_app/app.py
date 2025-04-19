from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import sys
import os
from psycopg2 import errors
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

@cross_origin()
@app.route("/", methods=["GET", "POST"])
def index():
    test = os.environ.get("TEST")
    if request.method == "POST":
        class_number = request.form.get("class_number")
        try: 
            # 1st part 
            # get a list of professors teaching this class from the professor table 
            prof_list = FlaskDAO.get_professor_list(class_number)
            print(prof_list) # returns [('Prof. A',), ('Prof. B',)]

            # 2nd part 
            res = FlaskDAO.get_reviews(prof_list)
            print(res)

            # TODO: render to the frontend 

        except LookupError as e:
            print(f"No instructor found: {e}")
        except errors.DatabaseError as e: 
            print(f"Database error: {e}")
        return render_template("index.html", data=user_data)
    else: # GET request        
        return render_template("index.html", data=user_data)


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


# Flask app driver
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
