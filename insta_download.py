import random
import instaloader
import time

time.sleep(5)

proxies = [
    "http://iweber02:qp9dQbDM@172.81.21.149:29842",
    "http://iweber02:qp9dQbDM@172.81.20.42:29842",
    "http://iweber02:qp9dQbDM@162.218.13.134:29842",
    "http://iweber02:qp9dQbDM@52.128.216.149:29842",
    "http://iweber02:qp9dQbDM@31.131.8.191:29842",
    "http://iweber02:qp9dQbDM@23.226.24.61:29842",
    "http://iweber02:qp9dQbDM@172.81.22.22:29842",
    "http://iweber02:qp9dQbDM@31.131.10.15:29842",
    "http://iweber02:qp9dQbDM@31.131.11.12:29842",
    "http://iweber02:qp9dQbDM@172.81.23.168:29842",
]

# Randomly pick a proxy
proxy = random.choice(proxies)

# Set up proxy in Instaloader
L = instaloader.Instaloader()
L.context.proxy = proxy
L.login("kimwolf8525", "instatokdsai25!")

profile_name = "hamster_walker"
L.download_profile(profile_name, profile_pic=True)
