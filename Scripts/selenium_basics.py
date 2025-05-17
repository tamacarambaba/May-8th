from modulefinder import test
import re
import os
import time
import zipfile
import json
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import requests

'''
HASHTAG LIST
#8Mai
#8Mai1945
#TagDerBefreiung
#May8
#Veday
#Veday80
9Mai
TagDesSieges
May9
VictoryDay
ДеньПобеды
80летПобеды
9мая
'''

# GLOBAL VARIABLES
instagram_url                   = "https://instagram.com"
#instagram_url_hashtag           = "https://www.instagram.com/explore/search/keyword/?q=%238mai1945"
#instagram_url_hashtag           = "https://www.instagram.com/explore/search/keyword/?q=%238mai"
#instagram_url_hashtag           = "https://www.instagram.com/explore/search/keyword/?q=%23TagDerBefreiung"
#instagram_url_hashtag           = "https://www.instagram.com/explore/search/keyword/?q=%23Veday"
#instagram_url_hashtag           = "https://www.instagram.com/explore/search/keyword/?q=%23Veday80"

#instagram_url_hashtag           = "https://www.instagram.com/explore/search/keyword/?q=%239Mai"
#instagram_url_hashtag           = "https://www.instagram.com/explore/search/keyword/?q=%23TagDesSieges"
#instagram_url_hashtag           = "https://www.instagram.com/explore/search/keyword/?q=%23May9"
#instagram_url_hashtag           = "https://www.instagram.com/explore/search/keyword/?q=%23VictoryDay"
#instagram_url_hashtag            = "https://www.instagram.com/explore/search/keyword/?q=%23ДеньПобеды"
#instagram_url_hashtag           = "https://www.instagram.com/explore/search/keyword/?q=%2380летПобеды"
#instagram_url_hashtag           = "https://www.instagram.com/explore/search/keyword/?q=%239мая"
#instagram_url_hashtag               = "https://www.instagram.com/explore/search/keyword/?q=%23"


cookie_button                   = "button._a9--._ap36._a9_1"
login_button                    = "button._acan._acap._acas._aj1-._ap30"


instagram_account_name = ""
instagram_account_password = ""



json_file = "posts.json"

# DECLARATION GLOBAL VARIABLES
new_post_urls   = []
old_urls        = []
last_height     = 0
new_height      = 0


def waiting(seconds):
    time.sleep(seconds)

def newTab():
    browser.execute_script("window.open('');")

def switchToMostRightTab():
    browser.switch_to.window(browser.window_handles[-1])                                             

def openWebpage(url):
    browser.get(url)

def clickButtonBy(by, value_x):                                                                     # finds and clicks the button
    browser.find_element(by, value = value_x).click()                                               # by: which way is chosen to find elemnt in the source code (CSS_SELECTOR; NAME etc.)

def fillInputFieldBy(by, value_x, text):
    browser.find_element(by, value_x).send_keys(text)

def openUrlInNewTab(url):
    newTab()
    switchToMostRightTab()
    openWebpage(url)

def get_json_post_urls():
    with open(json_file, 'r', encoding="utf-8") as f:
        data = json.load(f)
    post_urls = [entry['post_url'] for entry in data if 'post_url' in entry]
    return post_urls

def get_json_post_by_index(index):
    return get_json_posts_as_list()[index]

def get_post_id(url):
    url = url.rstrip("/")
    return url.split("/p/")[1]

def add_urls_to_json():
    all_urls = []
    f = open(json_file, "r", encoding="utf-8")
    old_urls = get_json_post_urls()
    all_urls = get_json_posts_as_list()
    for url in new_post_urls:
        if url not in old_urls:
            all_urls.append({"post_id": get_post_id(url), "post_url": url, "image_path": "", "text": []})
    f = open(json_file, "w", encoding="utf-8")
    json.dump(all_urls, f, indent=2)                                                                            # .dump writes list components to json file | indent: json file structure (2 spaces for higher readability)
    
    all_urls.clear()
    old_urls.clear()
    new_post_urls.clear()

def get_json_post_count():
    f = open(json_file, "r", encoding="utf-8")
    json_urls = json.load(f)
    return len(json_urls)

