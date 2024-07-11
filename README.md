# Allegro Scraper

The Allegro Scraper works by sending HTTP requests to the Allegro.pl website, simulating browser-like behavior using randomly selected user agents to prevent detection. It starts by making requests to the search results page for a given category (e.g., electronics). The spider then extracts the product links from the search results and follows these links to scrape detailed product information, such as the product title, price, and description.

To further avoid detection and potential IP bans, the scraper uses a proxy middleware to fetch a list of proxies from a public API, validate them, and randomly assign a proxy to each request. This ensures that requests appear to come from different IP addresses. The scraper also employs the AutoThrottle feature to adjust the request rate based on the server's load and uses a retry mechanism to handle intermittent network issues and rate limiting by retrying failed requests up to a specified number of times.

## Features

- **Rotating User Agents**: Uses a random user agent for each request to mimic different browsers.
- **Proxy Middleware**: Fetches and validates proxies from a public proxy API to distribute requests and avoid IP blocking.
- **AutoThrottle**: Adjusts the scraping speed based on the load of both the Scrapy server and the website being scraped.
- **Retry Mechanism**: Retries failed requests to handle intermittent network issues and rate limiting.

## Requirements

- Python 3.9
- Scrapy
- Requests
- Fake-UserAgent

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/arslan578/allegro_scraper.git
    cd allegro_scraper
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Run The Project **:
    ```bash
    scrapy crawl allegro
    ```
## Project Structure

allegro_scraper/
├── allegro_scraper/
│ ├── init.py
│ ├── items.py
│ ├── middlewares.py
│ ├── pipelines.py
│ ├── settings.py
│ └── spiders/
│ ├── init.py
│ └── allegro.py
├── scrapy.cfg
└── README.md



## File Descriptions

- **`__init__.py`**: Marks the directory as a Python package.
- **`items.py`**: Defines the data structure for storing the scraped items.
- **`middlewares.py`**: Contains custom middleware for rotating user agents and proxies to avoid detection and blocking.
- **`pipelines.py`**: Defines the pipeline for processing and saving scraped data.
- **`settings.py`**: Contains the Scrapy project settings, including middleware, throttling, and retry configurations.
- **`spiders/`**: Directory containing spider definitions.
  - **`allegro.py`**: The main spider file that contains the logic for scraping Allegro.pl, including parsing search results and product details.
- **`scrapy.cfg`**: Configuration file for the Scrapy project.

## Configuration

### `settings.py`

Key settings include:
- **DOWNLOADER_MIDDLEWARES**: Includes middleware for rotating user agents and proxies.
- **AUTOTHROTTLE_ENABLED**: Enables AutoThrottle to manage request rates dynamically.
- **RETRY_ENABLED**: Enables retrying failed requests.

### `middlewares.py`

Contains the following middlewares:
- **RotateUserAgentMiddleware**: Sets a random user agent for each request.
- **ProxyMiddleware**: Fetches and validates proxies from a proxy API.
- **ProxyUpdater**: Updates the proxy list periodically.

### `pipelines.py`

Configures the output of the scraped data:
```python
import os
import pandas as pd

class AllegroScraperPipeline:
    def open_spider(self, spider):
        self.df = pd.DataFrame()
        os.makedirs('data', exist_ok=True)

    def close_spider(self, spider):
        self.df.to_csv('data/scraped_data.csv', index=False)

    def process_item(self, item, spider):
        self.df = self.df.append(item, ignore_index=True)
        return item




