from helpers import tools
from helpers.tools import *

# STATIC VARIABLES
# urls
instagram_url                   = "https://instagram.com"
instagram_url_hashtag           = "https://www.instagram.com/explore/search/keyword/?q=%23"
instagram_hashtag_name          = "8mai1945"

# proxys
proxys                      = ["172.81.21.149", "172.81.20.42", "162.218.13.134", "52.128.216.149", "31.131.8.191", "23.226.24.61", "172.81.22.22", "31.131.10.15", "31.131.11.12", "172.81.23.168"]

# insta button classes
cookie_button                   = "button._a9--._ap36._a9_1"
login_button                    = "button._acan._acap._acas._aj1-._ap30"

# insta account username and password
instagram_account_name          = "reputationplus.de"
instagram_account_password      = "BoostBewertungen25"

# scrolls x times down on hashtag page
scrolling_down = 10

# CREATE JSON FILE FOR POSTS
json_file       = create_json_file_if_missing(instagram_hashtag_name)



##############################################################################################
# MAIN
##############################################################################################

#SET UP BROWSER
proxy           = proxys[get_random_in_range(0, len(proxys)-1)]
browser         = get_chrome_driver(True, proxy)
waiting(5)
openWebpage(browser, instagram_url)                                                                          # open instagram on the browser
browser.implicitly_wait(0.5)

#ACCOUNT LOG IN
#clickButtonBy   (By.CSS_SELECTOR, cookie_button)                                                    # Cookie Button press "reject optional cookies"
waiting(10)
fillInputFieldBy(browser, By.NAME, "username", instagram_account_name)
fillInputFieldBy(browser, By.NAME, "password", instagram_account_password)
#clickButtonBy   (By.CSS_SELECTOR, login_button)
waiting(10)

#OPEN HASHTAG PAGE
openUrlInNewTab(browser, (instagram_url_hashtag+instagram_hashtag_name))
browser.refresh()
waiting(10)

#COLLECT POST LINKS (ONLY NEW LINKS) AND STORE THEM IN THE <instagram_hashtag_name>.json
old_post_urls = get_json_post_count_updated(json_file)

scroll_x_times(browser, 2)
new_post_urls = collect_posting_urls_from_webpage(browser)
add_urls_to_json(json_file, new_post_urls)

new_post_urls = get_json_post_count(json_file)