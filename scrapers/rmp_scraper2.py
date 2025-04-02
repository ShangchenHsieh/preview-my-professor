from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to the geckodriver executable
driver_path = "../drivers/geckodriver.exe"

# Initialize WebDriver
service = Service(driver_path)
driver = webdriver.Firefox(service=service)

def search_professor_on_duckduckgo(professor_name):
    """Searches for the professor on DuckDuckGo and clicks the RMP link."""
    driver.get("https://duckduckgo.com/")

    wait = WebDriverWait(driver, 10)

    # Locate search bar and enter query
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    query = f"{professor_name} San Jose State site:ratemyprofessors.com"
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a")))

    try:
        # Re-find elements before clicking to avoid stale reference error
        while True:
            result_links = driver.find_elements(By.CSS_SELECTOR, "a")
            for link in result_links:
                try:
                    link_text = link.text.strip()
                    if "San Jose State University" in link_text and "Rate My Professors" in link_text:
                        print(f"Found link: {link_text}")
                        link.click()  # Click the correct link
                        print("Navigated to RMP page!")
                        return  # Exit after successful navigation
                except:
                    continue  # Ignore any stale element issues and retry

    except Exception as e:
        print(f"Error navigating to RMP page: {e}")

# Example usage
search_professor_on_duckduckgo("Wendy Lee")

# Close browser
# driver.quit()
