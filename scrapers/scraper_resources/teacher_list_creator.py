'''
The usage of this program is to extract a list of teachers to use in rmp_scraper.py

First check that within export_teachers that unique_instructors = a call to the proper table in which you are
attempting to recover the unique teachers.

For example:  unique_instructors = CourseDAO.get_unique_instructors_from_table("courses_fall_2025")
Here we are going to return all the unique instructors and their emails from the courses_fall_2025 table in our
database.

The teacher/email combination will be written to a file that is specified in the "if unique_instructors" portion.

The format will be as follows in this example:
A J Faas |001 aj.faas@sjsu.edu

Where |001 is interpreted as separator (when we use this file in rmp_scraper.py)
'''

from DAO.course_dao import CourseDAO

def export_teachers():
    unique_instructors = CourseDAO.get_unique_instructors_from_table("courses_fall_2025")
    unique_instructors.sort()

    if unique_instructors:
        with open("fall_2025/teacher_name_email_fall2025.txt", "w", encoding="utf-8") as file:
            for name, email in unique_instructors:
                file.write(f"{name} |001 {email}\n")

        print("Unique instructor list saved.")
    else:
        print("No instructors found.")

# Use this to query all unique teachers in the db and create a list with their name/email
export_teachers()

# def generate_teacher_names_only():
#     try:
#         with open("teacher_name_email.txt", "r", encoding="utf-8") as file:
#             lines = file.readlines()
#
#         # Extract only the instructor names (remove the email part)
#         teacher_names = [line.split(' (')[0] for line in lines]  # Split at ' (' and keep the first part (name)
#
#         # Write the names to a new file
#         with open("teacher_name_only.txt", "w", encoding="utf-8") as file:
#             for name in teacher_names:
#                 file.write(f"{name}\n")
#
#         print("Teacher names (without emails) saved to teacher_name_only.txt.")
#
#     except FileNotFoundError:
#         print("The file teacher_name_email.txt was not found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
#
# generate_teacher_names_only()
