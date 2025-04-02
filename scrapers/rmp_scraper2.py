from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Path to the geckodriver executable
driver_path = "../drivers/geckodriver.exe"

# Initialize WebDriver
service = Service(driver_path)
driver = webdriver.Firefox(service=service)


def scrape_professor_data(professor_name):
    """Scrapes professor details from Rate My Professors."""
    try:
        time.sleep(2)  # Let the page load

        # Extract professor's name
        prof_name = driver.find_element(By.CLASS_NAME, "NameTitle__Name-dowf0z-0").text

        # Extract rating
        rating = driver.find_element(By.CLASS_NAME, "RatingValue__Numerator-qw8sqy-2").text

        # Extract total ratings
        total_ratings = driver.find_element(By.CSS_SELECTOR, "a[href='#ratingsList']").text.split()[0]

        # Extract 'Would Take Again' percentage
        feedback_numbers = driver.find_elements(By.CLASS_NAME, "FeedbackItem__FeedbackNumber-uof32n-1")
        would_take_again = feedback_numbers[0].text if len(feedback_numbers) > 0 else "N/A"
        difficulty = feedback_numbers[1].text if len(feedback_numbers) > 1 else "N/A"

        # Extract comments (limit to first 3)
        comment_elements = driver.find_elements(By.CLASS_NAME, "Comments__StyledComments-dzzyvm-0")
        comments = [comment.text for comment in comment_elements[:3]]  # Store first 3 comments

        # Store in dictionary
        professor_data = {
            "Professor Name": professor_name,
            "Rating": rating,
            "Total Ratings": total_ratings,
            "Would Take Again": would_take_again,
            "Level of Difficulty": difficulty,
            "Comments": comments
        }

        print(professor_data)  # Debugging
        return professor_data

    except Exception as e:
        print(f"Error scraping professor data: {e}")
        return None


def search_and_scrape(professors):
    """Searches for each professor on DuckDuckGo, navigates to RMP, scrapes data, and repeats."""
    all_data = {}

    for professor_name in professors:
        print(f"Searching for {professor_name}...")
        driver.get("https://duckduckgo.com/")
        wait = WebDriverWait(driver, 10)

        # Locate search bar and enter query
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))

        # Clear the search box to avoid reusing the previous query
        search_box.clear()

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

                            # Scrape data
                            data = scrape_professor_data(professor_name)
                            if data:
                                all_data[professor_name] = data

                            # Go back to DuckDuckGo for next search
                            driver.back()
                            time.sleep(2)  # Small delay before next search
                            break  # Exit the loop for links after scraping data

                    except Exception as e:
                        print(f"Error while trying to click link: {e}")
                        continue  # Ignore stale element issues and retry
                break  # Break out of the 'while' loop after one valid professor link is processed

        except Exception as e:
            print(f"Error navigating to RMP page: {e}")

    # Save results to JSON file
    with open("professor_data.json", "w") as f:
        json.dump(all_data, f, indent=4)

    print("Scraping complete!")
    driver.quit()


# Example usage
professors_list = ["Wendy Lee", "Rula Khayrallah", "Chao-Li Tarng"]
search_and_scrape(professors_list)
