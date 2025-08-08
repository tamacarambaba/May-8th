from src.helpers.dir_helpers import * 
from src.helpers.selenium_helpers import *
from src.helpers.webdriver_helper import *
from src.helpers.extraction_helpers import *

def hashtag_post_scraper(base_path, hashtag, scroll_count, max_posts_to_scrape, instagram_name, instagram_password, use_proxy, proxy_host, proxy_port, proxy_user, proxy_pass, scraping_hidden):

    ##########################################################
    # Getting important links
    ##########################################################
    instagram_start_url         = get_json_value_by_filename_and_key(base_path, "instagram_urls_and_patterns.json", "instagram_url")
    instagram_hashtag_url       = (get_json_value_by_filename_and_key(base_path, "instagram_urls_and_patterns.json", "instagram_hashtag_base_url") + hashtag)
    
    ##########################################################
    # CREATE NEW Hashtag Dir if necessary
    ##########################################################
    create_hashtag_dir(base_path, hashtag)

    ##########################################################
    # SET WEBDRIVER
    ##########################################################
    browser = get_chrome_driver(base_path, use_proxy, proxy_host, proxy_port, proxy_user, proxy_pass, scraping_hidden)
    check_proxy_connection(browser)

    ##########################################################
    # Login Process and Opening Hashtag Page
    ##########################################################
    waiting(5)
    openWebpage(browser, instagram_start_url)                                           # OPEN INSTAGRAM START PAGE TO LOGIN                                                         # open instagram on the browser
    browser.implicitly_wait(0.5)

    #ACCOUNT LOG IN
    #clickButtonBy   (By.CSS_SELECTOR, cookie_button)                                   # Cookie Button press "reject optional cookies"
    waiting(10)
    fillInputFieldBy(browser, By.NAME, "username", instagram_name)
    fillInputFieldBy(browser, By.NAME, "password", instagram_password)
    #clickButtonBy   (By.CSS_SELECTOR, login_button)
    waiting(20)

    openUrlInNewTab(browser, instagram_hashtag_url)                                     # OPEN INSTAGRAM HASHTAG PAGE TO SCROLL AND COLLECT THE POST LINKS
    

    ##########################################################
    # Collecting Post Links of x Posts
    ##########################################################    
    scroll_x_times(browser, scroll_count)                                               # SCROLLS X-TIMES TILL BROWSER END
    new_post_urls = collect_posting_urls_from_webpage(browser)
    print("RESULT: ", new_post_urls)

    ##########################################################
    # SCRAPING IMAGE, VIDEO AND TEXT by Post Urls
    ##########################################################
    counter = 0
    for post_url in new_post_urls:
        post_id = get_post_id(post_url)
        if create_post_dir(base_path, hashtag, post_id):
            post_folder_path = join_paths(join_paths(join_paths(base_path, get_json_value_by_filename_and_key(base_path, "dir_paths.json", "posts_by_hashtags_path")), hashtag), post_id)
            post_metadata_path = join_paths(post_folder_path, ("metadata_" + post_id + ".json"))

            #OPEN POST URL
            openUrlInNewTab(browser, post_url)
            browser.refresh()
            waiting(get_random_in_range(5, 15))

            #SCRAPE POST FULL TEXT AND ADD IT TO METADATA
            full_text           = get_text_from_opened_post_page(browser, base_path)
            caption             = get_caption(full_text)
            caption_hashtags    = get_caption_hashtags(caption)
            caption_language    = get_caption_language(caption)
            scrape_date         = datetime.now()
            post_date           = get_date(full_text, scrape_date)

            add_value_to_json_file(post_metadata_path , "post_id", post_id)
            add_value_to_json_file(post_metadata_path , "post_url", post_url)
            add_value_to_json_file(post_metadata_path , "post_datetime", str(post_date))
            add_value_to_json_file(post_metadata_path , "scrape_datetime", str(scrape_date))
            add_value_to_json_file(post_metadata_path , "caption", caption)
            add_value_to_json_file(post_metadata_path , "caption_hashtags", caption_hashtags)
            add_value_to_json_file(post_metadata_path , "full_text", full_text)
            add_value_to_json_file(post_metadata_path , "caption_language", caption_language)

            #SCRAPE POST METADATA


            #SCRAPE MEDIA BY URL
            save_media_from_post_url_updated(browser, post_folder_path, post_url)

            counter += 1
        if counter >= max_posts_to_scrape: break
    print("--> " +str(counter) + " NEW POSTS ADDED TO *" + hashtag + "* FOLDER.")