from db_connection import DatabaseConnection  # Import the DatabaseConnection class
from model.course import Course

class CourseDAO:
    @staticmethod
    def insert_course(course: Course):
        cursor, conn = DatabaseConnection.get_connection()  # Get connection and cursor using the Singleton pattern
        if conn is not None:
            insert_query = """
            INSERT INTO courses (
                section, class_number, mode_of_instruction, course_title, satisfies, units,
                type, days, times, instructor, location, dates, open_seats, notes
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """
            cursor.execute(insert_query, course.to_tuple())  # Assuming the `to_tuple()` method converts the course object to a tuple
            conn.commit()  # Commit the changes
            # The connection and cursor will be automatically handled by the DatabaseConnection class,
            # but make sure to close them when you're done
            # DatabaseConnection.close_connection()  # Close connection after operation
        else:
            print("Failed to connect to the database.")
