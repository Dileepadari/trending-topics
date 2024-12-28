# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY trending5/ ./trending5

RUN apt-get update && \
    apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    libx11-dev \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxrandr2 \
    libxrender1 \
    libfontconfig1 \
    libdbus-1-3 \
    libasound2 \
    libnss3 \
    libxtst6 \
    libgtk-3-0 \
    xdg-utils && \
    rm -rf /var/lib/apt/lists/*


RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# Install Google Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -yqq update && \
    apt-get -yqq install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*


# Install Python dependencies
COPY trending5/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=/app/trending5/app.py

# Expose the port Flask runs on
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
