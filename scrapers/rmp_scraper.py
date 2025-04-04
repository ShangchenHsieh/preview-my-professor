import re
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
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
        for link in result_links:
            link_text = link.text.strip()
            link_href = link.get_attribute("href")

            if contains_in_order(professor_name, link_text):
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

# ----- Full Scrape
start_time = time.time()
# Keep track of time
search_and_scrape(professors_list)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Scraping completed in {elapsed_time:.2f} seconds.")


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

# def resume_scraping(professors_list, start_name):
#     try:
#         # Find the index of the professor where we want to start scraping
#         start_index = next(i for i, (name, _) in enumerate(professors_list) if name == start_name)
#
#         # Slice the list to start from the professor after the specified one
#         professors_to_scrape = professors_list[start_index + 1:]
#         search_and_scrape(professors_to_scrape)
#
#     except StopIteration:
#         print(f"Professor {start_name} not found in the list.")
#
# # Load the professors from the file
# professors_list = load_professors_from_file("professors.txt")
#
# # Call resume_scraping with the list of professors and the name where to resume
# resume_scraping(professors_list, "A.J. Faas")