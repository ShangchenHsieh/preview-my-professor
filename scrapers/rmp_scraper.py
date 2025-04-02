from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to the geckodriver executable
driver_path = "../drivers/geckodriver.exe"

# Initialize WebDriver
service = Service(driver_path)
driver = webdriver.Firefox(service=service)
wait = WebDriverWait(driver, 10)

# List of professor names
professors = ["Wendy Lee", "John Doe", "Jane Smith"]  # Replace with your list


def search_professor(professor_name):
    """Search for a professor on DuckDuckGo and click the RMP link."""
    driver.get("https://duckduckgo.com/")

    # Enter search query
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    query = f"{professor_name} San Jose State site:ratemyprofessors.com"
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Wait for search results to load
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a")))

    # Loop through search results to find the correct link
    while True:
        result_links = driver.find_elements(By.CSS_SELECTOR, "a")
        for link in result_links:
            try:
                link_text = link.text.strip()
                if "San Jose State University" in link_text and "Rate My Professors" in link_text:
                    print(f"Found link for {professor_name}: {link_text}")
                    link.click()
                    return True  # Successfully navigated to RMP
            except:
                continue
    return False  # No link found


def scrape_professor_data():
    """Scrape professor's rating and basic details."""
    try:
        time.sleep(2)  # Let page load (improve with better wait conditions)
        prof_name = driver.find_element(By.CLASS_NAME, "NameTitle__Name-dowf0z-0").text
        rating = driver.find_element(By.CLASS_NAME, "RatingValue__Numerator-qw8sqy-2").text
        print(f"Scraped: {prof_name} - Rating: {rating}")
    except Exception as e:
        print(f"Error scraping professor data: {e}")


# Loop through professors
for professor in professors:
    if search_professor(professor):  # Search and navigate to RMP
        scrape_professor_data()  # Scrape data
    driver.back()  # Go back to DuckDuckGo for next search

# Close browser
driver.quit()
