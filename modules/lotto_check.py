#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import sys


def get_results(url):
    ses = requests.sessions.session()
    resp = ses.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table", id="MB0")
    rows = table.find_all("tr")[1:-1]
    results = ""
    for row in rows:
        if row.find("p") != None:
            numbers = row.find("p").get_text(" ")
            results = " ".join([results, numbers])
        elif row.find("em") != None:
            numbers = row.find("em").get_text(" ")
            results = " ".join([results, numbers])
        else:
            pass
    results = results.strip().split(" ")
    return results


def check_winner(number, results):
    if number.isdigit():
        if str(number) in [result[-2:] for result in results]:
            return f"You'are winner with {number}!!!"
        else:
            return f"Good luck next time with {number}!"
    else:
        return f"Please recheck {number}"


def solve(numbers):
    url = "https://xskt.com.vn/"
    results = get_results(url)

    checked_result = ""
    for number in numbers:
        checked_result = "\n".join([check_winner(number, results), checked_result])
    return checked_result


def main():
    numbers = sys.argv[1:]

    print(solve(numbers))


if __name__ == "__main__":
    main()