def get_json_posts_as_list():
    f = open(json_file, "r", encoding="utf-8")
    json_urls = json.load(f)
    return json_urls

def get_text_from_post_url(url):
    openUrlInNewTab(url)
    browser.refresh()
    waiting(10)
    return browser.find_elements(By.CLASS_NAME, "x193iq5w")
    
def save_img_from_post_url(url):
    openUrlInNewTab(url)
    browser.refresh()
    waiting(10)
    image_path = os.path.join("images", f"insta_image_post_{get_post_id(url)}.jpg")
    
    img_element = browser.find_element(By.CSS_SELECTOR, "img.x5yr21d")
    img_url = img_element.get_attribute("src")
    img_data = requests.get(img_url).content

    with open(image_path, "wb", encoding="utf-8") as f:
        f.write(img_data)

def has_image_path(post):
    return bool(post.get("image_path"))

def has_text(post):
    return bool(post.get("text"))

def get_url(post):
    return post.get("post_url")

def add_img_to_json_posts():
    all_posts = []
    all_posts = get_json_posts_as_list()
    for post in all_posts:
        if not has_image_path(post):
            post["image_path"] = save_img_from_post_url(get_url(post))

def add_text_to_json_posts():
    all_posts = []
    all_posts = get_json_posts_as_list()
    for post in all_posts:
        if not has_text(post):
            post["text"] = get_text_from_post_url(get_url(post))
            

def scroll_till_end():
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def scroll_x_times(scroll_count):
    for i in range(scroll_count):
        scroll_till_end()
        waiting(10)





# COLLECTING ALL POSTING LINKS from current page AND STOREs THEM IN "post_urls"
def collect_posting_urls_from_webpage():
    post_elements = browser.find_elements(By.CSS_SELECTOR, 'a[href^="/p/"]')

    # Extract unique post URL
    seen = set()
    for elem in post_elements:
        href = elem.get_attribute("href")
        if href and href not in seen:
            new_post_urls.append(href)
            seen.add(href)

def print_collected_urls():
    # Output collected links
    print(f"Collected {len(new_post_urls)} post links.")
    for url in new_post_urls:
        print(url)


def get_chrome_driver(use_proxy=False, proxy=None, user_agent=None):
    PROXY_HOST = proxy
    PROXY_PORT = 29842
    PROXY_USER = 'iweber'
    PROXY_PASS = 'qp9dQbDM'
 
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
    #options.add_argument("--headless")                         # behaviour not visible on the machine
 
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



# SET UP BROWSER
browser = get_chrome_driver()                                                                       #webdriver.Chrome()                                                                         # choose chrome as browser
waiting(5)
openWebpage(instagram_url)                                                                          # open instagram on the browser
browser.implicitly_wait(0.5)

# ACCOUNG LOG IN
clickButtonBy   (By.CSS_SELECTOR, cookie_button)                                                    # Cookie Button press "reject optional cookies"
fillInputFieldBy(By.NAME, "username", instagram_account_name)
fillInputFieldBy(By.NAME, "password", instagram_account_password)
clickButtonBy   (By.CSS_SELECTOR, login_button)

# OPEN HASHTAG
waiting(5)
openUrlInNewTab(instagram_url_hashtag)
browser.refresh()
waiting(10)

old_post_urls = get_json_post_count()

scroll_x_times(10)
collect_posting_urls_from_webpage()
add_urls_to_json()

new_post_urls = get_json_post_count()

print("NEW POST URLS COLLECTED: " + str(new_post_urls - old_post_urls))
print("TOTAL POST URLS: " + str(new_post_urls))

#print_collected_urls()

#opneUrlInNewTab(post_urls[0]) 
#caption_elements = browser.find_elements(By.CLASS_NAME, "x193iq5w")
#caption_text = []

#for elem in caption_elements:
#    caption_text.append(elem.text)




#if caption_elements:
#    print("Caption:\n")
#    print(caption_elements[4].text)
#    print(caption_elements[5].text)
#    print(caption_elements[6].text)

waiting(1200)

browser.quit()                                                                                       # close the browser