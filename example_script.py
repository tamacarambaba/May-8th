import os
import asyncio
from TikTokApi import TikTokApi
from TT_Scraper import TT_Scraper

proxy = {
    "server": "http://172.81.22.22:29842",
    "username": "iweber02",
    "password": "qp9dQbDM",
}

ms_token = os.environ.get("ms_token", None)


async def get_video_ids_by_hashtag(hashtag, count=10):
    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=[ms_token],
            num_sessions=1,
            sleep_after=3,
            proxies=[proxy],
            browser=os.getenv("TIKTOK_BROWSER", "chromium"),
            headless=False
        )

        hashtag = api.hashtag(name=hashtag)
        video_ids = []

        async for video in hashtag.videos(count=count):
            video_ids.append(video.id)

        return video_ids


def fetch_ids_sync(hashtag, count=10):
    return asyncio.run(get_video_ids_by_hashtag(hashtag, count))


# Используем TT_Scraper
tt = TT_Scraper(wait_time=0.3, output_files_fp="data/")
ids = fetch_ids_sync("VE80", count=10)
tt.scrape_list(ids, scrape_content=True, clear_console=True)
