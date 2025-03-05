FROM ubuntu:latest
RUN apt-get update && apt-get install-y iputils-ping
# Use an official Python runtime as a parent image
FROM python:3.12-slim
# Set the working directory in the container
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . /app/
COPY templates /app/templates
# Install dependencies
RUN pip install -r requirements.txt

# Expose the port the app will run on
EXPOSE 8000
# Command to run the app using uvicon
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]