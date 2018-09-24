import argparse
import re
import time
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

# Input arguments to the program
parser = argparse.ArgumentParser (description='Provide the input parameters for the webcrawler')
parser.add_argument ("--max_depth", default=2, help='Maximum depth allowed for crawling')
parser.add_argument ("--unique_url_count", default=10, help="Maximum number of unique URLS in a crawl")
parser.add_argument ("--seed", default="https://en.wikipedia.org/wiki/Time_zone",
                     help="the seed URL to start crawling")
parser.add_argument ("--out_filename", default="crawledList", help="the filename to store the unique URL's crawled")
args = parser.parse_args ()

# Global Variables:

# variable to store the index of the files starting from 1 till 1000(at most)
FILE_INDEX = 1
# dictionary to store the file name and the corresponding URL
LINK_FILENAME_MAP = {}
# dictionary to store each unique URL crawled and their depth relative to the seed
URL_DEPTH_MAP = {}


# function which crawls the web following BFS
def webspider (seed):
    links_to_crawl = [seed]
    links_crawled = []
    links_at_nextdepth = []
    current_depth = 1
    while links_to_crawl and len (links_crawled) < args.unique_url_count and current_depth <= args.max_depth:
        current_crawl = links_to_crawl.pop (0)
        if current_crawl not in links_crawled:
            new_fetched_urls = get_all_urls (current_crawl)
            if new_fetched_urls is not None:
                update_to_crawl_list (links_at_nextdepth, new_fetched_urls)
                links_crawled.append (current_crawl)
                # respect politeness policy of the website
                time.sleep (1);
        if current_crawl not in URL_DEPTH_MAP:
            URL_DEPTH_MAP.update ({current_crawl: current_depth})
        # if all links at current depth is exhausted go to the next level
        if not links_to_crawl:
            links_to_crawl = links_at_nextdepth
            links_at_nextdepth = []
            current_depth = current_depth + 1
    return links_crawled


# helper function to keep the list updated for the crawler to crawl at the next depth
def update_to_crawl_list (links_at_nextdepth, new_fetched_urls):
    for url in new_fetched_urls:
        if url not in links_at_nextdepth:
            links_at_nextdepth.append (url)


# function to download the html content and write them to a file along with the URL
def write_html_content (current_crawl, html_content):
    global FILE_INDEX
    filename = 'file_' + str (FILE_INDEX) + '.txt'
    file_content = open (filename, 'a+')
    # storing the URL along with the page content
    file_content.write (current_crawl + '\n' + html_content.decode ())
    global LINK_FILENAME_MAP
    LINK_FILENAME_MAP.update ({filename: current_crawl})
    FILE_INDEX = FILE_INDEX + 1
    file_content.close ()


# helper function which support the webspider to retrieve urls based on the crawling policy
def get_all_urls (current_crawl):
    valid_url_list = []
    pattern = re.compile ('^/wiki/')
    base_url = "https://en.wikipedia.org/wiki"
    response = urllib.request.urlopen (current_crawl)
    html_content = BeautifulSoup (response, "html.parser")
    html_content.prettify ()
    write_html_content (current_crawl, html_content.encode ())
    # Get the links that obey the pattern
    body = html_content.find ('div', {'id': 'bodyContent'})
    links = body.find_all ('a', href=pattern)
    for link in links:
        if ":" not in link.get ('href'):
            url = urllib.parse.urljoin (base_url, link.get ('href'))
            if "#" in link.get ('href'):
                url = url[: url.index ('#')]
            if url not in valid_url_list:
                valid_url_list.append (url)
    return valid_url_list


# function which generates the file with the final list of unique urls
def crawled_url_list (links_crawled, outfh):
    for link in links_crawled:
        outfh.write (link)
        outfh.write ("\n")


def main ():
    outfilename = args.out_filename + ".txt";
    outfh = open (outfilename, "a+")
    start = time.time ()
    links_crawled = webspider (args.seed)
    end = time.time ()
    print (end - start)
    print (links_crawled)
    crawled_url_list (links_crawled, outfh)
    outfh.close ()

if __name__ == main ():
    main ()
