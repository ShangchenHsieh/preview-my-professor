import psycopg2
import dotenv
import os 

dotenv.load_dotenv()


# get sensitive data from the .env file
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")  
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")


def get_cursor_and_connection(): 
    """_summary_
        return the connection to the database 
    Returns:
        _type_: _description_
    """
    try: 
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
        )
        cur = conn.cursor()

    except Exception as e: 
        print("Error:", e)

    return cur, conn

    


    