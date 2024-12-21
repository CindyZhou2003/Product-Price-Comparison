FROM ubuntu:latest
LABEL authors="Cindy"
# backend/Dockerfile

# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /usr/src/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    libmariadb-dev-compat \
    wget \
    curl \
    unzip \
    xvfb \
    chromium \
    chromium-driver \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libnss3 \
    libasound2 \
    libatk1.0-0 \
    libpangocairo-1.0-0 \
    libcups2 \
    libxrandr2 \
    libgbm1 \
    fonts-liberation \
    libu2f-udev \
    libxshmfence1 \
    xdg-utils \
    && apt-get clean

# Install Python dependencies
COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django backend code
COPY .. /usr/src/backend

# Expose the port Django runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
