from helpers import tools
from helpers.tools import *

# STATIC VARIABLES
# urls
instagram_url                   = "https://instagram.com"
instagram_url_hashtag           = "https://www.instagram.com/explore/search/keyword/?q=%23"
instagram_hashtag_name          = "8mai1945"
instagram_url_hashtag_name      = instagram_url_hashtag + instagram_hashtag_name

# proxys
proxys                          = ["172.81.21.149", "172.81.20.42", "162.218.13.134", "52.128.216.149", "31.131.8.191", "23.226.24.61", "172.81.22.22", "31.131.10.15", "31.131.11.12", "172.81.23.168"]

# insta button classes
cookie_button                   = "button._a9--._ap36._a9_1"
login_button                    = "button._acan._acap._acas._aj1-._ap30"

# insta account username and password
instagram_account_name          = ["flipitberlin", "reputationplus.de", "immobilienkind", "luckygamblersberlin"]
instagram_account_password      = ["BigMillion#65", "BoostBewertungen25", "NeverStop50+", "BigMillion#65"]

# index of insta account to use
instagram_name                  = instagram_account_name[0]
instagram_password              = instagram_account_password[0]

# CREATE JSON FOLDER FOR IMAGES AND VIDEOS AND FILE NAMES
image_folder        = create_folder_if_missing(instagram_hashtag_name+"images")
video_folder        = create_folder_if_missing(instagram_hashtag_name+"videos")
json_file           = instagram_hashtag_name + ".json"

# count of posts to scrape
count_posts_to_scrape  = 100

# start index of post without text scraped yet
start_index         = has_no_text_index(json_file)

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
fillInputFieldBy(browser, By.NAME, "username", instagram_name)
fillInputFieldBy(browser, By.NAME, "password", instagram_password)
#clickButtonBy   (By.CSS_SELECTOR, login_button)
waiting(20)

#SCRAPE TEXT, IMAGES, VIDEOS
for i in range(count_posts_to_scrape):
    post_index = start_index + i
    all_posts_main = get_json_posts_as_list(json_file)
    post_url = get_url(all_posts_main[post_index])

    #OPEN POST URL
    openUrlInNewTab(browser, post_url)
    browser.refresh()
    waiting(get_random_in_range(5, 15))
    
    #ADD TEXT TO POST JSON FILE
    add_text_to_json_posts_mit_index(browser, post_index, json_file)

    #ADD POST DATES TO JSON FILE
    add_dates_to_json_posts(post_index, json_file)

    #ADD IMAGES AND VIDEOS
    all_posts_main = get_json_posts_as_list(json_file)
    all_posts_main[post_index]["image_path"]  =   save_media_from_post_url_updated(browser, image_folder, video_folder, post_url)
    with open(json_file, "w") as f:
        json.dump(all_posts_main, f, indent=2)

    print("DURCHGANG: " + str(post_index))








