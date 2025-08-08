from pathlib import Path
from src import *
from src.collection import *
from src.collection.hashtag_posts_scraper import *

from src.filtering.date_filter import *
from src.filtering.metadata_filters import *
from src.visualization.topic_modelling import *
from src.visualization.network_visualization import *

######## SET MODE ########
mode = "scraper"

######## SET GENERAL PARAMETERS ########
base_path = Path(__file__).parent

######## SET SCRAPER PARAMETERS ########
hashtag             = "example_hashtag"         # FILL IN THE HASHTAG TO SCRAPE
scroll_count        = 2                         # FILL IN THE COUNT OF SCROLLING DOWN THE HASHTAG PAGE TO COLLECT THE URLs OF THE POSTS
max_posts_to_scrpae = 20                        # SET THE MAX SCRAPING AMOUNT OF NEW POSTS TO AVOID GETTING BANNED (max. 100 per day)

instagram_name      = "user_name"               # FILL IN THE USERNAME
instagram_password  = "password"                # FILL IN THE PASSWORD

use_proxy           = True
proxy_host          = "example_host"            # SET THE PROXY HOST 
proxy_port          = "example_port"            # SET THE PORT
proxy_user          = "example_user"            # SET THE PROXY USER
proxy_pass          = "example_password"        # SET THE PROXY PASSWORD
scraping_hidden     = False                     # HIDDEN SCRAPING CURRENTLY NOT POSSIBLE BECAUSE CLICKING COOKIE BUTTON AND LOGIN BUTTON STILL MANUEL

######## SET FILTER PARAMETERS ########
filter_target_date = "2025-01-22 00:00:00"                                             # CHOOSE A DATE TO FILTER FOR FORMAT: "2025-01-22 00:00:00"
filter_target_folder_path = "data\\posts_by_hashtags\\example_hashtag_foldername"      # CHOOSE FOLDER FROM WHERE YOU WANT TO FILTER POSTS BY DATE
filter_output_folder_path = "data\\filtered\\example_output_foldername"                # CHOOSE FOLDER NAME WHERE TO STORE THE FILTERED POSTS

######## SET TOPICS PARAMETERS ########
topics_output_filename   = "topics_first_visualization"
topics_inner_folder_path = "data\\posts_by_hashtags\\example_hashtag"                   # FOLDER OF THE POSTS THAT SHOULD BE ANALYZED BY THE TOPICS OF THERE CAPTIONS
######## SET NETWORK PARAMETERS ########
network_output_filename   = "networks_first_visualization" 
network_inner_folder_path = "data\\posts_by_hashtags\\example_hashtag"                  # FOLDER OF THE POSTS THAT SHOULD BE VISUALIZED BY HASHTAG NETWORKS

match mode:
    case "scraper":
        hashtag_post_scraper(base_path, hashtag, scroll_count, max_posts_to_scrpae, instagram_name, instagram_password, use_proxy, proxy_host, proxy_port, proxy_user, proxy_pass, scraping_hidden)

    case "filter":
        get_posts_by_date(filter_target_date, join_paths(base_path,filter_target_folder_path), join_paths(base_path,filter_output_folder_path))
    
    case "topics":
        get_topics(get_caption_list(base_path, topics_inner_folder_path, "caption"), 5, topics_output_filename)

    case "network":
        visualize_hashtag_cooccurrence(get_caption_hashtag_list(base_path, network_inner_folder_path, "caption_hashtags"), network_output_filename)