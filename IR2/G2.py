import argparse
import collections
import re
import time
import urllib.parse
import urllib.request

import enchant
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize

# Input arguments to the program, default values are set as given in the problem statement of task1
parser = argparse.ArgumentParser (description='Provide the input parameters for the webcrawler')
parser.add_argument ("--max_depth", default=6, help='Maximum depth allowed for crawling')
parser.add_argument ("--unique_url_count", default=1000, help="Maximum number of unique URLS in a crawl")
parser.add_argument ("--keywords", default="green", help="The keyword to be searched")
parser.add_argument ("--seed", default="https://en.wikipedia.org/wiki/Carbon_footprint",
                     help="the seed URL to start crawling")
parser.add_argument ("--out_filename", default="G2.txt",
                     help="the filename to graph G2")
args = parser.parse_args ()

# Global Variables:
# dictionary to store each unique URL crawled and their depth relative to the seed
URL_DEPTH_MAP = {}

# Dictionary of English words to compare
dict_word_list = enchant.Dict ("en_US")


# function which crawls the web following BFS
def webspider (seed, keyword, bfs_graph):
    links_to_crawl = [seed]
    links_crawled = []
    links_crawled_at_currentdepth = []
    links_at_nextdepth = []
    current_depth = 1
    while links_to_crawl and len (links_crawled) < args.unique_url_count and current_depth <= args.max_depth:
        current_crawl = links_to_crawl.pop (0)
        if current_crawl not in links_crawled:
            new_fetched_urls = get_all_urls (current_crawl, keyword)
            if new_fetched_urls is not None:
                update_to_crawl_list (links_at_nextdepth, new_fetched_urls)
                links_crawled.append (current_crawl)
                links_crawled_at_currentdepth.append (current_crawl)
                webpage_map (current_crawl, new_fetched_urls, bfs_graph)
                # respect politeness policy of the website
                time.sleep (1);
            # update the information with depth and list of URL's at that depth
            URL_DEPTH_MAP.update ({current_depth: links_crawled_at_currentdepth})
        # if all links at current depth is exhausted go to the next level
        if not links_to_crawl:
            links_to_crawl = links_at_nextdepth
            links_crawled_at_currentdepth = []
            links_at_nextdepth = []
            current_depth = current_depth + 1
    return links_crawled


# helper function which support the webspider to retrieve urls based on the crawling policy
def get_all_urls (current_crawl, keywords_set):
    valid_url_list = []
    pattern = re.compile ('^/wiki/')
    base_url = "https://en.wikipedia.org/wiki"
    response = urllib.request.urlopen (current_crawl)
    html_content = BeautifulSoup (response, "html.parser")
    html_content.prettify ()
    # capture the url-directs
    url_redirects = html_content.find_all ("a", class_='mw-redirect')
    # skip the reference section
    if len (html_content.find ('ol', class_='references') or ()) > 1:
        html_content.find ('ol', class_='references').decompose ()
    # write_html_content (current_crawl, html_content.encode ())
    # Get the links that obey the pattern
    body = html_content.find ('div', {'id': 'bodyContent'})
    links = body.find_all ('a', href=pattern)
    for link in links:
        if link not in url_redirects:
            if '/wiki/MainPage' not in link.get ('href'):
                if ":" not in link.get ('href'):
                    url = urllib.parse.urljoin (base_url, link.get ('href'))
                    valid_keyword = keyword_checker (url, link.text, keywords_set)
                    if valid_keyword:
                        if "#" in link.get ('href'):
                            url = url[: url.index ('#')]
                        if url not in valid_url_list:
                            valid_url_list.append (url)
    return valid_url_list


# check the keyword or keywordchecker for validity
def keyword_checker (url, url_text, keywords):
    is_valid_keyword = None
    anchor_text = url_text
    link_text = url
    start = int (link_text.find ("/wiki/") + len ("/wiki/") - 1)
    start = start + 1
    temp = link_text
    link_text = temp[start:]

    anchor_text_tokens = word_tokenize (anchor_text)
    url_text_tokens = word_tokenize (link_text)
    for keyword in keywords:
        lower_case_keyword = keyword.lower ()
        # Check if the anchor or URL contains the keyword
        is_valid_anchor = anchor_text_checker (lower_case_keyword, anchor_text_tokens)
        is_valid_link = link_text_checker (lower_case_keyword, url_text_tokens)
        is_valid_keyword = is_valid_anchor or is_valid_link
    return is_valid_keyword


