import os
import re
import json
import time
import yt_dlp
import random
import zipfile
import requests
import selenium
from datetime import date
from modulefinder import test
from selenium import webdriver
from collections import Counter
from collections import defaultdict
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


def waiting(seconds):
    time.sleep(seconds)

def newTab(browser):
    browser.execute_script("window.open('');")

def switchToMostRightTab(browser):
    browser.switch_to.window(browser.window_handles[-1])                                             

def openWebpage(browser, url):
    browser.get(url)
    waiting(get_random_in_range(5, 10))

def clickButtonBy(browser, by, value_x):
    browser.find_element(by, value = value_x).click()                                            

def fillInputFieldBy(browser, by, value_x, text):
    browser.find_element(by, value_x).send_keys(text)

def openUrlInNewTab(browser, url):
    newTab(browser)
    switchToMostRightTab(browser)
    openWebpage(browser, url)

# RETURNS TRUE, IF THERE EXIST AT LEAST ONE MORE PICTURE FOR THE POST
def exist_weiter_button(driver):
    try:
        driver.find_element("css selector", 'div._9zm2')
        return True
    except NoSuchElementException:
        return False


# CLICKS THE BUTTON "WEITER" TO SEE THE NEXT PICTURE OF THE POST
def click_weiter_button(driver):
    try:
        div = driver.find_element("css selector", 'div._9zm2')
        button = div.find_element("xpath", './ancestor::button')
        button.click()
        return True
    except (NoSuchElementException, ElementClickInterceptedException):
        return False
    

def create_json_file_if_missing(filename_base):
    filename = f"{filename_base}.json"
    
    if os.path.exists(filename):
        print(f"'{filename}' already exists. Doing nothing.")
        return filename
    
    # File doesn't exist → create with empty JSON object
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)
    
    print(f"Created new JSON file: '{filename}'")
    return filename

