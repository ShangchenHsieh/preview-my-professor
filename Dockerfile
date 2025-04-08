# Use the official Python 3.12 image from the Docker Hub
FROM python:3.12

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt first to take advantage of Docker layer caching
COPY ./app/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app's code
COPY ./app /app

# Expose the port that Flask will run on (optional)
# Google Cloud will use the `$PORT` environment variable for this
EXPOSE 8080

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Start the Flask application and use the `$PORT` variable
CMD ["flask", "run", "--host=0.0.0.0", "--port=$PORT"]
