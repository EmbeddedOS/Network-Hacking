#!/usr/bin/python3
import requests
import optparse
import re
import urllib.parse
import os

# Crawling all resources with a specific URL: python3 web_crawler.py --path /home/larva/Downloads/tmp/ --url https://udemy.com/

links = []
path = "./"


def request(url):
    try:
        return requests.get(url)
    except Exception as e:
        pass


def download(url):
    global path

    try:
        res = request(url)

        file_path = urllib.parse.urlparse(url).path

        if os.path.basename(file_path) != "" and res:
            file_path = path + file_path
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "wb") as f:
                print("Crawling resource ---->> {}".format(file_path))
                f.write(res.content)

    except Exception as e:
        pass


def extract_links_url(url):
    res = request(url)

    if res:
        href_links = re.findall('(?:href=")(.*?)"', str(res.content))
        src_links = re.findall('(?:src=")(.*?)"', str(res.content))

        return href_links + src_links

    return []


def crawl(url):
    print("Crawling URL: {}".format(url))
    global links

    href_links = extract_links_url(url)
    for link in href_links:
        link = urllib.parse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if link not in links:
            links.append(link)
            download(link)
            crawl(link)


def main():
    global links, path

    parser = optparse.OptionParser()

    parser.add_option("-u", "--url", dest="url",
                      help="Target URL.")

    parser.add_option("-p", "--path", dest="path",
                      help="Resource storing path.")
    (options, arguments) = parser.parse_args()

    if not options.url:
        parser.error("Please specify an URL.")

    url = str(options.url)

    if options.path:
        path = str(options.path)

    crawl(url)


if __name__ == "__main__":
    main()
