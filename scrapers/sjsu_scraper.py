from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the geckodriver executable
driver_path = "C:\\Users\\mickd\\PycharmProjects\\preview-my-professor\\drivers\\geckodriver.exe"

# Initialize the WebDriver using the specified path for geckodriver
service = Service(driver_path)
driver = webdriver.Firefox(service=service)

# Open the new webpage
driver.get("https://cmsweb.cms.sjsu.edu/psp/CSJPRDF/EMPLOYEE/CSJPRD/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL?pslnkid=SJ_CLASS_SRCH_LNK")

# Wait for the Subject input field to become available
wait = WebDriverWait(driver, 20)

# Select the iframe that the textbox(s) exist on
driver.switch_to.frame("ptifrmtgtframe")

subject_field = wait.until(EC.presence_of_element_located((By.ID, "SSR_CLSRCH_WRK_SUBJECT$0")))

# Enter a subject (e.g., "CS")
subject_field.send_keys("CS")

# Wait for the Course Number input field to become available
course_number_field = wait.until(EC.presence_of_element_located((By.ID, "SSR_CLSRCH_WRK_CATALOG_NBR$1")))

# Enter a course number (e.g., "101")
course_number_field.send_keys("101")

# Wait for the Search button to be clickable
search_button = wait.until(EC.element_to_be_clickable((By.ID, "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH")))

# Click the Search button
search_button.click()

# Implement more webpage navigation and then the scraping below
