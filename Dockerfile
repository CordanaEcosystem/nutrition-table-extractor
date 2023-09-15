# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Install system dependencies, including libgl1-mesa-glx
RUN apt-get update && apt-get install -y gcc python3-dev && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 && apt-get install -y python3-opencv && apt-get install -y tesseract-ocr

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Copy the Gunicorn configuration file into the image.
COPY gunicorn_config.py ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Cloud Run will listen on.
ENV PORT 8080
EXPOSE $PORT

# Set the DJANGO_ENV environment variable to "development" by default.
# Override this variable when deploying on Cloud Run.
ENV DJANGO_ENV production

# Use Gunicorn to run the Django application with the provided Gunicorn configuration file.
CMD if [ "$DJANGO_ENV" = "production" ]; \
    then exec gunicorn --bind :$PORT --config gunicorn_config.py off-nutrition-table-extractor.wsgi:application; \
    else exec python manage.py runserver 0.0.0.0:$PORT; \
    fi
