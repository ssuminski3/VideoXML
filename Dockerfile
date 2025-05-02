FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

ENV DEBIAN_FRONTEND=noninteractive

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code into the container
COPY . .

# Command to run the application
CMD ["python", "main.py"]