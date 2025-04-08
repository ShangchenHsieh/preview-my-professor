FROM python:3.12

# Set working directory to the flask_app subdirectory
WORKDIR /app/flask_app

# Copy only what's needed first to leverage Docker layer caching
COPY /app/flask_app/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the project
COPY . /app

# Expose the port Flask will run on
EXPOSE 8080

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