def create_folder_if_missing(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")
        return folder_name
    else:
        print(f"Folder '{folder_name}' already exists.")
        return folder_name

def get_json_post_urls(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    post_urls = [entry['post_url'] for entry in data if 'post_url' in entry]
    return post_urls

def get_json_post_by_index(index):
    return get_json_posts_as_list()[index]

def get_post_id(url):
    url = url.rstrip("/")
    return url.split("/p/")[1]

def add_urls_to_json(json_file, new_post_urls):
    all_urls = []
    f = open(json_file, "r")
    old_urls = get_json_post_urls(json_file)
    all_urls = get_json_posts_as_list(json_file)
    for url in new_post_urls:
        if url not in old_urls:
            all_urls.append({"post_id": get_post_id(url), "post_url": url, "image_path": "", "text": [], "post_date":"", "scrape_date":str(date.today())})
    f = open(json_file, "w")
    json.dump(all_urls, f, indent=2)                                                                            # .dump writes list components to json file | indent: json file structure (2 spaces for higher readability)
    
    all_urls.clear()
    old_urls.clear()
    new_post_urls.clear()


def get_json_post_count(json_file):
    f = open(json_file, "r")
    json_urls = json.load(f)
    return len(json_urls)

def get_json_post_count_updated(json_file):
    if os.path.getsize(json_file) == 0:
        return 0

    with open(json_file, "r", encoding="utf-8") as f:
        try:
            json_data = json.load(f)
            return len(json_data)
        except json.JSONDecodeError:
            # Datei ist nicht leer, aber kein gültiges JSON
            return 0

def get_json_posts_as_list(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        json_urls = json.load(f)
    return json_urls

def get_text_from_post_url(browser):
    text_list = []
    text_elem_list = browser.find_elements(By.CLASS_NAME, "x193iq5w") 
    switchToMostRightTab(browser)
    for elem in text_elem_list:
        text_list.append(elem.text)
    #browser.close()
    return text_list


def get_matching_cache_key_indexes(ig_keys, target_count, similarity_threshold=0.6):
    """
    Findet die Indexe von ig_cache_keys, die mit mindestens 'similarity_threshold'
    Prozent Übereinstimmung am häufigsten vorkommen (und genau target_count mal).
    
    Args:
        ig_keys (list of str): Liste von ig_cache_keys (erster Teil).
        target_count (int): Anzahl Carousel-Bilder (z. B. Klicks + 1).
        similarity_threshold (float): Ähnlichkeitsgrenze (Standard = 0.6).
    
    Returns:
        list of int: Indexe der übereinstimmenden Cache Keys.
    """
    def similarity(a, b):
        matches = sum(x == y for x, y in zip(a, b))
        return matches / max(len(a), len(b))

    # Zähle Übereinstimmungen
    for candidate in ig_keys:
        similar_indexes = [i for i, key in enumerate(ig_keys) if similarity(candidate, key) >= similarity_threshold]
        if len(similar_indexes) == target_count:
            return similar_indexes

    return []  # Kein passender Satz gefunden

def get_url(post):
    return  post.get("post_url")

def get_count_of_posts_per_date(json_file):
    # Load the JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # If it's just one post, wrap it in a list for uniformity
    if isinstance(data, dict):
        posts = [data]
    elif isinstance(data, list):
        posts = data
    else:
        raise ValueError("Unexpected JSON structure.")

    # Count posts by post_date
    date_counter = Counter()
    for post in posts:
        post_date = post.get('post_date', 'UNKNOWN')
        if post_date.strip():  # Ignore empty strings
            date_counter[post_date.strip()] += 1

    # Print the results
    print("Post count per date:")
    for date, count in date_counter.items():
        print(f"{date}: {count}")


def get_post_count_for_date(json_file, target_post_date):
    # Load the JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Ensure uniform list structure
    if isinstance(data, dict):
        posts = [data]
    elif isinstance(data, list):
        posts = data
    else:
        raise ValueError("Unexpected JSON structure.")

    # Count matching posts
    count = 0
    for post in posts:
        post_date = post.get('post_date', '').strip()
        if post_date == target_post_date:
            count += 1

    print(f"\n📅 Post count for date '{target_post_date}': {count}")
    return count


def map_hashtags_to_posts(posts_list, hashtag_list):
    hashtag_to_posts = defaultdict(list)
    normalized_hashtags = [tag.lower().strip() for tag in hashtag_list]

    for post in posts_list:
        post_id = post.get("post_id")
        text_items = post.get("text", [])
        full_text = "\n".join(text_items).lower()

        for tag in normalized_hashtags:
            pattern = re.escape(tag).replace("#", "#?")
            if re.search(rf'\b{pattern}\b', full_text, re.UNICODE):
                hashtag_to_posts[tag].append(post_id)

    # Print hashtag counts
    print("\n📊 Hashtag usage summary:")
    for tag in normalized_hashtags:
        count = len(hashtag_to_posts[tag])
        print(f"{tag}: {count} post(s)")

    return dict(hashtag_to_posts)

def map_hashtags_for_specific_date(posts_list, hashtag_list, target_post_date):
    """
    Returns a dictionary mapping hashtags to post_ids, but only for posts
    with post_date matching target_post_date exactly.
    """
    hashtag_to_posts = defaultdict(list)
    normalized_hashtags = [tag.lower().strip() for tag in hashtag_list]

    for post in posts_list:
        if post.get("post_date", "").strip() != target_post_date:
            continue  # Skip posts with different date

        post_id = post.get("post_id")
        text_items = post.get("text", [])
        full_text = "\n".join(text_items).lower()

        for tag in normalized_hashtags:
            pattern = re.escape(tag).replace("#", "#?")
            if re.search(rf'\b{pattern}\b', full_text, re.UNICODE):
                hashtag_to_posts[tag].append(post_id)

    # Print summary
    print(f"\n📅 Hashtag usage for date: {target_post_date}")
    for tag in normalized_hashtags:
        count = len(hashtag_to_posts[tag])
        print(f"{tag}: {count} post(s)")

    return dict(hashtag_to_posts)

def extract_ig_key(url):
    match = re.search(r"ig_cache_key=([^\%\&]+)", url)
    return match.group(1) if match else None


def is_video(browser):
    try:
        # Wait if needed and locate video element
        video_element = browser.find_element(By.TAG_NAME, "video")
        return video_element is not None
    except:
        return False

def is_video_in_carousel(driver):
    try:
        # Find all <li> elements with class "_acaz"
        li_elements = driver.find_elements(By.CLASS_NAME, "_acaz")
        
        for li in li_elements:
            # Check if a <video> tag exists inside the <li>
            video_tags = li.find_elements(By.TAG_NAME, "video")
            if video_tags:
                return True
        return False
    except:
        return False

def save_media_from_post_url(browser, post_url):
    
    #SET FOR MEDIA URLS
    img_urls = set()
    #STORES BOOL TO RUN yt_dlb LATER
    videos_exists = False 
    
    # OPEN POSTING PAGE:
    openUrlInNewTab(browser, post_url)
    browser.refresh()
    time.sleep(5)
    waiting(5)

    
    
    #LOOP THROUGH CAROUSEL IF IT IS A CAROUSEL
    while True:
        file_path = ""

        #IF VIDEOS EXISTS RUN yt_dlb LATER
        if not videos_exists and is_video_in_carousel(browser):
            videos_exists = True
            print("VIDEOS EXIST")
        
        #SELECT CAROUSEL SECTION
        carousel_items = browser.find_elements(By.CSS_SELECTOR, "li._acaz")

        #SINGLE IMAGE OR VIDEO
        if not carousel_items:
            if videos_exists:
                #GET COOKIE FROM CURRENT SESSION
                cookies = browser.get_cookies()
                cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}

                #FORMAT COOKIES FOR yt_dlb
                with open("cookies_instagram.txt", "w", encoding="utf-8") as f:
                    f.write("# Netscape HTTP Cookie File\n")
                    for cookie in cookies:
                        domain = cookie["domain"]
                        name = cookie["name"]
                        value = cookie["value"]
                        path = cookie.get("path", "/")
                        secure = "TRUE" if cookie.get("secure", False) else "FALSE"
                        f.write(f"{domain}\tTRUE\t{path}\t{secure}\t0\t{name}\t{value}\n")

                #DOWNLOAD VIDEOS
                ydl_opts = {
                    'outtmpl': os.path.join("videos", f"insta_video_post_{get_post_id(post_url)}_%(autonumber)s.%(ext)s"),
                    'format': 'bv*+ba/bv/b[ext=mp4]/bestvideo',  # Only video formats
                    'merge_output_format': 'mp4',
                    'noplaylist': True,
                    'quiet': False,
                    'ignoreerrors': True,
                    'cookiesfromfile': 'cookies_instagram.txt',
                }

                # Download starten
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([post_url])
            else:
                file_path = os.path.join("images", f"insta_image_post_{get_post_id(post_url)}.jpg")
        
                img_element = browser.find_element(By.CSS_SELECTOR, "img.x5yr21d")
                img_url     = img_element.get_attribute("src")
                img_data    = requests.get(img_url).content

                with open(file_path, "wb") as f:
                    f.write(img_data)
                print("IMAGE HERUNTERGELADEN " + file_path)
            break

        #COLLECT IMAGE URLs
        for item in carousel_items:
            #ONLY IMG URLs
            try:
                img = item.find_element(By.CSS_SELECTOR, "img.x5yr21d")
                img_url = img.get_attribute("src")
                #ONLY NEW IMG URLs
                if img_url and img_url not in img_urls:
                    img_urls.add(img_url)
                    print("URLS GESAMMELT: " + str(len(img_urls)))
            except:
                pass
        if exist_weiter_button(browser):
            click_weiter_button(browser)
            waiting(5)
            print("WEITER------>")
        else:
            print("XXXXXXXXXXXXXXXX LOOP STOPPED XXXXXXXXXXXXXXXX")
            break


    os.makedirs("test_images", exist_ok=True)
    os.makedirs("test_videos", exist_ok=True)
    

    #DOWNLOAD IMAGES
    for img_counter, img_url in enumerate(img_urls):
        img_data = requests.get(img_url).content
        file_path = os.path.join("images", f"insta_image_post_{get_post_id(post_url)}_{img_counter}.jpg")
        with open(file_path, "wb") as f:
            f.write(img_data)
        print("IMAGE HERUNTERGELADEN " + file_path)
        
    #DOWNLOAD VIDEOS IF VIDEOS EXISTED
    if videos_exists:
        #GET COOKIE FROM CURRENT SESSION
        cookies = browser.get_cookies()
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}

        #FORMAT COOKIES FOR yt_dlb
        with open("cookies_instagram.txt", "w", encoding="utf-8") as f:
            f.write("# Netscape HTTP Cookie File\n")
            for cookie in cookies:
                domain = cookie["domain"]
                name = cookie["name"]
                value = cookie["value"]
                path = cookie.get("path", "/")
                secure = "TRUE" if cookie.get("secure", False) else "FALSE"
                f.write(f"{domain}\tTRUE\t{path}\t{secure}\t0\t{name}\t{value}\n")

        #DOWNLOAD VIDEOS
        ydl_opts = {
            'outtmpl': os.path.join("videos", f"insta_video_post_{get_post_id(post_url)}_%(autonumber)s.%(ext)s"),
            'format': 'bv*+ba/bv/b[ext=mp4]/bestvideo',  # Only video formats
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': False,
            'ignoreerrors': True,
            'cookiesfromfile': 'cookies_instagram.txt',
        }

        # Download starten
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([post_url])
    
    return file_path

def save_media_from_post_url_updated(browser, image_folder, video_folder, post_url):
    
    #SET FOR MEDIA URLS
    img_urls = set()
    #STORES BOOL TO RUN yt_dlb LATER
    videos_exists = False
    
    
    #LOOP THROUGH CAROUSEL IF IT IS A CAROUSEL
    while True:
        file_path = ""

        #IF VIDEOS EXISTS RUN yt_dlb LATER
        if not videos_exists and is_video_in_carousel(browser):
            videos_exists = True
            print("VIDEOS EXIST")
        
        #SELECT CAROUSEL SECTION
        carousel_items = browser.find_elements(By.CSS_SELECTOR, "li._acaz")

        #SINGLE IMAGE OR VIDEO
        if not carousel_items:
            if videos_exists:
                #GET COOKIE FROM CURRENT SESSION
                cookies = browser.get_cookies()
                cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}

                #FORMAT COOKIES FOR yt_dlb
                with open("cookies_instagram.txt", "w", encoding="utf-8") as f:
                    f.write("# Netscape HTTP Cookie File\n")
                    for cookie in cookies:
                        domain = cookie["domain"]
                        name = cookie["name"]
                        value = cookie["value"]
                        path = cookie.get("path", "/")
                        secure = "TRUE" if cookie.get("secure", False) else "FALSE"
                        f.write(f"{domain}\tTRUE\t{path}\t{secure}\t0\t{name}\t{value}\n")

                #DOWNLOAD VIDEOS
                ydl_opts = {
                    'outtmpl': os.path.join(video_folder, f"insta_video_post_{get_post_id(post_url)}_%(autonumber)s.%(ext)s"),
                    'format': 'bv*+ba/bv/b[ext=mp4]/bestvideo',  # Only video formats
                    'merge_output_format': 'mp4',
                    'noplaylist': True,
                    'quiet': False,
                    'ignoreerrors': True,
                    'cookiesfromfile': 'cookies_instagram.txt',
                }

                # Download starten
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([post_url])
            else:
                file_path = os.path.join(image_folder, f"insta_image_post_{get_post_id(post_url)}.jpg")
        
                img_element = browser.find_element(By.CSS_SELECTOR, "img.x5yr21d")
                img_url     = img_element.get_attribute("src")
                img_data    = requests.get(img_url).content

                with open(file_path, "wb") as f:
                    f.write(img_data)
                print("IMAGE HERUNTERGELADEN " + file_path)
            break

        #COLLECT IMAGE URLs
        for item in carousel_items:
            #ONLY IMG URLs
            try:
                img = item.find_element(By.CSS_SELECTOR, "img.x5yr21d")
                img_url = img.get_attribute("src")
                #ONLY NEW IMG URLs
                if img_url and img_url not in img_urls:
                    img_urls.add(img_url)
                    print("URLS GESAMMELT: " + str(len(img_urls)))
            except:
                pass
        if exist_weiter_button(browser):
            click_weiter_button(browser)
            waiting(5)
            print("WEITER------>")
        else:
            print("XXXXXXXXXXXXXXXX LOOP STOPPED XXXXXXXXXXXXXXXX")
            break
    

    #DOWNLOAD IMAGES
    for img_counter, img_url in enumerate(img_urls):
        img_data = requests.get(img_url).content
        file_path = os.path.join(image_folder, f"insta_image_post_{get_post_id(post_url)}_{img_counter}.jpg")
        with open(file_path, "wb") as f:
            f.write(img_data)
        print("IMAGE HERUNTERGELADEN " + file_path)
        
    #DOWNLOAD VIDEOS IF VIDEOS EXISTED
    if videos_exists:
        #GET COOKIE FROM CURRENT SESSION
        cookies = browser.get_cookies()
        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}

        #FORMAT COOKIES FOR yt_dlb
        with open("cookies_instagram.txt", "w", encoding="utf-8") as f:
            f.write("# Netscape HTTP Cookie File\n")
            for cookie in cookies:
                domain = cookie["domain"]
                name = cookie["name"]
                value = cookie["value"]
                path = cookie.get("path", "/")
                secure = "TRUE" if cookie.get("secure", False) else "FALSE"
                f.write(f"{domain}\tTRUE\t{path}\t{secure}\t0\t{name}\t{value}\n")

        #DOWNLOAD VIDEOS
        ydl_opts = {
            'outtmpl': os.path.join(video_folder, f"insta_video_post_{get_post_id(post_url)}_%(autonumber)s.%(ext)s"),
            'format': 'bv*+ba/bv/b[ext=mp4]/bestvideo',  # Only video formats
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': False,
            'ignoreerrors': True,
            'cookiesfromfile': 'cookies_instagram.txt',
        }

        # Download starten
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([post_url])
    
    return file_path
      
