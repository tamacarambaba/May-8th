Instagram Scraper, Filter, and Visualization Tool
Overview

This project allows you to:

    Scrape Instagram posts by hashtag

    Filter posts by date

    Perform topic modeling on post captions using BERTopic

    Visualize hashtag co-occurrences as a network

All features are controlled by a single script (main.py) using a mode setting.
Virtual Environment (venv)

A complete virtual environment with all required dependencies is already included in this project.
If you are using this environment, you do not need to install the requirements again.
How to use the included venv

On Windows (PowerShell):

.\venv\Scripts\activate
python main.py

On macOS/Linux:

source venv/bin/activate
python main.py

If you decide to create a fresh environment instead, install the dependencies via:

pip install -r requirements.txt

Modes

You can select the mode by setting the mode variable in main.py:

    scraper: Scrapes posts from Instagram based on a hashtag

    filter: Filters posts by a specific date

    topics: Runs BERTopic on captions to find most frequent topics

    network: Creates a hashtag co-occurrence network visualization

Parameters
General

    base_path: Base directory of the project

Scraper Parameters

    hashtag: Hashtag to scrape

    scroll_count: How many times to scroll down the hashtag page

    max_posts_to_scrape: Maximum number of posts to scrape

    instagram_name: Instagram username

    instagram_password: Instagram password

    use_proxy: Boolean, use proxy or not

    proxy_host, proxy_port, proxy_user, proxy_pass: Proxy settings

    scraping_hidden: Hidden scraping (currently not fully automated)

Filter Parameters

    filter_target_date: Date to filter posts by (format: YYYY-MM-DD HH:MM:SS)

    filter_target_folder_path: Folder containing posts to filter

    filter_output_folder_path: Folder to store filtered posts

Topics Parameters

    topics_output_filename: Output filename for topic visualization

    topics_inner_folder_path: Folder containing posts to analyze

Network Parameters

    network_output_filename: Output filename for network visualization

    network_inner_folder_path: Folder containing posts to visualize

Example Usage

    Scraping:

mode = "scraper"

Runs the hashtag scraper.

    Filtering:

mode = "filter"

Copies all posts from the target folder that match the given date to the output folder.

    Topics:

mode = "topics"

Analyzes captions and generates a visualization of the top topics.

    Network:

mode = "network"

Builds and visualizes a hashtag co-occurrence network.
Output

    Scraper: Saves post folders with metadata JSON

    Filter: Saves filtered post folders to the output path

    Topics: Saves a PNG visualization of the most frequent topics

    Network: Saves a PNG visualization of the hashtag network