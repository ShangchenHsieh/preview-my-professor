import psycopg2
import dotenv
import os

dotenv.load_dotenv()

# Get sensitive data from the .env file
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")


class DatabaseConnection:
    _connection = None
    _cursor = None

    @staticmethod
    def get_connection():
        """Get or create a database connection and cursor."""
        if DatabaseConnection._connection is None:
            try:
                # Establish a connection if one doesn't exist
                DatabaseConnection._connection = psycopg2.connect(
                    host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT
                )
                DatabaseConnection._cursor = DatabaseConnection._connection.cursor()
                print("Database connection established.")
            except Exception as e:
                print(f"Error establishing connection: {e}")
        return DatabaseConnection._cursor, DatabaseConnection._connection

    @staticmethod
    def close_connection():
        """Close the cursor and connection."""
        if DatabaseConnection._cursor:
            try:
                DatabaseConnection._cursor.close()
                print("Cursor closed.")
            except Exception as e:
                print(f"Error closing cursor: {e}")
        if DatabaseConnection._connection:
            try:
                DatabaseConnection._connection.close()
                print("Connection closed.")
            except Exception as e:
                print(f"Error closing connection: {e}")
            # Reset static variables so connection is re-established when needed again
            DatabaseConnection._cursor = None
            DatabaseConnection._connection = None


# Usage example (to be done in your other code):
# cursor, connection = DatabaseConnection.get_connection()

# Don't forget to close the connection when done
# DatabaseConnection.close_connection()
