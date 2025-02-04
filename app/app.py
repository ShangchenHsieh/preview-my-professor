from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from sqlalchemy.orm import Session
from database import get_db, SessionLocal 

app = Flask(__name__)
CORS(app)  

# Example Function to Fetch User Transaction History
def get_user_transaction_history(db: Session, user_id: str):
    # Assuming a `transactions` table exists with a `user_id` column
    result = db.execute(f"SELECT * FROM transactions WHERE user_id = '{user_id}'").fetchall()
    return [dict(row) for row in result]  # Convert to list of dicts

@cross_origin()
@app.route('/<user_id>', methods=['GET'])
def get_user_transaction_history_route(user_id):
    db = SessionLocal()  # Open a new database session
    try:
        transactions = get_user_transaction_history(db, user_id)
        return jsonify(transactions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()  # Ensure session closes after request

if __name__ == '__main__':
    app.run(debug=True)
