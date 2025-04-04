from db_connection import DatabaseConnection  # Import the DatabaseConnection class
from model.professor import Professor  # Assuming you have a Professor model
import psycopg2
from psycopg2 import errors


class RMPProfessorInfoDAO:
    @staticmethod
    def insert_professor(professor):
        cursor, conn = DatabaseConnection.get_connection()

        if conn is not None:
            insert_query = """
              INSERT INTO rmp_professor_info (
                  professor_email, professor_name, rmp_name, rating, total_ratings, would_take_again, level_of_difficulty, tags, comments, rmp_url
              ) VALUES (
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
              )
              ON CONFLICT (professor_email) DO UPDATE SET
                  professor_name = EXCLUDED.professor_name,
                  rmp_name = EXCLUDED.rmp_name,
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
                comments = "{" + ",".join([f'"{comment.replace('"', '\\"')}"' for comment in professor.comments]) + "}" if professor.comments else "{}"
                rmp_url = professor.rmp_url if professor.rmp_url else None  # Handle URL insertion

                # Execute the insert query with adapted arrays for tags, comments, and URL
                cursor.execute(insert_query, (
                    professor.professor_email,
                    professor.professor_name,
                    professor.rmp_name,
                    professor.rating,
                    professor.total_ratings,
                    professor.would_take_again,
                    professor.level_of_difficulty,
                    tags,
                    comments,
                    rmp_url
                ))

                conn.commit()  # Commit the transaction
                print(f"Insertion complete for professor: {professor.professor_name} ({professor.professor_email})")  # Success message

            except psycopg2.errors.UniqueViolation:
                print(f"Duplicate entry found for {professor.professor_email}, skipping insertion.")
                conn.rollback()
            except Exception as e:
                print(f"Error inserting professor {professor.professor_email}: {e}")
                conn.rollback()
            finally:
                pass  # Optional: Close cursor and connection if necessary
        else:
            print("Failed to connect to the database.")

    @staticmethod
    def get_professor_by_email(professor_email: str):
        cursor, conn = DatabaseConnection.get_connection()

        if conn is not None:
            query = """
            SELECT professor_email, professor_name, rmp_name, rating, total_ratings, would_take_again, level_of_difficulty, tags, comments, rmp_url
            FROM rmp_professor_info
            WHERE professor_email = %s;
            """
            try:
                cursor.execute(query, (professor_email,))
                professor_data = cursor.fetchone()  # Fetch the professor data
                return professor_data
            except Exception as e:
                print(f"Error retrieving professor data: {e}")
                return None
        else:
            print("Failed to connect to the database.")
            return None

    @staticmethod
    def get_all_professors():
        """Fetch all professors from the database and return as a dictionary indexed by email."""
        cursor, conn = DatabaseConnection.get_connection()

        if conn is not None:
            query = "SELECT professor_email, professor_name, rmp_name, rmp_url FROM rmp_professor_info;"
            try:
                cursor.execute(query)
                professors = {
                    row[0]: {"professor_name": row[1], "rmp_name": row[2], "rmp_url": row[3]}
                    for row in cursor.fetchall()
                }
                return professors
            except Exception as e:
                print(f"Error retrieving professor data: {e}")
                return {}
        else:
            print("Failed to connect to the database.")
            return {}
