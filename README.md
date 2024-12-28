# Trending Topics Scraper and Viewer

## Project Overview
This project consists of a **Flask-based web application** that scrapes trending topics from Twitter (X) using Selenium WebDriver and stores the data in a **MongoDB database**. The application allows users to view the latest trending topics by clicking a button, with the option to fetch the most recent scraped data or get the data directly from MongoDB.

The project is divided into several key components:
1. **Flask Web Application** - The main web interface.
2. **Selenium-based Scraping** - A Python script that scrapes trending topics from Twitter (X) using Selenium.
3. **ProxyMesh Integration** - Utilizes ProxyMesh to rotate IP addresses for scraping.
4. **MongoDB Database** - Stores the scraped data for later retrieval.
5. **Docker Setup** - Containerizes the application for easy deployment.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [API Endpoints](#api-endpoints)
4. [Scraping Process](#scraping-process)
5. [Folder Structure](#folder-structure)
6. [Docker Setup](#docker-setup)

## Installation

### Prerequisites:
- **Python 3.10+**
- **MongoDB** (local or remote instance)
- **Docker** (for containerized setup)

### Setup Instructions:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Dileepadari/trending-topics.git
   cd trending-topics
   ```

2. **Set up MongoDB:**
   Ensure you have access to a MongoDB instance. You can either use a local instance or a cloud-based service like MongoDB Atlas. Update the MongoDB connection details in `db.py` and `config.py`.
Set up MongoDB: Ensure you have access to a MongoDB instance. You can either use a local instance or a cloud-based service like MongoDB Atlas. Update the MongoDB connection details in db.py and config.py.

3. **Create a .env File:**
   You will need to configure environment variables in a `.env` file for API keys and other sensitive details. Example:
   ```bash
   MONGO_URI=mongodb+srv://dummy:dummpy_password@dummy.0k8nk.mongodb.net/dummy?retryWrites=true&w=majority&appName=dummy
   PROXY_URI=http://dummy:dummy_password@dummy:6540
   TWITTER_USERNAME=dummy
   TWITTER_PASSWORD=dummy
   TWITTER_MAIL=dummy@gmail.com
   ```
Create a .env File: You will need to configure environment variables in a .env file for API keys and other sensitive details. Example:

### Running the Application:
Usage
Running the Flask Application:

- After ensuring that the requirements are met, go to the project directory and run the following commands:
  ```bash
  docker compose up --build
  ```
This will start the server at `http://localhost:5000/`.

later you can just use docker compose up to start the server.

### Web Interface:
- **Home Page (/):** Displays a button that, when clicked, scrapes the trending topics from Twitter (X) and displays them on the page.
This will start the server at http://127.0.0.1:5000/.

### Screenshots:
- **Home Page (/):** Displays a button that, when clicked, scrapes the trending topics
![Home](/project_images/home.png)

- **Loading Page:** While the scraping process is running, a loading page is displayed.
![Home_loading](/project_images/home_loading.png)

### API Endpoints:
- **`/api/trending`:** This endpoint triggers the scraping process and returns the latest trending topics in JSON format.
- **`/api/alltrending`:** Fetches all previously saved trending topics from the MongoDB database.
- **`/api/lasttrending`:** Returns the most recent trend from the database.
    Home Page (/): Displays a button that, when clicked, scrapes the trending topics from Twitter (X) and displays them on the page.
    API Endpoints:
        /api/trending: This endpoint triggers the scraping process and returns the latest trending topics in JSON format.
        /api/alltrending: Fetches all previously saved trending topics from the MongoDB database.
        /api/lasttrending: Returns the most recent trend from the database.

### Interaction Flow:
- **Scraping Button:** When clicked, the `scrape_and_save` endpoint is triggered, scraping the latest trending topics and saving them in the MongoDB database.
- **Generate Again Button:** After fetching the trends, another button appears. When clicked, it fetches the most recent trending topics from the MongoDB collection using the `/api/lasttrending` endpoint.

## Scraping Process
The `scrape_trending_topics` function uses Selenium WebDriver to automate the following tasks:
1. **Login to Twitter (X):** Using credentials from the `.env` file, the script logs into Twitter (X).
2. **Navigate to Trending Section:** After logging in, the script navigates to the trending topics section of the platform.
3. **Scrape Trending Topics:** The script collects the first five trending topics on Twitter (X).
4. **Store Data in MongoDB:** The scraped data, along with the IP address used, is stored in MongoDB for future reference.
/api/lasttrending (GET)

**Important:** The script uses a headless browser (with ChromeDriver) to run without opening a graphical browser window.
    Description: Fetches the most recent trend from the database.
    Response:
        200 OK: Returns the latest trend data from MongoDB.

**Note:** 
- The scraping process takes time about 30 seconds to 3 min depending on the internet speed.
- The proxymesh account has a bandwidth limit, so use your own proxy if the limit exceeds.