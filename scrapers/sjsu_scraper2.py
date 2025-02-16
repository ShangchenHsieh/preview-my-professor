from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the geckodriver executable
driver_path = "C:\\Users\\mickd\\PycharmProjects\\preview-my-professor\\drivers\\geckodriver.exe"

# Initialize the WebDriver using the specified path for geckodriver
service = Service(driver_path)
driver = webdriver.Firefox(service=service)

# Open the webpage
driver.get("https://www.sjsu.edu/classes/schedules/spring-2025.php")

# Wait for the Subject input field to become available
wait = WebDriverWait(driver, 20)

# Locate and click the 'Load Table' button using JavaScript
load_table_button = driver.find_element(By.ID, "btnLoadTable")
driver.execute_script("arguments[0].click();", load_table_button)

# Wait for the search input field to become available
search_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']")))

# Enter the search query
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
        instructor_name = columns[9].text
        mode_of_instruction = columns[2].text
        print(f"Course: {course_name}, Instructor: {instructor_name}, Mode of Instruction: {mode_of_instruction}")

# Close the driver
driver.quit()
