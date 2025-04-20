# from db_connection import DatabaseConnection  # Import the DatabaseConnection class
# import psycopg2
# from psycopg2 import errors
# from typing import List, Tuple
# import re
# class FlaskDAO:
#     @staticmethod
#     def get_professor_list(course: str):
#         """
#         _summary_: takes a course string and returns a list of professors, does regular expression and case conversion
#         _params_: course: str
#         _return_: List of professors in tuples -> [(P1,), (P2,), (P3,), ...]
#         """
#         cursor, conn = DatabaseConnection.get_connection()  # Get connection and cursor using the Singleton pattern
#         c = None
#         match = re.match(r"([A-Za-z]+)(\d+[A-Za-z]?)", course)
#         print({"match": match})
#         print({"course": course})
#         if match:
#             subject = match.group(1).upper()
#             class_number = match.group(2)
#             c = f"{subject} {class_number}"
#         else:
#             raise LookupError("No instructors found for the given section pattern.")
#
#         if conn is not None:
#             query = """
#             SELECT DISTINCT instructor FROM courses WHERE section LIKE %s
#             """
#             try:
#                 like_pattern = f"%{c}%"
#                 cursor.execute(query, (like_pattern,))
#                 result = cursor.fetchall()
#                 if result:
#                     return result
#                 else:
#                     raise LookupError("No instructors found for the given section pattern.")
#             finally:
#                 DatabaseConnection.close_connection()
#         else:
#             raise errors.DatabaseError("Connection to the database could not be established.")
#
#     @staticmethod
#     def get_reviews(prof_list: List[Tuple]):
#         """
#         _summary_: takes a list of professors and returns a list of reviews for each professor
#         _params_: prof_list: List of professors in tuples -> [(P1,), (P2,), (P3,), ...]
#         _return_: List of reviews in tuples -> [(P1, r1, r1, r1, r1, ...), (P2, r2, r2, r2, r2, r2, ...), ...]
#         """
#         cursor, conn = DatabaseConnection.get_connection()  # Get connection and cursor using the Singleton pattern
#         if conn:
#             try:
#                 query = """
#                 SELECT * FROM rmp_professor_info WHERE professor_name LIKE %s
#                 """
#                 res = []
#                 for prof in prof_list:
#                     cursor.execute(query, (prof[0],))
#                     result = cursor.fetchone()
#                     if result:
#                         res.append(result)
#                 return res
#             finally:
#                 DatabaseConnection.close_connection()
#         else:
#             raise errors.DatabaseError("Connection to the database could not be established.")

from db_connection import DatabaseConnection  # Import the DatabaseConnection class
import psycopg2
from psycopg2 import errors
from typing import List, Tuple, Dict
import re
import json


def get_clean_course_name(title: str) -> str:
    # This regex removes the course code and the section part
    cleaned_title = re.sub(r'\s?\(Section.*\)', '', title)  # Remove section part
    return cleaned_title.strip()

