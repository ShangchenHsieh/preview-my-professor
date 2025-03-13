from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from openai import OpenAI  # Use the client class as shown in your example
import uuid
import os
import util

#################
### Flask App ###
#################
# This is where we define the endpoints for our Flask application 

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
        return "Please enter a prompt."

@app.route("/", methods=["GET", "POST"])
def index():
    user_data = {
            "course_num": "",
            "api_key": "",
            "model": "gpt-4o-mini",
            "prompt": load_default_prompt(),
            "result": "", 
            "summary": "",
        }
    return render_template("index.html", data=user_data)

@app.route("/set_api_key", methods=["GET", "POST"])
def set_api_key():
    data = user_data
    if request.method == "POST":
        api_key = request.form.get("api_key", "")
        selected_model = request.form.get("model", "")
        if api_key:
            user_data["api_key"] = api_key
            if selected_model:
                user_data["model"] = selected_model
            flash("API key and model updated successfully.", "success")
            return redirect(url_for("index"))
        else:
            flash("Please enter a valid API key.", "error")
    return render_template("set_api_key.html", data=data)

@app.route("/demo_url", methods=["GET", "POST"])
def demo_url():
    data = util.demo()
    data
    return render_template("index.html", data=data)

# Flask app driver
if __name__ == '__main__':
    app.run(debug=True)
