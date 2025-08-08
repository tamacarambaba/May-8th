import re
import yt_dlp
import requests
from datetime import datetime, timedelta
from src.helpers.generator import *
from src.helpers.json_helpers import *  
from src.helpers.selenium_helpers import *
from langdetect import detect, detect_langs, LangDetectException, DetectorFactory

def get_post_id(url):
    url = url.rstrip("/")
    return url.split("/p/")[1]

def get_date(text_list, scrape_date):

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

    post_date = uniform_date_format(post_date, scrape_date)
    return post_date

def uniform_date_format(insta_str: str, now: datetime) -> datetime:
    insta_str = insta_str.strip()

    # Minuten
    m = re.match(r"Vor (\d+) Minute[n]?", insta_str)
    if m:
        return now - timedelta(minutes=int(m.group(1)))

    # Stunden
    m = re.match(r"Vor (\d+) Stunde[n]?", insta_str)
    if m:
        return now - timedelta(hours=int(m.group(1)))

    # Heute
    if insta_str.lower() == "heute":
        return datetime(now.year, now.month, now.day)

    # Gestern
    if insta_str.lower() == "gestern":
        dt = now - timedelta(days=1)
        return datetime(dt.year, dt.month, dt.day)

    # Tage
    m = re.match(r"Vor (\d+) Tag[e]?", insta_str)
    if m:
        dt = now - timedelta(days=int(m.group(1)))
        return datetime(dt.year, dt.month, dt.day)

    # Wochen
    m = re.match(r"Vor (\d+) Woche[n]?", insta_str)
    if m:
        dt = now - timedelta(weeks=int(m.group(1)))
        return datetime(dt.year, dt.month, dt.day)

    # Monate
    m = re.match(r"Vor (\d+) Monat[e]?", insta_str)
    if m:
        months_ago = int(m.group(1))
        year = now.year
        month = now.month - months_ago
        while month <= 0:
            month += 12
            year -= 1
        return datetime(year, month, now.day)

    # Datum im selben Jahr (z. B. "1. Januar")
    m = re.match(r"(\d{1,2})\.\s+([A-Za-zäöüÄÖÜ]+)", insta_str)
    if m and len(insta_str.split()) == 2:
        day = int(m.group(1))
        month_name = m.group(2)
        month_map = {
            "Januar": 1, "Februar": 2, "März": 3, "April": 4,
            "Mai": 5, "Juni": 6, "Juli": 7, "August": 8,
            "September": 9, "Oktober": 10, "November": 11, "Dezember": 12
        }
        month = month_map[month_name]
        return datetime(now.year, month, day)

    # Datum mit Jahr (z. B. "1. Januar 2024")
    m = re.match(r"(\d{1,2})\.\s+([A-Za-zäöüÄÖÜ]+)\s+(\d{4})", insta_str)
    if m:
        day = int(m.group(1))
        month_name = m.group(2)
        year = int(m.group(3))
        month_map = {
            "Januar": 1, "Februar": 2, "März": 3, "April": 4,
            "Mai": 5, "Juni": 6, "Juli": 7, "August": 8,
            "September": 9, "Oktober": 10, "November": 11, "Dezember": 12
        }
        month = month_map[month_name]
        return datetime(year, month, day)
    
    return None

def get_caption_language(caption):
    """
    Fügt jedem Post-Dictionary in der Liste das Feld 'caption_language' hinzu.
    - Nutzt langdetect.detect() auf dem Feld 'caption'
    - Ignoriert alle Hashtags (Wörter, die mit '#' beginnen)
    - Bei Fehlern (z. B. leerer Text) wird 'unknown' eingetragen.
    """
    hashtag_pattern = re.compile(r'#\S+')
    
    # Hashtags entfernen
    cleaned = hashtag_pattern.sub("", caption).strip()
    
    try:
        # Sprache detektieren
        lang = detect(cleaned) if cleaned else "unknown"
    except LangDetectException:
        lang = "unknown"
  
    return lang