class FlaskDAO:
    @staticmethod
    def get_professor_list(course: str) -> List[Tuple]:
        """
        _summary_: Takes a course string and returns a list of professors, does regular expression and case conversion.
        _params_: course: str
        _return_: List of professors in tuples -> [(P1,), (P2,), (P3,), ...]
        """
        cursor, conn = DatabaseConnection.get_connection()  # Get connection and cursor using the Singleton pattern
        c = None
        match = re.match(r"([A-Za-z]+)\s*(\d+[A-Za-z]?)", course)
        print({"match": match})
        print({"course": course})
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
                like_pattern = f"%{c}%"  # Apply the like pattern
                cursor.execute(query, (like_pattern,))
                result = cursor.fetchall()
                if result:
                    return result  # Return list of professors
                else:
                    raise LookupError("No instructors found for the given section pattern.")
            finally:
                DatabaseConnection.close_connection()
        else:
            raise errors.DatabaseError("Connection to the database could not be established.")

    @staticmethod
    def get_reviews(prof_list: List[Tuple]):
        """
        _summary_: takes a list of professors and returns a list of reviews for each professor
        _params_: prof_list: List of professors in tuples -> [(P1,), (P2,), (P3,), ...]
        _return_: List of reviews in tuples -> [(P1, r1, r1, r1, r1, ...), (P2, r2, r2, r2, r2, r2, ...), ...]
        """
        cursor, conn = DatabaseConnection.get_connection()  # Get connection and cursor using the Singleton pattern
        if conn:
            try:
                query = """
                SELECT professor_name, rating, would_take_again, level_of_difficulty, comments
                FROM rmp_professor_info
                WHERE professor_name LIKE %s
                """
                res = []
                for prof in prof_list:
                    cursor.execute(query, (prof[0],))
                    result = cursor.fetchone()
                    if result:
                        # Add the result as a dictionary
                        review_dict = {
                            'professor_name': result[0],
                            'rating': result[1],
                            'would_take_again': result[2],
                            'level_of_difficulty': result[3],
                            #'comments': result[4]
                        }
                        res.append(review_dict)
                return res
            finally:
                DatabaseConnection.close_connection()
        else:
            raise errors.DatabaseError("Connection to the database could not be established.")




    # This is our workhorse that gets the job done queries->dict for the frontend
    @staticmethod
    def get_frontend_teachers(course: str) -> List[Dict]:
        """
        Returns a list of FrontEndTeacher dictionaries, each combining data from `courses`
        and `rmp_professor_info` tables.
        """
        cursor, conn = DatabaseConnection.get_connection()
        if not conn:
            raise errors.DatabaseError("Connection to the database could not be established.")

        try:
            # Step 1: Match and normalize the course string
            match = re.match(r"([A-Za-z]+)\s*(\d+[A-Za-z]?)", course.strip())
            if not match:
                raise LookupError("Invalid course format.")

            subject = match.group(1).upper()
            class_number = match.group(2).upper()
            normalized_course = f"{subject} {class_number}"
            like_pattern = f"%{normalized_course}%"

            # Step 2: Get all rows for the given course
            course_query = """
            SELECT instructor, instructor_email, section, course_title, times, location
            FROM courses
            WHERE section LIKE %s
            """
            cursor.execute(course_query, (like_pattern,))
            course_rows = cursor.fetchall()

            if not course_rows:
                raise LookupError(f"No courses found for the given course: {normalized_course}.")

            # Step 3: Group course info by instructor (email preferred)
            instructors = {}
            for row in course_rows:
                name, email, section, title, times, location = row
                key = email if email else name  # Use email if available, fallback to name

                course_name = get_clean_course_name(section)

                if key not in instructors:
                    instructors[key] = {
                        'name': name,
                        'email': email,
                        'course_name': f'({course_name} {title})',
                        'sections': [],
                        'rating': None,
                        'would_take_again': None,
                        'difficulty': None,
                        'tags': None,
                        'comments': None,
                        'rmp_page': None,
                        'department': None,
                        'total_ratings': None
                    }

                # Clean up the times field
                cleaned_times = " ".join(times.splitlines()).strip()

                # Group sections, times, and locations together in a dictionary
                section_info = {
                    'section': section,
                    'time': cleaned_times,
                    'location': location
                }

                instructors[key]['sections'].append(section_info)

            # Step 4: Fill in review info from RMP table
            rmp_query = """
            SELECT rating, would_take_again, level_of_difficulty, tags, comments, rmp_url, department, total_ratings
            FROM rmp_professor_info
            WHERE professor_email = %s OR professor_name = %s
            LIMIT 1
            """

            for key, info in instructors.items():
                cursor.execute(rmp_query, (info['email'], info['name']))
                result = cursor.fetchone()
                if result:
                    (
                        rating,
                        would_take_again,
                        difficulty,
                        tags,
                        comments,
                        rmp_url,
                        department,
                        total_ratings
                    ) = result

                    info['rating'] = rating
                    info['would_take_again'] = would_take_again
                    info['difficulty'] = difficulty
                    info['tags'] = tags
                    info['comments'] = comments
                    info['rmp_page'] = rmp_url
                    info['department'] = department
                    info['total_ratings'] = total_ratings

            return list(instructors.values())

        finally:
            DatabaseConnection.close_connection()


if __name__ == "__main__":
    test_course = "CS 122"  # Replace with a course code that exists in your DB

    try:
        frontend_teachers = FlaskDAO.get_frontend_teachers(test_course)
        print(f"\n[+] Found {len(frontend_teachers)} frontend teacher(s) for course '{test_course}':\n")

        for teacher in frontend_teachers:
            # Using json.dumps() to pretty-print the dictionary with key order intact
            print(json.dumps(teacher, indent=4, sort_keys=False))
            print("-" * 80)
    except Exception as e:
        print(f"[-] Error: {e}")
