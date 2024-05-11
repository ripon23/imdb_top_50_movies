## IMDb Scraper: Advanced Web Scraper for Media Data
A fun projects made using Scrapy. The Spiders included in this are able to extract Movie, TV-Series, TV-Movies based on year and title type. A lot more to come features ahead

### Objective:
Develop a Python-based web scraper using Scrapy to extract detailed information from IMDb’s
Top 50 movies list. The scraper should be robust, handling concurrent requests efficiently, and
packaged in a Docker container for deployment.

### Problem Description:
* The scraper must target the IMDb "Top 50" movies list at this URL: IMDb Top 50 Movies.
* Extract the movie name, year of release, director, and main stars from each movie’s detail page linked from the Top 50 list.
* The scraper must manage concurrent requests and comply with IMDb’s robots.txt to respect their scraping policies.


## Run

### Create and activate virtual env 

**Python3**

```python

python3 -m venv venv
. ./venv/bin/activate

```


## Dependencies

### Scrapy

An open source and collaborative framework for extracting the data you need from websites. In a fast, simple, yet extensible way.

### Unidecode
It often happens that you have text data in Unicode, but you need to represent it in ASCII. For example when integrating with legacy code that doesn’t support Unicode, or for ease of entry of non-Roman names on a US keyboard, or when constructing ASCII machine identifiers from human-readable Unicode strings that should still be somewhat intelligible. A popular example of this is when making an URL slug from an article title.

Unidecode is not a replacement for fully supporting Unicode for strings in your program. There are a number of caveats that come with its use, especially when its output is directly visible to users. Please read the rest of this README before using Unidecode in your project.

## Extracted information

IMDb Scraper extracts the following attributes from IMDb websites.

* Movie Name
* Released Year
* Director Name
* Stars Name

## Managing concurrent requests & robots.txt
For managing concurrent requests and comply with IMDb’s robots.txt to respect their scraping policies there is a setting file & we enable following 2 line
```python
# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

```


## Install dependencies

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install following

```python

pip install -r requirements.txt

```

### Usage

```python

scrapy crawl imdb_topmovies

```

**Save the output as a file**

```python

scrapy crawl imdb_topmovies -o output.json

scrapy crawl imdb_topmovies -o output.csv

```

### 1. Create a Dockerfile:
Create a file named Dockerfile in the root directory of your Scrapy project with the following content:

```bash
# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the Scrapy spider when the container launches
CMD scrapy crawl imdb_topmovies
```
### 2. Build the Docker image:

Open a terminal/command prompt, navigate to the directory containing your Dockerfile and Scrapy project, and run the following command to build the Docker image:

```bash
docker build -t scrapy-imdb .
```
This command will build a Docker image named scrapy-imdb based on the instructions in your Dockerfile.

### 3. Run the Docker container:

Once the image is built, you can run a Docker container based on that image using the following command:

```bash
docker run -it scrapy-imdb
```
This command will start a Docker container based on the scrapy-imdb image, and your Scrapy spider will start crawling IMDb's top movies.

Make sure to replace scrapy-imdb with your desired image name and tag.

That's it! Your Scrapy scraper is now packaged within a Docker container, making it portable and easy to deploy across different environments.
