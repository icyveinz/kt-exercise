# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /tg_bot

# Copy the current directory contents into the container at /tg_bot
COPY . /tg_bot

# Make sure the wait-for-db.sh script is executable
RUN chmod +x /tg_bot/wait-for-db.sh

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/tg_bot

# Run the wait-for-db.sh script and then the application
ENTRYPOINT ["/tg_bot/wait-for-db.sh", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]