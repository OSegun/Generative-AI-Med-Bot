# Official Python image version 3.10 from the Docker Hub
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container's working directory /app
COPY . /app

# Install all packages in the requirements file
RUN pip install -r requirements.txt

# Launch and run app in container
CMD ["python3", "app.py"]