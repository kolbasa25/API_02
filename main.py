import os
import argparse
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

SHORTEN_URL_ENDPOINT = "https://clc.li/api/url/add"
GET_URLS_ENDPOINT = "https://clc.li/api/urls"


def shorten_link(token, link):
    response = requests.post(
        SHORTEN_URL_ENDPOINT,
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
        GET_URLS_ENDPOINT,
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
    parser = argparse.ArgumentParser(
        description='Сокращает ссылку или показывает количество кликов'
    )
    parser.add_argument('link', help='Ссылка для обработки')
    args = parser.parse_args()

    try:
        load_dotenv()
        api_token = os.environ["CLC_API_TOKEN"]

        user_input = args.link.strip()

        if is_bitlink(user_input):
            print("Количество кликов:", count_clicks(api_token, user_input))
        else:
            print("Короткая ссылка", shorten_link(api_token, user_input))
    except requests.exceptions.RequestException as error:
        print("Ошибка:", error)


if __name__ == "__main__":
    main()