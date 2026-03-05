import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

API_SHORTEN = "https://clc.li/api/url/add"
API_LIST = "https://clc.li/api/urls"


def shorten_link(token, link):
    response = requests.post(
        API_SHORTEN,
        headers={"Authorization": f"Bearer {token}"},
        json={"url": link}
    )
    response.raise_for_status()

    api_response = response.json()

    if api_response.get("error"):
        raise requests.exceptions.HTTPError(api_response.get("message"))

    return api_response["shorturl"]


def count_clicks(token, link):
    response = requests.get(
        API_LIST,
        headers={"Authorization": f"Bearer {token}"},
        params={"short": link}
    )
    response.raise_for_status()

    api_response = response.json()

    if api_response.get("error"):
        raise requests.exceptions.HTTPError(api_response.get("message"))

    return api_response["data"]["clicks"]


def is_bitlink(url):
    return urlparse(url).netloc == "clc.li"


def main():
    load_dotenv()
    api_token = os.getenv("CLC_API_TOKEN")

    user_input = input("Введите ссылку: ").strip()

    if is_bitlink(user_input):
        print("Количество кликов:", count_clicks(api_token, user_input))
    else:
        print("Короткая ссылка", shorten_link(api_token, user_input))


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.RequestException as error:
        print("Ошибка:", error)