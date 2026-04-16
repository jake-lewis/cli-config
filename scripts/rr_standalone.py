#!/usr/bin/python3
import argparse
import requests
import subprocess
import sys

from bs4 import BeautifulSoup

def parse_args():
    parser = argparse.ArgumentParser(description="Read Royal Road stories chapter by chapter in-terminal, via w3m.")

    parser.add_argument(
        "url",
        type=str,
        help="The Royal Road chapter URL"
    )

    parser.add_argument(
        "--single-chapter", "-s",
        action="store_true",
        help="Single chapter only. Will not prompt to continue reading."
    )

    return parser.parse_args()

def replace_prev_line(replacement = ""):
    sys.stdout.write("\033[F") # Move cursor up one line
    sys.stdout.write("\033[K") # Clear the line
    if replacement:
        print(replacement)

def render(url, single_chapter = False):
    response = requests.get(url)
    response.raise_for_status()

    # Page scraping
    page = BeautifulSoup(response.content, "html.parser")
    html = BeautifulSoup("<!DOCTYPE html><html lang='en'><head></head><body></body></html>", "html.parser")

    content = page.body("div", "chapter-inner chapter-content")[0]
    keywords = page.select("meta[name=keywords]")[0]['content'].split("; ")
    story_name = keywords[0]
    chapter_title = keywords[2]

    meta = html.new_tag("meta", charset="utf-8")
    html.head.append(meta)

    title = html.new_tag("title")
    title.string = story_name + " | " + chapter_title
    html.head.append(title)
    html.body.append(content)

    print("Reading\t\t- '" + title.string + "'")

    # w3m rendering
    html_str = html.prettify()
    p = subprocess.Popen(
        ["w3m", "-T", "text/html", "-"],
        text=True,
        stdin=subprocess.PIPE,
    )

    # Manage tty state
    p.stdin.write(html_str)
    p.stdin.close()
    p.wait()
    sys.stdin = open("/dev/tty")

    # Manage output & next chapter behaviour
    if single_chapter:
        sys.exit(0)

    next_link = page.select("link[rel=next]")
    read_next = False

    if next_link:
        read_next = input("Next chapter? (Y/n): ").strip().lower() in ('', 'y', 'yes')
        replace_prev_line()
        if read_next:
            render("https://www.royalroad.com" + next_link[0]['href'])

    if not read_next:
        replace_prev_line("Finished on\t- '" + title.string + "'")

    if not next_link:
        print("All caught up on chapters!")

if __name__ == "__main__":
    try:
        args = parse_args()
        render(args.url, args.single_chapter)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    sys.exit(0)