# is a valid dictionary word
def dict_presence (formatted_keyword_list):
    isPresent = False
    for keyword in formatted_keyword_list:
        if keyword != "" and len (keyword) != 0:
            if dict_word_list.check (keyword):
                isPresent = True
            else:
                isPresent = False
    return isPresent


def split_word (formatted_string, lower_case_keyword):
    isPresent = False
    start = formatted_string.find (lower_case_keyword)
    if lower_case_keyword == formatted_string:
        return True
    else:
        word_before = formatted_string[:start]
        word_after = formatted_string[start:]
        if word_before != "" and len (word_before) != 0:
            dict_word_list.check (word_before)
            isPresent = True
        if word_after != "" and len (word_after) != 0:
            dict_word_list.check (word_after)
            isPresent = True
    return isPresent


def link_text_checker (lower_case_keyword, url_text_tokens):
    for token in url_text_tokens:
        if lower_case_keyword in token.lower ():
            formatted_string = re.sub ("[!@#$%^&*()[]{};:,./<>?\|`~-=_+]", ' ', token.lower ())
            formatted_string = formatted_string.replace ("-", " ")
            formatted_string = formatted_string.replace ("_", " ")
            formatted_keyword_list = formatted_string.split (" ")
            # if dict_word_list.check(formatted_string.lower()) or dict_presence(formatted_keyword_list) or word_split(formatted_string, lower_case_keyword):
            if dict_presence (formatted_keyword_list) or split_word (formatted_string, lower_case_keyword):
                return True
            else:
                continue
    return False


def anchor_text_checker (lower_case_keyword, anchor_text_tokens):
    for token in anchor_text_tokens:
        if lower_case_keyword in token.lower ():
            formatted_string = re.sub ("[!@#$%^&*()[]{};:,./<>?\|`~-=_+]", ' ', token.lower ())
            formatted_string = formatted_string.replace ("-", " ")
            formatted_keyword_list = formatted_string.split (" ")
            if dict_word_list.check (token.lower ()) or dict_presence (formatted_keyword_list):
                return True
            else:
                continue
    return False


# helper function to keep the list updated for the crawler to crawl at the next depth
def update_to_crawl_list (links_at_nextdepth, new_fetched_urls):
    for url in new_fetched_urls:
        if url not in links_at_nextdepth:
            links_at_nextdepth.append (url)


# To extract the webpage docID from the URL
def extract_docId (url):
    extract_url = urllib.parse.urlparse (url)
    extract_path = extract_url.path
    article_id = extract_path.split ("/wiki/")[1]
    return article_id


# Populate the initial map with all the docID's
def webpage_map (current_url, new_fetched_urls, bfs_graph):
    article_id_current_page = extract_docId (current_url)
    article_id_list = []
    for url in new_fetched_urls:
        article_id_url_in_page = extract_docId (url)
        article_id_list.append (article_id_url_in_page)
    bfs_graph[article_id_current_page] = article_id_list


# Build the graph with in-links to each documents
def build_graph (bfs_graph):
    connected_graph = collections.OrderedDict ()
    for key in bfs_graph.keys ():
        connected_graph[key] = []
    for key in bfs_graph.keys ():
        values = bfs_graph[key]
        for value in values:
            if value in connected_graph.keys ():
                match_list = connected_graph[value]
                match_list.append (key)
                connected_graph[value] = match_list
    return connected_graph


# Write the output of the graph to a file
def write_graph_to_file (connected_graph, file_writer):
    for key in connected_graph.keys ():
        file_writer.write (key)
        for value in connected_graph[key]:
            file_writer.write (" ")
            file_writer.write (value)
        file_writer.write ("\n")


def main ():
    keywords_set = args.keywords.split (",")
    bfs_graph = collections.OrderedDict ()
    crawled_list = webspider (args.seed, keywords_set, bfs_graph)
    # print ("Printing the list of urls" + str (crawled_list))
    # print ("***************")
    # print ("Printing the bfs_graph" + str (bfs_graph))
    file_bfs = open (args.out_filename, "w+")
    connected_graph = build_graph (bfs_graph)
    # print ("***************")
    # print ("Printing the connected_graph" + str (connected_graph))
    write_graph_to_file (connected_graph, file_bfs)
    file_bfs.close ()


if __name__ == main ():
    main ()
