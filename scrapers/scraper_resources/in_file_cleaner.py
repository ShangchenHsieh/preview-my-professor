def clean_course_list(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            clean_line = line.split(' - ')[0].strip()  # Keep only the part before " - "
            outfile.write(clean_line + '\n')

# To use input the file with courses in format "AFAM 157 - Race, Tech, and Global Futures"
input_file = "fast_list_dirty.txt"
output_file = "fast_list_clean.txt"  # The output file will be in format "AFAM 157"
#clean_course_list(input_file, output_file) # Uncomment before running.
print("Cleaning complete. Check test_list_clean.txt")

# # Read cleaned course list and store as a list
# with open("fast_list_clean.txt", "r") as file:
#     class_list = [line.strip() for line in file if line.strip()]
#
# print(class_list)  # Verify the list