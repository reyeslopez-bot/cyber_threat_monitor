# Use an official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose any necessary ports (e.g., if you want to access the app externally)
EXPOSE 5000

# Run the main application
CMD ["python", "main.py"]
