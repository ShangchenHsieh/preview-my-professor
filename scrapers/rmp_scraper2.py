# This is a backup of version that doesnt include department when storing the data, just in case department has issues

import re
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from fuzzywuzzy import fuzz

from DAO.rmp_professor_info_dao import RMPProfessorInfoDAO
from model.professor import Professor

# Path to the geckodriver executable
driver_path = "../drivers/geckodriver.exe"

# Initialize WebDriver with Firefox
service = Service(driver_path)
options = Options()
options.headless = False  # Set to True if you want to run headlessly
driver = webdriver.Firefox(service=service, options=options)


def scrape_professor_data(professor_name, professor_email):
    """Scrapes professor details from Rate My Professors."""
    try:
        time.sleep(5)  # Let the page load

        # Extract the professor's name from the RMP page
        try:
            rmp_name = driver.find_element(By.CLASS_NAME, "NameTitle__Name-dowf0z-0").text
        except:
            rmp_name = professor_name  # If we can't scrape it, default to passed name

        # Extract rating
        try:
            rating = driver.find_element(By.CLASS_NAME, "RatingValue__Numerator-qw8sqy-2").text
            if rating == "N/A":
                rating = "-1"  # Store -1 to show the teacher is not rated
        except:
            rating = ""  # Handle missing rating

        # Extract total ratings
        try:
            total_ratings = driver.find_element(By.CSS_SELECTOR, "a[href='#ratingsList']").text.split()[0]
        except:
            total_ratings = "0"

        # Extract 'Would Take Again' percentage and Difficulty
        try:
            feedback_numbers = driver.find_elements(By.CLASS_NAME, "FeedbackItem__FeedbackNumber-uof32n-1")
            would_take_again = feedback_numbers[0].text if len(feedback_numbers) > 0 else ""
            difficulty = feedback_numbers[1].text if len(feedback_numbers) > 1 else ""
        except:
            would_take_again = ""
            difficulty = ""

        # Extract professor tags
        tags = []
        try:
            tags_container = driver.find_element(By.CLASS_NAME, "TeacherTags__TagsContainer-sc-16vmh1y-0")
            tags = [tag.text for tag in tags_container.find_elements(By.CLASS_NAME, "Tag-bs9vf4-0")]
        except:
            print("No tags found for this professor.")

        # Extract comments (limit to first 10)
        comment_elements = driver.find_elements(By.CLASS_NAME, "Comments__StyledComments-dzzyvm-0")
        comments = [comment.text for comment in comment_elements[:10]]

        # Extract the current URL
        prof_url = driver.current_url

        # Store in dictionary
        professor_data = {
            "Professor Email": professor_email,
            "Professor Name": professor_name,  # Original search name
            "RMP Name": rmp_name,  # Name as listed on RMP
            "Rating": rating,
            "Total Ratings": total_ratings,
            "Would Take Again": would_take_again,
            "Level of Difficulty": difficulty,
            "Tags": tags,
            "Comments": comments,
            "URL": prof_url
        }

        print(professor_data)  # Debugging
        return professor_data

    except Exception as e:
        print(f"Error scraping professor data: {e}")
        return None


def normalize_name(name):
    """Normalize a name by removing punctuation and extra spaces."""
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", name)).strip().lower()


def contains_in_order(search_name, link_name):
    """Check if both the professor's name and 'San Jose' appear in order within the link name."""
    search_words = search_name.lower().split()
    link_name = link_name.lower()

    # Check if "San Jose" is in the link
    if "san jose" not in link_name:
        return False

    idx = 0
    for word in search_words:
        idx = link_name.find(word, idx)
        if idx == -1:
            return False
        idx += len(word)  # Move index forward to maintain order
    return True

def sanitize_link_text(link_text):
    """Remove everything after 'at San Jose State University | Rate My Professors' or 'at San Jose State University - Rate My Professors'."""
    # Check for the first possible match and split
    if " at San Jose State University | Rate My Professors" in link_text:
        sanitized_link_text = link_text.split(" at San Jose State University | Rate My Professors")[0].strip()
    # Check for the second possible match and split
    elif " at San Jose State University - Rate My Professors" in link_text:
        sanitized_link_text = link_text.split(" at San Jose State University - Rate My Professors")[0].strip()
    else:
        # If neither match is found, return the original link_text
        sanitized_link_text = link_text.strip()

    return sanitized_link_text

def fuzzy_match_name_3(name, link_text):
    """
    Attempts to match the name (first name, middle name, last name) with the link text using fuzzy matching.
    It first tries the first + middle name, then the first + last name.
    Returns True if any match is above a certain threshold.
    """
    # Split the name into parts (first, middle, last)
    name_parts = name.split()

    if len(name_parts) == 3:
        first_name = name_parts[0]
        middle_name = name_parts[1]
        last_name = name_parts[2]

        # Fuzzy match first + middle name to the link text
        first_middle_match = fuzz.partial_ratio(f"{first_name} {middle_name}", link_text)
        # Fuzzy match first + last name to the link text
        first_last_match = fuzz.partial_ratio(f"{first_name} {last_name}", link_text)

        # Define a threshold score for a valid match (e.g., 80)
        threshold = 90
        if first_middle_match >= threshold or first_last_match >= threshold:
            print("✅ 3 part match found.")
            return True

    # If no valid match is found
    return False

