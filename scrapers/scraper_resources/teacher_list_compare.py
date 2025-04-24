'''
The purpose of this function is to compare two files of teacher names in the format as ex:
A J Faas |001 aj.faas@sjsu.edu
Aaron Freitas |001 aaron.freitas@sjsu.edu
Aaron Lington |001 aaron.lington@sjsu.edu
Aaron Miller |001 aaron.l.miller@sjsu.edu
Abbas Moallem |001 abbas.moallem@sjsu.edu
Abdulmelik Mohammed |001 abdulmelik.mohammed@sjsu.edu

The first parameter file is a list of teachers (most likely from a previous semester, or the file which has a
compiled list of the most teachers... see scraper_resources/compiled_lists/all_teachers_compiled.txt)

The second parameter file is a list of teachers (from a new semester, recently created by teacher_list_creator)

The third parameter is an output file including a path. This output file will be all the teachers that were found in
the second file that were not found in the first file.

The purpose of this process is to find teachers that may not have been scraped from RMP yet, and to create a
file which we can use in rmp_scraper.py. (a full scrape takes about 7-8hrs, ideally we only want to scrape teachers
which were not scraped yet to reduce scrape time).

It's also wise to add these new teachers to the scraper_resources/compiled_lists/all_teachers_compiled.txt file.
'''

def get_new_names_only_in_file2(file1_path, file2_path, output_path):
    with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
        lines_file1 = set(line.strip() for line in f1 if line.strip())  # Remove blank lines
        lines_file2 = [line.strip() for line in f2 if line.strip()]

    # Only keep lines from file2 that aren't in file1
    new_lines = [line for line in lines_file2 if line not in lines_file1]

    with open(output_path, 'w') as out:
        for line in new_lines:
            out.write(line + '\n')


get_new_names_only_in_file2("fall_2025/teacher_name_email_spring2025.txt",
                            "fall_2025/teacher_name_email_fall2025.txt",
                            "fall_2025/new_teachers_found_spring2025.txt")