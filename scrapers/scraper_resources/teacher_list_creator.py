from DAO.course_dao import CourseDAO

def export_teachers():
    unique_instructors = CourseDAO.get_unique_instructors()
    unique_instructors.sort()

    if unique_instructors:
        with open("teacher_name_email.txt", "w", encoding="utf-8") as file:
            for name, email in unique_instructors:
                file.write(f"{name} ({email})\n")

        print("Unique instructor list saved to teacher_name_email.txt.")
    else:
        print("No instructors found.")

# Use this to query all unique teachers in the db and create a list with their name/email
# export_teachers()

def generate_teacher_names_only():
    try:
        with open("teacher_name_email.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Extract only the instructor names (remove the email part)
        teacher_names = [line.split(' (')[0] for line in lines]  # Split at ' (' and keep the first part (name)

        # Write the names to a new file
        with open("teacher_name_only.txt", "w", encoding="utf-8") as file:
            for name in teacher_names:
                file.write(f"{name}\n")

        print("Teacher names (without emails) saved to teacher_name_only.txt.")

    except FileNotFoundError:
        print("The file teacher_name_email.txt was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


generate_teacher_names_only()