def save_img_from_post_url(browser, url):


    # OPEN POSTING PAGE:
    openUrlInNewTab(browser, url)
    browser.refresh()
    time.sleep(5)
    
    # NO NEXT BUTTON -> DOWNLOAD IMAGE
    if not exist_weiter_button(browser):
        image_path = os.path.join("test_images_2", f"insta_image_post_{get_post_id(url)}.jpg")
        
        img_element = browser.find_element(By.CSS_SELECTOR, "li._acaz img.x5yr21d")
        img_url     = img_element.get_attribute("src")
        img_data    = requests.get(img_url).content

        with open(image_path, "wb") as f:
            f.write(img_data)
    
    else:
        # GO TO LAST IMAGE/VIDEO IN CAROUSEL AND COUNT ITEMS
        img_counter = 0
        media_urls = set()
        os.makedirs("test_images_2", exist_ok=True)

        while exist_weiter_button(browser):
            waiting(3)

            # Check for both images and videos
            carousel_items = browser.find_elements(By.CSS_SELECTOR, "li._acaz")

            for item in carousel_items:
                media_url = None
                file_ext = ".jpg"  # Default

                # 🖼️ Versuche Bild zu finden
                try:
                    img = item.find_element(By.CSS_SELECTOR, "img.x5yr21d")
                    media_url = img.get_attribute("src")
                    file_ext = ".jpg"
                except:
                    pass  # Kein Bild gefunden

                # 🎥 Falls kein Bild, versuche Video
                if not media_url:
                    try:
                        video = item.find_element(By.TAG_NAME, "video")

                        # Versuche echte URL zu bekommen
                        media_url = video.get_attribute("src")

                        # Falls blob, nutze currentSrc per JS
                        if not media_url or media_url.startswith("blob:"):
                            media_url = browser.execute_script("return arguments[0].currentSrc;", video)

                        # Wenn immer noch ungültig, überspringen
                        if not media_url or not media_url.startswith("http"):
                            continue

                        file_ext = ".mp4"
                    except:
                        continue  # Kein Video gefunden, Element überspringen

                # ✅ Nur neue Medien speichern
                if media_url and media_url not in media_urls:
                    img_counter += 1
                    media_urls.add(media_url)

                    try:
                        media_data = requests.get(media_url).content
                        file_path = os.path.join("test_images_2", f"insta_media_post_{get_post_id(url)}_{img_counter}{file_ext}")
                        with open(file_path, "wb") as f:
                            f.write(media_data)
                    except Exception as e:
                        print(f"❌ Fehler beim Download von {media_url}: {e}")


            click_weiter_button(browser)
            waiting(5)

    """
    # NEXT BUTTON EXISTS
    else:
        # GO TO LAST IMAGE IN CAROUSEL AND COUNT IMAGES
        img_counter = 0
        img_urls = set()
        while exist_weiter_button(browser):
            waiting(3)
            img_elements = browser.find_elements(By.CSS_SELECTOR, "li._acaz img.x5yr21d")
            print(len(img_elements))
            for img_element in img_elements:
                img_url     = img_element.get_attribute("src")
                if img_url not in img_urls:
                    img_counter += 1
                    img_urls.add(img_url)
                    img_data    = requests.get(img_url).content
                    image_path  = os.path.join("test_images_2", f"insta_image_post_{get_post_id(url)}_"+ str(img_counter)+".jpg")
                    with open(image_path, "wb") as f:
                        f.write(img_data)

            click_weiter_button(browser)
            waiting(5)
    """

    return True

