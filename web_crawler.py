#!/usr/bin/python3
import requests
import optparse
import re
import urllib.parse

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

    res = request(url)

    file_name = url.split("/")[-1]
    file_name = file_name.split('?')[0]

    if file_name != "" and res:
        file_name = path + file_name

        with open(file_name, "wb") as f:
            print("Crawling resource ---->> {}".format(file_name))
            f.write(res.content)


def extract_links_url(url):
    res = request(url)
    if res:
        return re.findall('(?:href=")(.*?)"', str(res.content))
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
