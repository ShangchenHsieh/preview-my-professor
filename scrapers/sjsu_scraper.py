# Basic model, was used for testing

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from db_connection import DatabaseConnection
from model.course import Course
from DAO.course_dao import CourseDAO

# Path to the geckodriver executable
driver_path = "../drivers/geckodriver.exe"

# Initialize the WebDriver using the specified path for geckodriver (firefox)
service = Service(driver_path)
driver = webdriver.Firefox(service=service)

# Open the webpage
driver.get("https://www.sjsu.edu/classes/schedules/spring-2025.php")

# Wait for the Subject input field to become available (wait for webpage load)
wait = WebDriverWait(driver, 20)

# Locate and click the 'Load Class Schedule' button using JavaScript
load_table_button = driver.find_element(By.ID, "btnLoadTable")
driver.execute_script("arguments[0].click();", load_table_button)

# Wait for the search input field to become available
search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']")))

# Enter the search query (we can automate this process and use a variable that contains classname)
search_input.send_keys("\"CS 158A\"")

# Submit the search
search_input.send_keys(Keys.RETURN)

# Wait for the table to load
wait.until(EC.presence_of_element_located((By.ID, "classSchedule")))

# Locate the table
table = driver.find_element(By.ID, "classSchedule")

# Extract table rows
rows = table.find_elements(By.TAG_NAME, "tr")

# Iterate through each row and extract data
for row in rows:
    columns = row.find_elements(By.TAG_NAME, "td")
    if columns:
        # Extract info from rows
        section = columns[0].text
        class_number = columns[1].text
        mode_of_instruction = columns[2].text
        course_title = columns[3].text
        satisfies = columns[4].text
        units = columns[5].text
        course_type = columns[6].text
        days = columns[7].text
        times = columns[8].text
        instructor_name = columns[9].text
        location = columns[10].text
        dates = columns[11].text
        open_seats = columns[12].text
        notes = columns[13].text


        # Create a Course object with the extracted data
        course_data = Course(
            section=section,
            class_number=class_number,
            mode_of_instruction=mode_of_instruction,
            course_title=course_title,
            satisfies=satisfies,
            units=units,
            type=course_type,
            days=days,
            times=times,
            instructor=instructor_name,
            location=location,
            dates=dates,
            open_seats=open_seats,
            notes=notes
        )

        # Insert the course data into the database
        CourseDAO.insert_course(course_data)


# Close db connection/driver (exit browser)
DatabaseConnection.close_connection()
driver.quit()