def get_caption(full_text):
    """
    Fügt jedem Instagram-Post-Dictionary das Feld 'caption' hinzu gemäß folgender Regeln:

    Case 1: Colab-Post
      Erkannt, wenn das erste Element in post['text'] dem Muster "<profilename>\nund <x> weitere" entspricht.
      - Ist texts[6] == "Bearbeitet", dann caption = texts[9]
      - Sonst caption = texts[7]

    Case 2: Zwei-Profile-Post
      Erkannt, wenn das erste Element in post['text'] dem Muster "<profilename>\nund\n<profilename>" entspricht.
      - Ist texts[4] == "Bearbeitet", dann caption = texts[7]
      - Sonst caption = texts[5]

    Case 3: Alle anderen
      - Ist texts[4] == "Bearbeitet", dann caption = texts[7]
      - Sonst caption = texts[5]

    Fehlende Indizes werden als leerer String behandelt.
    """
    pattern_colab = re.compile(r".+\nund \d+ weitere")
    pattern_two = re.compile(r".+\nund\n.+")

    caption = ""

    if full_text and pattern_colab.match(full_text[0]):
        # Case 1: Colab-Post
        if len(full_text) > 6 and full_text[6] == "Bearbeitet":
            caption = full_text[9] if len(full_text) > 9 else ""
        else:
            caption = full_text[7] if len(full_text) > 7 else ""

    elif full_text and pattern_two.match(full_text[0]):
        # Case 2: Zwei-Profile-Post
        if len(full_text) > 4 and full_text[4] == "Bearbeitet":
            caption = full_text[7] if len(full_text) > 7 else ""
        else:
            caption = full_text[5] if len(full_text) > 5 else ""

    else:
        # Case 3: Alle anderen
        if len(full_text) > 4 and full_text[4] == "Bearbeitet":
            caption = full_text[7] if len(full_text) > 7 else ""
        else:
            caption = full_text[5] if len(full_text) > 5 else ""

    return caption

def get_caption_hashtags(caption):

    # HASHTAG PATTERN FOR FILTERING CAPTION
    hashtag_pattern = re.compile(r"#\w+")
    hashtags = hashtag_pattern.findall(caption)

    return hashtags

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

def get_text_from_opened_post_page(browser, base_path):
    text_list = []
    text_elem_list = browser.find_elements(By.CLASS_NAME, get_json_value_by_filename_and_key(base_path, "instagram_urls_and_patterns.json", "post_full_text_class")) 
    switchToMostRightTab(browser)
    for elem in text_elem_list:
        text_list.append(elem.text)
    #browser.close()
    return text_list

def save_media_from_post_url_updated(browser, post_folder_path, post_url):
    
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
                    'outtmpl': os.path.join(post_folder_path, f"insta_video_post_{get_post_id(post_url)}_%(autonumber)s.%(ext)s"),
                    'format': 'bv*+ba/bv/b[ext=mp4]/bestvideo', 
                    'merge_output_format': 'mp4',
                    'noplaylist': True,
                    'quiet': False,
                    'ignoreerrors': True,
                    'cookiesfromfile': 'cookies_instagram.txt',
                }

                # STARTS DOWNLOAD
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([post_url])
            else:
                file_path = os.path.join(post_folder_path, f"insta_image_post_{get_post_id(post_url)}.jpg")
        
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
            waiting(get_random_in_range(3, 5))
            print("WEITER------>")
        else:
            print("XXXXXXXXXXXXXXXX LOOP STOPPED XXXXXXXXXXXXXXXX")
            break
    

    #DOWNLOAD IMAGES
    for img_counter, img_url in enumerate(img_urls):
        img_data = requests.get(img_url).content
        file_path = os.path.join(post_folder_path, f"insta_image_post_{get_post_id(post_url)}_{img_counter}.jpg")
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
            'outtmpl': os.path.join(post_folder_path, f"insta_video_post_{get_post_id(post_url)}_%(autonumber)s.%(ext)s"),
            'format': 'bv*+ba/bv/b[ext=mp4]/bestvideo',
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': False,
            'ignoreerrors': True,
            'cookiesfromfile': 'cookies_instagram.txt',
        }

        # STARTS DOWNLOAD
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([post_url])
    
    return True


