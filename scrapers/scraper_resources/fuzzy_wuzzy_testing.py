from fuzzywuzzy import fuzz


def test_fuzzy_match(name1, name2):
    """Test fuzzy match between two names and return the similarity score."""
    # Calculate the fuzzy matching score using fuzz.partial_ratio or fuzz.ratio
    score = fuzz.ratio(name1.lower(), name2.lower())  # Normalize to lowercase for better comparison
    print(f"Fuzzy matching score between '{name1}' and '{name2}': {score}")

    # You can also experiment with partial_ratio or token_sort_ratio
    partial_score = fuzz.partial_ratio(name1.lower(), name2.lower())
    print(f"Partial fuzzy matching score: {partial_score}")

    return score


# Test the method
name1 = "Jean-Benoit Levy"
name2 = "Jean Benoit Levy"
test_fuzzy_match(name1, name2)

name3 = "David Chai"
name4 = "Dave Chai"
test_fuzzy_match(name3, name4)


def fuzzy_match_name(name, link_text):
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

        print(f"Matching '{first_name} {middle_name}' to '{link_text}' with score: {first_middle_match}")
        print(f"Matching '{first_name} {last_name}' to '{link_text}' with score: {first_last_match}")

        # Define a threshold score for a valid match (e.g., 80)
        threshold = 80
        if first_middle_match >= threshold or first_last_match >= threshold:
            print("✅ Match found!")
            return True
        else:
            print("❌ No sufficient match.")
            return False
    else:
        # If the name doesn't contain three parts, don't proceed with fuzzy matching
        print("❌ Name is not 3 parts long.")
        return False


# Example usage
link_text = "Owen Aurelio at San Jose State University | Rate My Professors"
name = "Owen Matthew Aurelio"

fuzzy_match_name(name, link_text)