def has_image_path(post):
    return post["image_path"]                               #bool(post.get("image_path"))

def has_text(post):
    return post["text"]                                     #bool(post.get("text"))

def has_no_text_index(json_file):
    all_posts = get_json_posts_as_list(json_file)
    i = 0
    while all_posts[i]['text']:
        i = i + 1
    return i

def has_no_image_index(json_file):
    all_posts = get_json_posts_as_list(json_file)
    i = 0
    while all_posts[i]['image_path']:
        i = i + 1
    return i

def get_url(post):
    return  post.get("post_url")

def add_img_to_json_posts(counter, json_file):
    all_posts = get_json_posts_as_list()
    for post in all_posts:
        if not has_image_path(post):
            post["image_path"] = save_img_from_post_url(get_url(post))
            counter = counter - 1
        if counter <= 0:
            break
    with open(json_file, "w") as f:
        json.dump(all_posts, f, indent=2)

def add_text_to_json_posts(count, json_file):
    all_posts = get_json_posts_as_list()
    for post in all_posts:
        if not has_text(post):
            post["text"] = get_text_from_post_url(get_url(post))
            count = count - 1
        if not (count > 0):
            break
    with open(json_file, "w") as f:
        json.dump(all_posts, f, indent=2)
    
def add_text_to_json_posts_mit_index(browser, index, json_file):
    all_posts = get_json_posts_as_list(json_file)
    all_posts[index]["text"] = get_text_from_post_url(browser)
    with open(json_file, "w") as f:
        json.dump(all_posts, f, indent=2)

