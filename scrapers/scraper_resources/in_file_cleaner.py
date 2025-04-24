'''
This function removes the course description from files where the format is
AFAM 152 - Black Feminisms
AFAM 155A - Triumphs and Trials of the Black Athlete in the U.S., 1850-1999
AFAM 155B - Triumphs and Trials of the Black Athlete in the U.S., 2000-Present
AFAM 156 - Black Women’s Writing
AFAM 157 - Race, Tech, and Global Futures
AFAM 158 - Race, Sport, Activism & Social Movements
AFAM 159 - The Racial Wealth Gap in America
AFAM 160 - Black Political Power in the US
AFAM 161 - Black Representations in Media and

and returns a file where:
AFAM 152
AFAM 155A
AFAM 155B
AFAM 156
AFAM 157
AFAM 158
AFAM 159
AFAM 160
AFAM 161

This is used for sjsu_scraper2 as a list where each course is searched in SJSUs course catalog database before storing in our
database.
'''

def clean_course_list(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            clean_line = line.split(' - ')[0].strip()  # Keep only the part before " - "
            outfile.write(clean_line + '\n')

# Example usage
input_file = "fall_2025/courses_with_description_fall2025.txt"
output_file = "fall_2025/courses_clean_fall2025.txt"
clean_course_list(input_file, output_file)
print("Cleaning complete.")

# # Read cleaned course list and store as a list
# with open("fast_list_clean.txt", "r") as file:
#     class_list = [line.strip() for line in file if line.strip()]
#
# print(class_list)  # Verify the list