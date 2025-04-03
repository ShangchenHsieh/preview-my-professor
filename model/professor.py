class Professor:
    def __init__(self, professor_name, rating, total_ratings, would_take_again, level_of_difficulty, tags, comments):
        self.professor_name = professor_name
        self.rating = rating
        self.total_ratings = total_ratings
        self.would_take_again = would_take_again
        self.level_of_difficulty = level_of_difficulty
        self.tags = tags  # This will be a list of tags
        self.comments = comments  # This will be a list of comments

    def to_tuple(self):
        """
        Converts the professor object to a tuple that can be used in the SQL query.
        """
        # Convert list of tags and comments to a string, e.g., comma-separated
        tags_str = ", ".join(self.tags) if self.tags else None
        comments_str = " | ".join(self.comments) if self.comments else None

        return (
            self.professor_name,
            self.rating,
            self.total_ratings,
            self.would_take_again,
            self.level_of_difficulty,
            tags_str,  # Store tags as a comma-separated string
            comments_str  # Store comments as a pipe-separated string
        )

    def __repr__(self):
        return f"<Professor {self.professor_name}, Rating: {self.rating}, Total Ratings: {self.total_ratings}>"
