class Professor:
    def __init__(self, professor_email, professor_name, rmp_name, department, rating, total_ratings, would_take_again, level_of_difficulty, tags, comments, rmp_url=None):
        self.professor_email = professor_email  # New primary key
        self.professor_name = professor_name  # The name as per the search
        self.rmp_name = rmp_name  # The name from Rate My Professors
        self.department = department
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
            self.professor_email,
            self.professor_name,
            self.rmp_name,
            self.department,
            self.rating,
            self.total_ratings,
            self.would_take_again,
            self.level_of_difficulty,
            tags_str,
            comments_str,
            self.rmp_url
        )

    def __repr__(self):
        class_name = type(self).__name__
        attributes = ', '.join(f"{key}={repr(value)}" for key, value in self.__dict__.items())
        return f"{class_name}({attributes})"