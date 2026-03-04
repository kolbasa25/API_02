import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

API_SHORTEN = "https://clc.li/api/url/add"
API_LIST = "https://clc.li/api/urls"


def shorten_link(link):
    r = requests.post(
        API_SHORTEN,
        headers={"Authorization": f"Bearer {TOKEN}"},
        json={"url": link}
    )
    r.raise_for_status()
    data = r.json()
    if data.get("error"):
        raise requests.exceptions.HTTPError(data.get("message"))
    return data["shorturl"]


def count_clicks(link):
    r = requests.get(
        API_LIST,
        headers={"Authorization": f"Bearer {TOKEN}"},
        params={"short": link}
    )
    r.raise_for_status()
    data = r.json()
    if data.get("error"):
        raise requests.exceptions.HTTPError(data.get("message"))
    return data["data"]["clicks"]


def is_bitlink(url):
    return urlparse(url).netloc == "clc.li"


def main():
    user_input = input("Введите ссылку: ").strip()

    if is_bitlink(user_input):
        clicks = count_clicks(user_input)
        print("Количество кликов:", clicks)
    else:
        short = shorten_link(user_input)
        print("Короткая ссылка", short)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.RequestException as e:
        print("Ошибка:", e)