import os
import random
import asyncio
from TikTokApi import TikTokApi
from TT_Scraper import TT_Scraper

proxies = [{'server': 'http://172.81.21.149:29842', 'username': 'iweber02', 'password': 'qp9dQbDM'}, {'server': 'http://172.81.20.42:29842', 'username': 'iweber02', 'password': 'qp9dQbDM'}, {'server': 'http://162.218.13.134:29842', 'username': 'iweber02', 'password': 'qp9dQbDM'}, {'server': 'http://52.128.216.149:29842', 'username': 'iweber02', 'password': 'qp9dQbDM'}, {'server': 'http://31.131.8.191:29842', 'username': 'iweber02', 'password': 'qp9dQbDM'},
           {'server': 'http://23.226.24.61:29842', 'username': 'iweber02', 'password': 'qp9dQbDM'}, {'server': 'http://172.81.22.22:29842', 'username': 'iweber02', 'password': 'qp9dQbDM'}, {'server': 'http://31.131.10.15:29842', 'username': 'iweber02', 'password': 'qp9dQbDM'}, {'server': 'http://31.131.11.12:29842', 'username': 'iweber02', 'password': 'qp9dQbDM'}, {'server': 'http://172.81.23.168:29842', 'username': 'iweber02', 'password': 'qp9dQbDM'}]

ms_token = os.environ.get("ms_token", None)

with open("unique_ids.txt", "r") as f:
    unique_ids = set(line.strip() for line in f if line.strip())

hashtags_by_lang = {
    "en": ["VictoryDay", "Veday80"],
    "de": ["9Mai", "TagDesSieges"],
    "ru": ["ДеньПобеды", "80летПобеды", "9мая"]
}


async def get_video_ids_by_hashtag(hashtag, count):
    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=[ms_token],
            num_sessions=1,
            sleep_after=3,
            proxies=[random.choice(proxies)],
            browser=os.getenv("TIKTOK_BROWSER", "chromium"),
            headless=False
        )

        hashtag = api.hashtag(name=hashtag)
        video_ids = []

        async for video in hashtag.videos(count):
            video_id = video.id
            if video_id in unique_ids:
                continue

            unique_ids.add(video_id)
            video_ids.append(video_id)

            if len(video_ids) >= count:
                break

        return video_ids


def fetch_ids_sync(hashtag, count):
    return asyncio.run(get_video_ids_by_hashtag(hashtag, count))


for lang, hashtags in hashtags_by_lang.items():
    for tag in hashtags:
        output_dir = os.path.join("data", lang, tag)
        os.makedirs(output_dir, exist_ok=True)

        print(f"🔍 Data collection for #{tag} ({lang})")

        # Сбор ID
        ids = fetch_ids_sync(tag, count=100)

        # Скрейпинг видео
        tt = TT_Scraper(wait_time=0.3, output_files_fp=output_dir)
        tt.scrape_list(ids, scrape_content=True, clear_console=True)

with open("unique_ids.txt", "w") as f:
    for uid in sorted(unique_ids):
        f.write(uid + "\n")
