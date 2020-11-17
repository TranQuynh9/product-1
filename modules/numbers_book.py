import requests
from bs4 import BeautifulSoup
import json


def table_of_numbers(url, **pairs):
    ses = requests.sessions.session()
    resp = ses.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    rows = soup.find("table").find_all("tr")[1:-1]

    for row in rows:
        text = row.get_text("|")
        pair = text[text.find("|") + 1 :].split("|")
        if len(pair) == 2:
            key = pair[0]
            value = pair[1]
            if key not in pairs:
                pairs[key] = value
            else:
                pairs[key] = (" - ").join([pairs[key], value])
    return pairs


def solve():
    result = {}
    urls = [
        "https://xskt.com.vn/so-mo/",
        "https://xskt.com.vn/so-mo/?pg=2",
        "https://xskt.com.vn/so-mo/?pg=3",
        "https://xskt.com.vn/so-mo/?pg=4",
        "https://xskt.com.vn/so-mo/?pg=5",
        "https://xskt.com.vn/so-mo/?pg=6",
    ]
    for url in urls:
        result = table_of_numbers(url, **result)
    return result


def main():
    with open("../data/numbers_book.json", "wt") as f:
        json.dump(solve(), f, indent=4)


if __name__ == "__main__":
    main()
