import time
import zipfile
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# GLOBAL VARIABLES
instagram_url                   = "https://instagram.com"
instagram_url_hashtag_8mai1945  = "https://www.instagram.com/explore/search/keyword/?q=%238mai1945"

cookie_button                   = "button._a9--._ap36._a9_1"
login_button                    = "button._acan._acap._acas._aj1-._ap30"


instagram_account_name = "reputationplus.de"
instagram_account_password = "BoostBewertungen25"

# DECLARATION GLOBAL VARIABLES
post_urls = []

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

def opneUrlInNewTab(url):
    newTab()
    switchToMostRightTab()
    openWebpage(url) 


# COLLECTING ALL POSTING LINKS from current page AND STOREs THEM IN "post_urls"
def collect_posting_urls_from_webpage():
    post_elements = browser.find_elements(By.CSS_SELECTOR, 'a[href^="/p/"]')

    # Extract unique post URL
    seen = set()
    for elem in post_elements:
        href = elem.get_attribute("href")
        if href and href not in seen:
            post_urls.append(href)
            seen.add(href)

def print_collected_urls():
    # Output collected links
    print(f"Collected {len(post_urls)} post links.")
    for url in post_urls:
        print(url)


## PROXY
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
 
 
    # service = Service(executable_path='/home/brahmani/Downloads/chromedriver-linux64/chromedriver')
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
 
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(options=options)
    return driver



browser = get_chrome_driver()                                                                       #webdriver.Chrome()                                                                         # choose chrome as browser
waiting(5)
openWebpage(instagram_url)                                                                           # open instagram on the browser
browser.implicitly_wait(0.5)

clickButtonBy   (By.CSS_SELECTOR, cookie_button)                                                     # Cookie Button press "reject optional cookies"
fillInputFieldBy(By.NAME, "username", instagram_account_name)
fillInputFieldBy(By.NAME, "password", instagram_account_password)
clickButtonBy   (By.CSS_SELECTOR, login_button)

waiting(5)
opneUrlInNewTab(instagram_url_hashtag_8mai1945)
browser.refresh()
waiting(10)

collect_posting_urls_from_webpage()
print_collected_urls()

opneUrlInNewTab(post_urls[0]) 
caption_elements = browser.find_elements(By.CLASS_NAME, "x193iq5w")

if caption_elements:
    print("Caption:\n")
    print(caption_elements[4].text)
    print(caption_elements[5].text)
    print(caption_elements[6].text)

waiting(1200)

browser.quit()                                                                                       # close the browser