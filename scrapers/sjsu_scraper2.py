from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

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
search_input.send_keys("CS 122")

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
        # Extract and print the desired information
        course_name = columns[0].text
        stripped_course = re.sub(r"\s*\(.*\)", "", course_name)
        # We have course here, we want to store this as a dictionary key maybe and the teachers
        # after the name?

        instructor_name = columns[9].text
        stripped_instructor = instructor_name.split(" / ")[0]
        # insert instructor to the db

        mode_of_instruction = columns[2].text

        # -------database insertion could happen here--------
        print(f"Course: {stripped_course}, Instructor: {stripped_instructor}, Mode of Instruction: {mode_of_instruction}")

# Close the driver a.k.a. exit browser
driver.quit()

# we are going to want to add some output cleaning of the names, remove , / etc.
# we should design an object to hold all the information so we can move it around easily if needed.