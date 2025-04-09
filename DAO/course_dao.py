from db_connection import DatabaseConnection  # Import the DatabaseConnection class
from model.course import Course
import psycopg2
from psycopg2 import errors


class CourseDAO:
    @staticmethod
    def insert_course(course: Course):
        cursor, conn = DatabaseConnection.get_connection()  # Get connection and cursor using the Singleton pattern

        if conn is not None:
            insert_query = """
            INSERT INTO courses (
                section, class_number, mode_of_instruction, course_title, satisfies, units,
                type, days, times, instructor, location, dates, open_seats, notes, instructor_email
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            try:
                cursor.execute(insert_query,
                               course.to_tuple())  # Assuming the `to_tuple()` method converts the course object to a tuple
                conn.commit()  # Commit the changes
            except psycopg2.errors.UniqueViolation as e:
                # Handle the case when a duplicate section is found
                print(f"Duplicate entry found for section {course.section}, skipping insertion.")
                conn.rollback()  # Rollback the transaction to avoid further issues
            except Exception as e:
                # Handle any other exceptions
                print(f"Error inserting course {course.section}: {e}")
                conn.rollback()  # Rollback on other errors
            finally:
                # Optional: Close cursor and connection if necessary
                # DatabaseConnection.close_connection()  # Uncomment this if needed
                pass
        else:
            print("Failed to connect to the database.")

    @staticmethod
    def get_unique_instructors():
        cursor, conn = DatabaseConnection.get_connection()

        if conn is not None:
            query = """
            SELECT DISTINCT instructor, instructor_email
            FROM courses
            WHERE instructor IS NOT NULL AND instructor != '';
            """
            try:
                cursor.execute(query)
                unique_instructors = cursor.fetchall()  # Fetch all unique instructors
                return unique_instructors
            except Exception as e:
                print(f"Error retrieving unique instructors: {e}")
                return []
        else:
            print("Failed to connect to the database.")
            return []