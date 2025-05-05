from TT_Scraper import TT_Scraper

# Configure the scraper, this step is always needed
tt = TT_Scraper(wait_time=0.3, output_files_fp="test_folder/")

# Download all metadata as a .json and all content as .mp4/.jpeg
tt.scrape_list(ids = [7498540589986663726], scrape_content = True, clear_console=True)

# scrape user profile
tt.scrape_user(username="tagesschau", download_metadata=True)
