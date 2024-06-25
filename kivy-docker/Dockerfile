# Step 1: Start with an Ubuntu base image
FROM ubuntu:20.04

# Step 2: Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libgl1-mesa-glx \
    libgles2-mesa \
    x11-xserver-utils \
    libx11-dev \
    xauth \
    xvfb \
    sudo

# Step 3: Install Kivy
RUN pip3 install Cython==0.29.21 kivy==2.3.0 kivy-examples==2.3.0 kivy-garden==0.1.5

# Step 4: Create a directory for the app
WORKDIR /usr/src/app

# Step 5: Copy the app files to the container
COPY ./src /usr/src/app

# Step 6: Set environment variables for display and X11 forwarding
ENV DISPLAY=:0
ENV PYTHONUNBUFFERED=1

# Step 7: Run the Kivy app
CMD ["python3", "kivy_test.py"]

