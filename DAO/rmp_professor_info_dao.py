from db_connection import DatabaseConnection  # Import the DatabaseConnection class
from model.professor import Professor  # Assuming you have a Professor model
import psycopg2
from psycopg2 import errors


class RMPProfessorInfoDAO:
    """
        Data Access Object (DAO) for inserting and updating RateMyProfessor (RMP) information for professors.
        """

    @staticmethod
    def insert_professor(professor: Professor):
        """
                Inserts or updates a professor's RMP information in the 'rmp_professor_info' table.

                If a row with the same professor_email already exists, it updates the existing record with
                the new values.

                Args:
                    professor (Professor): A Professor object containing all necessary fields, including:
                        - professor_email (str)
                        - professor_name (str)
                        - rmp_name (str)
                        - department (str or None)
                        - rating (float)
                        - total_ratings (int)
                        - would_take_again (float)
                        - level_of_difficulty (float)
                        - tags (list of str)
                        - comments (list of str)
                        - rmp_url (str or None)

                Notes:
                    - Converts Python lists to PostgreSQL array format for 'tags' and 'comments'.
                    - Uses 'ON CONFLICT' clause to update existing rows based on professor_email.
                    - Commits changes on success and rolls back on exceptions.
                """

        cursor, conn = DatabaseConnection.get_connection()

        if conn is not None:
            insert_query = """
                    INSERT INTO rmp_professor_info (
                        professor_email, professor_name, rmp_name, department, rating, total_ratings,
                        would_take_again, level_of_difficulty, tags, comments, rmp_url
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (professor_email) DO UPDATE SET
                        professor_name = EXCLUDED.professor_name,
                        rmp_name = EXCLUDED.rmp_name,
                        department = EXCLUDED.department,
                        rating = EXCLUDED.rating,
                        total_ratings = EXCLUDED.total_ratings,
                        would_take_again = EXCLUDED.would_take_again,
                        level_of_difficulty = EXCLUDED.level_of_difficulty,
                        tags = EXCLUDED.tags,
                        comments = EXCLUDED.comments,
                        rmp_url = EXCLUDED.rmp_url;
                """
            try:
                # Convert lists to PostgreSQL array format
                tags = "{" + ",".join([f'"{tag}"' for tag in professor.tags]) + "}" if professor.tags else "{}"
                comments = "{" + ",".join([f'"{comment.replace('"', '\\"')}"' for comment in
                                           professor.comments]) + "}" if professor.comments else "{}"
                rmp_url = professor.rmp_url if professor.rmp_url else None  # Handle URL insertion
                department = professor.department if professor.department else None  # Handle department insertion

                # Execute the insert query with adapted arrays for tags, comments, and URL
                cursor.execute(insert_query, (
                    professor.professor_email,
                    professor.professor_name,
                    professor.rmp_name,
                    department,
                    professor.rating,
                    professor.total_ratings,
                    professor.would_take_again,
                    professor.level_of_difficulty,
                    tags,
                    comments,
                    rmp_url
                ))

                # Check if row was inserted or updated
                if cursor.rowcount > 0:
                    print(
                        f"Insertion or update complete for professor: {professor.professor_name} ({professor.professor_email})")
                else:
                    print(f"No changes made for professor: {professor.professor_email} (possibly due to a conflict)")

                conn.commit()  # Commit the transaction after the operation

            except psycopg2.errors.UniqueViolation as e:
                # Handle the case when a duplicate email is found
                print(f"Duplicate entry found for professor email: {professor.professor_email}, skipping insertion...")
                conn.rollback()  # Rollback the transaction to avoid further issues
            except Exception as e:
                # Handle any other exceptions
                print(f"Error inserting professor {professor.professor_email}: {e}")
                conn.rollback()  # Rollback on other errors
            finally:
                # Optional: Close cursor and connection if necessary
                # DatabaseConnection.close_connection()  # Uncomment this if needed
                pass
        else:
            print("Failed to connect to the database.")
