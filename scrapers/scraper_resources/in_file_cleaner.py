def clean_course_list(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            clean_line = line.split(' - ')[0].strip()  # Keep only the part before " - "
            outfile.write(clean_line + '\n')

# Example usage
input_file = "test_list_dirty.txt"  # Update with your actual file name
output_file = "test_list_clean.txt"
clean_course_list(input_file, output_file)
print("Cleaning complete. Check test_list_clean.txt")

# Read cleaned course list and store as a list
with open("test_list_clean.txt", "r") as file:
    class_list = [line.strip() for line in file if line.strip()]

print(class_list)  # Verify the list