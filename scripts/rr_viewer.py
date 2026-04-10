#!/usr/bin/python3
import requests
import sys

from bs4 import BeautifulSoup

link = sys.stdin.read()

response = requests.get(link)
response.raise_for_status()

page = BeautifulSoup(response.content, "html.parser")
html = BeautifulSoup("<!DOCTYPE html><html lang='en'><head></head><body></body></html>", "html.parser")

content = page.body("div", "chapter-inner chapter-content")[0]

meta = html.new_tag("meta", charset="utf-8")
title = html.new_tag("title")
title.string = page.title.string

html.head.append(meta)
html.head.append(title)
html.body.append(content)

print(html.prettify())