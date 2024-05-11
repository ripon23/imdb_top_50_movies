## IMDb Scraper: Advanced Web Scraper for Media Data
A fun projects made using Scrapy. The Spiders included in this are able to extract Movie, TV-Series, TV-Movies based on year and title type. A lot more to come features ahead

### Objective:
Develop a Python-based web scraper using Scrapy to extract detailed information from IMDb’s
Top 50 movies list. The scraper should be robust, handling concurrent requests efficiently, and
packaged in a Docker container for deployment.

### Problem Description:
● The scraper must target the IMDb "Top 50" movies list at this URL: IMDb Top 50 Movies.
● Extract the movie name, year of release, director, and main stars from each movie’s detail
page linked from the Top 50 list.
● The scraper must manage concurrent requests and comply with IMDb’s robots.txt to
respect their scraping policies.


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

IMDb Scraper extracts the following attributes from IMDb websites. Also, have a look at an examplary [json](https://github.com/santhoshse7en/IMDb_Scraper/blob/master/example/sample.json) and [CSV](https://github.com/santhoshse7en/IMDb_Scraper/blob/master/example/sample.csv) file extracted by IMDb Scraper.

* Movie Name
* Released Year
* Director
* Stars Name

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
