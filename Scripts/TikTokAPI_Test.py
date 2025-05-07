from TikTokApi import TikTokApi
import asyncio
import os

ms_token = "8JwLYHq9fIDWo4KcdnVCxb8AKaVxxMuTTCedclqz2FKNRvcZEgRio9ixHG46-tQoivQp30Pwl9gC7ikHgeM9z0_r6B0_wLCmEdDlgh17Ylw-vNRLuJX_0cQI1pw-W7qPFHJL2x76A4PDw2xJxuXO0Zc0" # set your own ms_token


async def trending_videos():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "chromium"))
        async for video in api.trending.videos(count=30):
            print(video)
            print(video.as_dict)


if __name__ == "__main__":
    asyncio.run(trending_videos())