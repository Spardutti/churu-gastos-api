# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the render-build.sh script into the container
COPY ./render-build.sh /app/bin/render-build.sh

# Make render-build.sh executable
RUN chmod +x /app/bin/render-build.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE $PORT

# Run the render build script and start gunicorn
CMD ["sh", "-c", "/app/bin/render-build.sh && gunicorn churugastos.wsgi --workers=3 --bind=0.0.0.0:8000"]
