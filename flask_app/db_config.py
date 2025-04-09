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


# def test_connection():
#     """Test the database connection by querying the version."""
#     cur, conn = get_cursor_and_connection()
#
#     if cur and conn:
#         try:
#             # Execute a simple query to check the connection
#             cur.execute("SELECT version();")
#             db_version = cur.fetchone()  # Fetch the result of the query
#             print(f"Connected to the database. Version: {db_version[0]}")
#         except Exception as e:
#             print("Error executing query:", e)
#         finally:
#             # Close the cursor and connection after the test
#             cur.close()
#             conn.close()
#     else:
#         print("Failed to connect to the database.")
#
#
# # Call the test connection function
# test_connection()

    


    