def check_link_match(professor_name, link_text):
    # San Jose and In Order Matching
    if contains_in_order(professor_name, link_text):
        print(f"✅ Contains in order match found: {link_text}")
        return True

    if "at San Jose State University | Rate My Professors" not in link_text and "at San Jose State University - Rate My Professors" not in link_text:
        print(f"❌ No \"San Jose State University part\": {link_text}")
        return False

    # Remove everything after "at San Jose State University | Rate My Professors"
    sanitized_link_text = sanitize_link_text(link_text)

    # Reverse Name Order Check (e.g., "Zepecki Carol" instead of "Carol Zepecki")
    professor_name_parts = professor_name.lower().split()
    link_text_parts = sanitized_link_text.lower().split()

    if len(professor_name_parts) == 2 and len(link_text_parts) == 2:
        # Compare the reverse order of name
        if professor_name_parts[1] == link_text_parts[0] and professor_name_parts[0] == link_text_parts[1]:
            print(f"✅ Reversed name order match found: {link_text}")
            return True

    if fuzzy_match_name_3(professor_name, link_text):
        return True

    # Fuzzy Matching as a Last Resort (if nothing else matches)
    if fuzz.partial_ratio(professor_name.lower(), link_text.lower()) > 90:  # Threshold can be adjusted
        print(f"✅ Fuzzy match found: {link_text}")
        return True




    # print(f"❌ No match found for: {link_text}")
    return False



def search_and_scrape(professors):
    """Searches for each professor on DuckDuckGo, navigates to RMP, scrapes data, and repeats."""

    driver.get("https://duckduckgo.com/")
    wait = WebDriverWait(driver, 10)

    all_data = {}

    for professor_name, professor_email in professors:
        print(f"\n🔎 Searching for {professor_name}, with email: {professor_email}...")
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.clear()

        query = f"{professor_name} San Jose State site:ratemyprofessors.com"
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2 a")))
        time.sleep(2)

        result_links = driver.find_elements(By.CSS_SELECTOR, "h2 a")

        found_match = False

        print("\n--- Search Results ---")
        for i, link in enumerate(result_links, 1):
            link_text = link.text.strip()
            link_url = link.get_attribute('href')
            print(f"{i}. {link_text} - {link_url}")

        for link in result_links:
            link_text = link.text.strip()
            link_href = link.get_attribute("href")

            if check_link_match(professor_name, link_text):
                print(f"✅ Found matching link: {link_text}")
                time.sleep(1)

                try:
                    link.click()
                    found_match = True
                    time.sleep(3)

                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "NameTitle__Name-dowf0z-0")))

                    data = scrape_professor_data(professor_name, professor_email)
                    if data:
                        all_data[professor_name] = data

                        professor = Professor(
                            professor_email=professor_email,  # Include email
                            professor_name=data["Professor Name"],
                            rmp_name=data["RMP Name"],
                            rating=data["Rating"],
                            total_ratings=data["Total Ratings"],
                            would_take_again=data["Would Take Again"],
                            level_of_difficulty=data["Level of Difficulty"],
                            tags=data["Tags"],
                            comments=data["Comments"],
                            rmp_url=data["URL"]
                        )

                        RMPProfessorInfoDAO.insert_professor(professor)
                        driver.back()
                        time.sleep(2)
                        break
                except Exception as e:
                    print(f"❌ Error clicking link: {e}")

        if not found_match:
            print(f"⚠️ No matching link found for {professor_name}, skipping...")

    driver.quit()
    print("✅ Scraping complete!")


def load_professors_from_file(filename):
    """Reads professor names and emails from a file, returning a list of tuples (name, email)."""
    professors = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            # Split by the separator " |001 " to separate name and email
            parts = line.strip().split(" |001 ")
            if len(parts) == 2:
                name, email = parts
                professors.append((name.strip(), email.strip()))
            else:
                print(f"⚠️ Skipping malformed line: {line.strip()}")

    return professors



# --------------------------------------------- Main
# Load professors
professors_list = load_professors_from_file("scraper_resources/teacher_name_email.txt")

# # ----- Full Scrape
# start_time = time.time()
# # Keep track of time
# search_and_scrape(professors_list)
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"Scraping completed in {elapsed_time:.2f} seconds.")


# ----- Easy Resume (if errors, or any other reason a stop was needed)
# def resume_scraping(professors_list, start_name):
#     try:
#         # Find the index of the professor where we want to start scraping
#         start_index = next(i for i, name in enumerate(professors_list) if name == start_name)
#
#         # Slice the list to start from the professor after the specified one
#         professors_to_scrape = professors_list[start_index:]
#         search_and_scrape(professors_to_scrape)
#
#     except StopIteration:
#         print(f"Professor {start_name} not found in the list.")
#
# resume_scraping(professors_list, "A.J. Faas")

def resume_scraping(professors_list, start_name):
    try:
        # Find the index of the professor where we want to start scraping
        start_index = next(i for i, (name, _) in enumerate(professors_list) if name == start_name)

        # Slice the list to start from the professor after the specified one
        professors_to_scrape = professors_list[start_index + 1:]
        search_and_scrape(professors_to_scrape)

    except StopIteration:
        print(f"Professor {start_name} not found in the list.")


# Call resume_scraping with the list of professors and the name where to resume
resume_scraping(professors_list, "Lan Nguyen")