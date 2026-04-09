#!/usr/bin/python3
import requests
import sys

from bs4 import BeautifulSoup

link = sys.stdin.read()

response = requests.get(link)
response.raise_for_status()

page = BeautifulSoup(response.content, "html.parser")

content = page.body("div", "chapter-inner chapter-content")[0]

#Love this story? Find the genuine version on the author's preferred platform and support theid work!
#Love this novel? Read it on Royal Road to ensure the author gets credit.
#The narrative has been taken without autorization; if you see it on Amazon, report the incident.
#If you spot this tale on Amazon, know that it has been stolen. Report the violation.
#Taken from Royal Road, this narrative should be reported if found on Amazon.
#Help support creative writers by finding and reading their stories on the original site.
#Stolen novel; please report.
#You could be reading stolen content. Head to the original site for the genuine story.
#Unauthorized reproduction: this story has been taken without approval. Report sightings.
#<span><br>test</br></span>

html = BeautifulSoup("<!DOCTYPE html><html lang='en'><head></head><body></body></html>", "html.parser")
meta = html.new_tag("meta", charset="utf-8")
html.head.append(meta)

title = html.new_tag("title")
title.string = page.title.string
html.head.append(title)

html.body.append(content)

print(html.prettify())