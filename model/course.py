class Course:
    def __init__(self, section, class_number, mode_of_instruction, course_title, satisfies, units,
                 type, days, times, instructor, location, dates, open_seats, notes, instructor_email):
        self.section = section
        self.class_number = class_number
        self.mode_of_instruction = mode_of_instruction
        self.course_title = course_title
        self.satisfies = satisfies
        self.units = units
        self.type = type
        self.days = days
        self.times = times
        self.instructor = instructor
        self.location = location
        self.dates = dates
        self.open_seats = open_seats
        self.notes = notes
        self.instructor_email = instructor_email

    def to_tuple(self):
        # Convert the object into a tuple for insertion into the database
        # Ensure that empty strings are replaced with `None` or valid defaults for numeric fields
        return (
            self.section,
            self.class_number,
            self.mode_of_instruction,
            self.course_title,
            self.satisfies,
            float(self.units) if self.units.strip() != "" else None,  # Convert to float or None
            self.type,
            self.days,
            self.times,
            self.instructor,
            self.location,
            self.dates,
            int(self.open_seats) if self.open_seats.strip() != "" else None,  # Convert to int or None
            self.notes,
            self.instructor_email
        )
