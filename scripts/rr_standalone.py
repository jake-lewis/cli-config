#!/usr/bin/python3
import re
import requests
import subprocess
import sys

from bs4 import BeautifulSoup

linkArg = sys.stdin.read()

def is_next_link(href):
    return href and re.compile(r"/fiction/\d+/.+/(\d+)/.+").search(href)

def render(url):
    response = requests.get(url)
    response.raise_for_status()

    # Page scraping
    page = BeautifulSoup(response.content, "html.parser")
    html = BeautifulSoup("<!DOCTYPE html><html lang='en'><head></head><body></body></html>", "html.parser")

    content = page.body("div", "chapter-inner chapter-content")[0]

    meta = html.new_tag("meta", charset="utf-8")
    html.head.append(meta)

    title = html.new_tag("title")
    title.string = page.title.string
    html.head.append(title)
    html.body.append(content)

    links = page.find_all(href=is_next_link, limit = 7)

    print("Reading '" + title.string + "'")

    # w3m rendering
    htmlStr = html.prettify()
    p = subprocess.Popen(
        ["w3m", "-T", "text/html", "-"],
        text=True,
        stdin=subprocess.PIPE,
    )

    # Manage tty state
    p.stdin.write(htmlStr)
    p.stdin.close()
    p.wait()
    sys.stdin = open("/dev/tty")

    # Manage next chapter prompt
    if len(links) > 4:
        answer = input("Next chapter? (Y/n): ").strip().lower() in ('', 'y', 'yes')
        sys.stdout.write("\033[F") # Move cursor up one line
        sys.stdout.write("\033[K") # Clear the line
        nextLink = "https://www.royalroad.com" + links[2]["href"]
        if answer:
            render(nextLink)
        else:
            print("Finished on '" + title.string + "'")
    else:
        print("All caught up on chapters!")

render(linkArg)
