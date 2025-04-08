from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import os
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
        with open("app/default_prompt.txt") as file:
            return file.read()
    except Exception:
        return "Please provide a prompt."

@cross_origin()
@app.route("/", methods=["GET", "POST"])
def index():
    test = os.environ.get("TEST")
    if request.method == "POST":
        try: 
            cur, conn = db_config.connect_to_db()
            #
            #
            #
        except Exception as e:
            print("Error connecting to database:", e)
            return jsonify({"error": "Database connection error"}), 500
        finally: 
            cur.close()
            conn.close()

        return render_template("index.html", data=user_data)
    else: # GET request
        user_data = {
            "course_num": "",
            "result": "", 
        }
        
        return render_template("index.html", data={"test": test})


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
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()


# Flask app driver
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
