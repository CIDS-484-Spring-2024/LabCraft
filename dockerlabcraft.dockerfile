# Use a Python base image
FROM python:latest

# Install X server dependencies
RUN apt-get update && apt-get install -y \
    xvfb \
    x11-apps \
    mesa-utils \
    libgl1-mesa-glx \
    libxtst6 \
    libxrandr2 \
    libxcursor1 \
    libxrandr-dev

# Set the display environment variable
ENV DISPLAY=host.docker.internal:0

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install the project dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Expose the necessary port
EXPOSE 5000

# Start the application
CMD ["python", "labcraft.py"]
