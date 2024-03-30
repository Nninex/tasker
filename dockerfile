# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /code

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code to the container
COPY . .

# Expose port 8000
EXPOSE 8000

# Command to run the production server using Gunicorn
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]