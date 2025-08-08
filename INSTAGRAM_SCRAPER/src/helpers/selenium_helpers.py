import time
from src.helpers.generator import *
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException


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
    return list(post_urls)

