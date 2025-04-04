class Professor:
    def __init__(self, professor_email, professor_name, rmp_name, rating, total_ratings, would_take_again, level_of_difficulty, tags, comments, rmp_url=None):
        self.professor_email = professor_email  # New primary key
        self.professor_name = professor_name  # The name as per the search
        self.rmp_name = rmp_name  # The name from Rate My Professors
        self.rating = rating
        self.total_ratings = total_ratings
        self.would_take_again = would_take_again
        self.level_of_difficulty = level_of_difficulty
        self.tags = tags  # List of tags
        self.comments = comments  # List of comments
        self.rmp_url = rmp_url  # Store the RMP URL

    def to_tuple(self):
        """
        Converts the professor object to a tuple that can be used in the SQL query.
        """
        tags_str = ", ".join(self.tags) if self.tags else None
        comments_str = " | ".join(self.comments) if self.comments else None

        return (
            self.professor_email,  # Now first in tuple
            self.professor_name,
            self.rmp_name,
            self.rating,
            self.total_ratings,
            self.would_take_again,
            self.level_of_difficulty,
            tags_str,
            comments_str,
            self.rmp_url
        )

    def __repr__(self):
        return f"<Professor {self.professor_name}, Email: {self.professor_email}, RMP Name: {self.rmp_name}, Rating: {self.rating}, Total Ratings: {self.total_ratings}, URL: {self.rmp_url}>"
