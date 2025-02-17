# Use a lightweight Python image with multi-arch support
FROM --platform=$TARGETPLATFORM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy application source code
COPY . /app
COPY templates /app/templates

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the application's port (default FastAPI runs on 80)
EXPOSE 80

# Command to start the FastAPI app using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]