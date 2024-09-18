# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE $PORT

# Run gunicorn with your wsgi app
CMD ["gunicorn", "churugastos.wsgi", "--workers=3", "--bind=0.0.0.0:8000"]
