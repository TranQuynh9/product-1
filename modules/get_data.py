#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
import datetime


class get_data:
    def __init__(self):
        self.list = []

    def get_request(self, url):
        ses = requests.sessions.session()
        resp = ses.get(url)

        return resp

    def github_jobs(self, url):
        resp = self.get_request(url)
        jobs = resp.json()

        for job in jobs:
            self.list.append((job["title"], job["html_url"]))
        try:
            url = resp.links["next"]["url"]
            self.github_jobs(url)
        except:
            return self.list

        return self.list

    def get_links_by_label(self, url, label):
        soup = BeautifulSoup(self.get_request(url).text, "html.parser")

        links = soup.find_all("h3", attrs={"itemprop": "name"})
        for link in links:
            self.list.append(str(link.a))
            if len(self.list) == 10 and label == "Lastest":
                return self.list

        try:
            url = soup.find("a", attrs={"id": "Blog1_blog-pager-older-link"}).get(
                "href"
            )
            self.get_links_by_label(url, label)
        except:
            return self.list

        return self.list


def get_posts_by_label(label):
    if label == "Lastest":
        url = "https://www.familug.org"
    else:
        url = "https://www.familug.org/search/label/{}".format(label)

    posts = get_data().get_links_by_label(url, label)

    return posts


def solve():
    posts = {}
    labels = ["Python", "Command", "sysadmin", "Lastest"]

    for label in labels:
        posts[label] = get_posts_by_label(label)

    API = "https://api.github.com/repos/awesome-jobs/vietnam/issues"

    jobs = get_data().github_jobs(API)

    return {"jobs": jobs, "posts": posts}


def main():
    data = solve()
    data["update_time"] = datetime.datetime.now().strftime("%a, %d %b at %H:%M:%S")
    with open("../data/data.json", "wt") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    main()
