FROM python:3.12

WORKDIR /app

COPY ./app /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Set the Flask app to the location of your app.py script
ENV FLASK_APP=app/app.py 

ENV FLASK_ENV=production

# Use flask run with proper script reference
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
