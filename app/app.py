from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from sqlalchemy.orm import Session
from database import get_db, SessionLocal 

app = Flask(__name__)
CORS(app)  

# Example Function to Fetch User Transaction History
def get_professor_information(db: Session, email: str):
    result = db.execute(f"SELECT * FROM professors WHERE user_email = '{email}'").fetchall()
    return [dict(row) for row in result], 200
@cross_origin()
@app.route('/<email>', methods=['GET'])
def get_user_transaction_history_route(email: str):
    db = SessionLocal()
    try:
        professors = get_professor_information(db, email)
        return jsonify(professors)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close() 

if __name__ == '__main__':
    app.run(debug=True)
