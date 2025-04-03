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
                  professor_name, rating, total_ratings, would_take_again, level_of_difficulty, tags, comments
              ) VALUES (
                  %s, %s, %s, %s, %s, %s, %s
              )
              """
            try:
                # Convert lists to PostgreSQL array format
                tags = "{" + ",".join([f'"{tag}"' for tag in professor.tags]) + "}" if professor.tags else "{}"
                comments = "{" + ",".join(
                    [f'"{comment}"' for comment in professor.comments]) + "}" if professor.comments else "{}"

                # Execute the insert query with adapted arrays for tags and comments
                cursor.execute(insert_query, (
                    professor.professor_name,
                    professor.rating,
                    professor.total_ratings,
                    professor.would_take_again,
                    professor.level_of_difficulty,
                    tags,  # Insert formatted tags as a PostgreSQL array
                    comments  # Insert formatted comments as a PostgreSQL array
                ))

                conn.commit()  # Commit the transaction
            except psycopg2.errors.UniqueViolation as e:
                print(f"Duplicate entry found for {professor.professor_name}, skipping insertion.")
                conn.rollback()
            except Exception as e:
                print(f"Error inserting professor {professor.professor_name}: {e}")
                conn.rollback()
            finally:
                pass  # Optional: Close cursor and connection if necessary
        else:
            print("Failed to connect to the database.")

    @staticmethod
    def get_professor_by_name(professor_name: str):
        cursor, conn = DatabaseConnection.get_connection()

        if conn is not None:
            query = """
            SELECT professor_name, rating, total_ratings, would_take_again, level_of_difficulty, tags, comments
            FROM rmp_professor_info
            WHERE professor_name = %s;
            """
            try:
                cursor.execute(query, (professor_name,))
                professor_data = cursor.fetchone()  # Fetch the professor data
                return professor_data
            except Exception as e:
                print(f"Error retrieving professor data: {e}")
                return None
        else:
            print("Failed to connect to the database.")
            return None