def get_random_in_range(start, end):
    return random.randint(start,end)

def scroll_till_end(browser):
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def scroll_x_times(browser, scroll_count):
    for i in range(scroll_count):
        scroll_till_end(browser)
        waiting(10)

# COLLECTING ALL POSTING LINKS from current page AND STOREs THEM IN "post_urls"
def collect_posting_urls_from_webpage(browser):
    post_urls = []
    post_elements = browser.find_elements(By.CSS_SELECTOR, 'a[href^="/p/"]')

    # Extract unique post URL
    seen = set()
    for elem in post_elements:
        href = elem.get_attribute("href")
        if href and href not in seen:
            post_urls.append(href)
            seen.add(href)
    return post_urls

def print_collected_urls(new_post_urls):
    # Output collected links
    print(f"Collected {len(new_post_urls)} post links.")
    for url in new_post_urls:
        print(url)

def check_proxy_connection(browser):
    try:
        browser.get("https://api.ipify.org/?format=json")
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
        print("CONNECTED TO PROXY")
    except:
        print("PROXY CONNECTION FAILED")

## PROXY
def get_chrome_driver(use_proxy=False, proxy_host=None, proxy_port=29842, proxy_user="iweber02", proxy_pass="qp9dQbDM", scraping_hidden=False, user_agent=None):
    PROXY_HOST = proxy_host
    PROXY_PORT = proxy_port
    PROXY_USER = proxy_user
    PROXY_PASS = proxy_pass
 
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
 
    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };
 
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
 
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
 
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    service = Service(executable_path='C:\\Users\\User1\\Documents\\UNIVERSITAET\\DSAI_PROJEKT\\May-8th\\Webdriver\\chromedriver-win64\\chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")  if scraping_hidden else None                       # behaviour not visible on the machine
 
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'
 
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        options.add_extension(pluginfile)
    if user_agent:
        options.add_argument('--user-agent=%s' % user_agent)
 
    driver = webdriver.Chrome(service=service, options=options)
    #driver = webdriver.Chrome(options=options)
    return driver


def extract_post_date(posts):
    for post in posts:
        text_list = post.get("text", [])
        post_date = ""

        # Case 1: Use last element if it's valid
        if text_list:
            last_text = text_list[-1].strip()
            if last_text and last_text.lower() != "mehr":
                post_date = last_text
            else:
                # Case 2: Use the entry before "Meta"
                if "Meta" in text_list:
                    meta_index = text_list.index("Meta")
                    if meta_index > 0:
                        possible_date = text_list[meta_index - 1].strip()
                        if possible_date:
                            post_date = possible_date

        print(post_date)
        post["post_date"] = post_date  # Save into the post dictionary
    return posts

def extract_single_post_date(post):
    text_list = post.get("text", [])
    post_date = ""

    # Case 1: Use last element if it's valid
    if text_list:
        last_text = text_list[-1].strip()
        if last_text and last_text.lower() != "mehr":
            post_date = last_text
        else:
            # Case 2: Use the entry before "Meta"
            if "Meta" in text_list:
                meta_index = text_list.index("Meta")
                if meta_index > 0:
                    before_meta = text_list[meta_index - 1].strip()

                    if before_meta == "Kommentare zu diesem Beitrag wurden limitiert." and meta_index >= 2:
                        possible_date = text_list[meta_index - 2].strip()
                    else:
                        possible_date = before_meta

                    if possible_date:
                        post_date = possible_date

    print(post_date)
    post["post_date"] = post_date  # Save into the post dictionary
    return post

def get_recent_post_indexes(posts):
    recent_keywords = ["Gestern", "Tagen", "Stunden"]
    matching_indexes = []

    for i, post in enumerate(posts):
        post_date = post.get("post_date", "")
        if any(keyword in post_date for keyword in recent_keywords):
            matching_indexes.append(i)

    return matching_indexes

def add_dates_to_json_posts(post_index, json_file):
    all_posts   = get_json_posts_as_list(json_file)
    all_posts[post_index] = extract_single_post_date(all_posts[post_index])
    with open(json_file, "w") as f:
        json.dump(all_posts, f, indent=2)


def is_valid_post_date(post_date):
    """
    Prüft, ob das post_date einem gültigen Muster wie '9. April' oder '12. November 2024' entspricht.
    """
    month_names = [
        "Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember"
    ]
    # Regulärer Ausdruck für Tag. Monatname (optional Jahr)
    regex = r"^\d{1,2}\.\s+(" + "|".join(month_names) + r")(?:\s+\d{4})?$"
    return re.match(regex, post_date.strip()) is not None


def save_posts_with_valid_dates(posts, output_path):
    """
    Filtert Posts mit gültigem post_date und speichert sie als neue JSON-Datei.
    """
    valid_posts = [post for post in posts if is_valid_post_date(post.get("post_date", ""))]

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(valid_posts, f, ensure_ascii=False, indent=2)

    print(f"{len(valid_posts)} gültige Posts gespeichert in {output_path}")

def count_hashtags_for_post_date(posts_list, target_post_date):
    """
    Zählt alle Hashtags in Posts mit dem gegebenen post_date.
    Gibt ein Dictionary zurück: {hashtag: anzahl}
    """

    hashtag_counts = defaultdict(int)
    hashtag_pattern = re.compile(r"#\w+", re.UNICODE)

    for post in posts_list:
        if post.get("post_date", "").strip() != target_post_date:
            continue

        text_items = post.get("text", [])
        for entry in text_items:
            hashtags = hashtag_pattern.findall(entry)
            for tag in hashtags:
                hashtag_counts[tag.lower()] += 1  # Normalisiere auf lowercase

    # Übersicht ausgeben
    print(f"\n📅 Hashtags am {target_post_date}:")
    for tag, count in sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{tag}: {count}x")

    return dict(hashtag_counts)
