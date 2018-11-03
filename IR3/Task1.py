import optparse
import os
from string import punctuation

from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner

# Input corpus
bfs_corpus = "/Users/dipanjan/PycharmProjects/Python/IR3/Input_Corpus/"
# Output corpus (Cleaned files)
clean_files = "/Users/dipanjan/PycharmProjects/Python/IR3/ProcessedFiles"


# Read the contents of the files from the folders
def process_bfs_corpus (bfs_corpus, choice):
    for filename in os.listdir (bfs_corpus):
        clean_html (filename, bfs_corpus, choice)


# Clean the html content from each file in the BFS corpus
def clean_html (filename, bfs_corpus, choice):
    current_file = open (bfs_corpus + filename, 'r')
    soup_extract = BeautifulSoup (current_file.read (), 'html.parser')
    current_file.close ()
    cleaned_contents = cleaned_content (soup_extract, choice)
    write_to_file (filename, cleaned_contents)


# Start the cleaning process
def cleaned_content (soup_extract, choice):
    clean_content = remove_tags (soup_extract, choice)
    return clean_content


# Remove unwanted tags from the parsed html object
def remove_tags (soup_extract, choice):
    nav_bar = soup_extract.find ('div', class_='mw-jump')
    page_footer = soup_extract.find ('div', class_='printfooter')
    page_site = soup_extract.find ('div', id='siteSub')
    if nav_bar:
        soup_extract.find ('div', class_='mw-jump').decompose ()

    if page_footer:
        soup_extract.find ('div', class_='printfooter').decompose ()

    if page_site:
        soup_extract.find ('div', id='siteSub').decompose ()
    html_cleaner = cleaner_parameters ()
    page_title = soup_extract.find ('title')
    page_body = soup_extract.find ('div', {'id': 'bodyContent'})
    soup_extract = html_cleaner.clean_html (str (page_title) + " " + str (page_body))
    clean_content = soup_cleaner (soup_extract, choice)
    return clean_content


# Apply case folding and remove punctuation
def soup_cleaner (soup_extract, choice):
    clean_content = BeautifulSoup (soup_extract, 'lxml').get_text ()
    clean_content = ' '.join (clean_content.split ())
    clean_content = clean_content.replace ('html ', '')
    clean_content = ''.join (content for content in clean_content if 0 < ord (content) < 127)
    if choice == "CF":
        clean_content = case_folding (clean_content)
    elif choice == "RP":
        clean_content = remove_punctuations (clean_content)
    # apply both for default where there is no choice
    else:
        clean_content = case_folding (clean_content)
        clean_content = remove_punctuations (clean_content)
    return clean_content


def case_folding (clean_content):
    clean_content = clean_content.lower ()
    return clean_content


# To remove punctuation characters from the content
def remove_punctuations (clean_content):
    clean_content = ''.join (characters for characters in clean_content if characters not in '}{][)(\><=')
    clean_content = ' '.join (
        token.strip (punctuation) for token in clean_content.split () if token.strip (punctuation))
    clean_content = ' '.join (token.replace ("'", "") for token in clean_content.split () if token.replace ("'", ""))
    clean_content = ' '.join (clean_content.split ())
    return clean_content


# create a cleaner object to chuck out unnecessary content
def cleaner_parameters ():
    reject_list = ['script', 'noscript', 'style', 'meta', 'semantics', 'img', 'label', 'table', 'li', 'ul',
                   'ol', 'nav', 'dl', 'dd', 'sub', 'sup', 'math']
    accept_list = ['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6' 'span', 'b', 'a', 'u', 'i', 'body']
    html_cleaner = Cleaner ()
    html_cleaner.remove_unknown_tags = True
    html_cleaner.processing_instructions = True
    html_cleaner.style = True
    html_cleaner.comments = True
    html_cleaner.scripts = True
    html_cleaner.javascript = True
    html_cleaner.meta = True
    html_cleaner.links = True
    html_cleaner.embedded = True
    html_cleaner.annoying_tags = True
    html_cleaner.frames = True
    html_cleaner.forms = True
    html_cleaner.remove_tags = accept_list
    html_cleaner.kill_tags = reject_list
    return html_cleaner


# Write the cleaned HTML corpus
def write_to_file (filename, corpus):
    folder = os.path.join (clean_files, filename)
    file_new = open (folder, "a+")
    file_new.write (str (corpus))
    file_new.close ()


# Take input from user and parse
def parse_input ():
    parser_for_input = optparse.OptionParser ()
    args = parser_for_input.parse_args ()
    return args


# Main Function
def main ():
    args = parse_input ()
    # Choice whether you want Case-folding or punctuation
    # For Case-Folding -> CF
    # For Removing Punctutaion -> RP
    # Default is both
    choice = args[1]
    process_bfs_corpus (bfs_corpus, choice)


if __name__ == "__main__":
    main ()
