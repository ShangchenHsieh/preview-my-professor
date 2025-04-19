from db_connection import DatabaseConnection  # Import the DatabaseConnection class
import psycopg2
from psycopg2 import errors
from typing import List, Tuple
import re
class FlaskDAO:
    @staticmethod
    def get_professor_list(course: str):
        cursor, conn = DatabaseConnection.get_connection()  # Get connection and cursor using the Singleton pattern
        c = None
        match = re.match(r"([A-Za-z]+)(\d+[A-Za-z]?)", course)
        if match:
            subject = match.group(1).upper()  
            class_number = match.group(2)  
            c = f"{subject} {class_number}"
        else:
            raise LookupError("No instructors found for the given section pattern.")

        if conn is not None:
            query = """
            SELECT DISTINCT instructor FROM courses WHERE section LIKE %s
            """
            try:
                like_pattern = f"%{c}%"
                cursor.execute(query, (like_pattern,))
                result = cursor.fetchall()
                if result:
                    return result
                else:
                    raise LookupError("No instructors found for the given section pattern.")
            finally:
                DatabaseConnection.close_connection()  
        else:
            raise errors.DatabaseError("Connection to the database could not be established.")
        
    @staticmethod
    def get_reviews(prof_list: List[Tuple]): 
        cursor, conn = DatabaseConnection.get_connection()  # Get connection and cursor using the Singleton pattern
        if conn: 
            try: 
                query = """
                SELECT * FROM rmp_professor_info WHERE professor_name LIKE %s
                """
                res = []
                for prof in prof_list: 
                    cursor.execute(query, (prof[0],))
                    result = cursor.fetchone() 
                    if result: 
                        res.append(result)
                return res
            finally: 
                DatabaseConnection.close_connection()
        else: 
            raise errors.DatabaseError("Connection to the database could not be established.")
