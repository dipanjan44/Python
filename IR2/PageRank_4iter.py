import operator

# Global variables:
# dictionary for all the pages and their corresponding inlinks
inlink_map = {}
# dictionary for all the pages and their corresponding outlinks
outlink_map = {}
# dictionary for the initial page rank for all the pages
last_page_rank_map = {}
# dictionary for the revised page rank for all the pages
new_page_rank_map = {}
# list of all the pages for which pagerank is calculated
page_list = []
# list of all pages that have no links to other pages
sink_page_list = []
# map containing URL's and page ranks in descending order
url_page_rank_map={}
# base_url
base_url="https://en.wikipedia.org/wiki/"
# damping factor
d = 0.85
# variable to extract the input file name
file_name=""


# parses the graph file given to it and calls functions to populate all the dictionaries
def parse_graph (graph):
    file_content = open (graph, 'r')
    for line in file_content.readlines ():
        words = line.split ()
        populate_inlink_dictionary (words)
        populate_page_list (words)
    populate_outlink_dictionary ()


# populates the inlink dictionary
def populate_inlink_dictionary (words):
    key = words[0]
    values = words[1:]
    inlink_map[key] = values


# populates the list maintaining all the pages
def populate_page_list (words):
    page_list.insert (0, words[0])


# populates the outlink dictionary
def populate_outlink_dictionary ():
    for key in inlink_map.keys ():
        for value in inlink_map[key]:
            if value in outlink_map.keys ():
                outlink_map[value] = outlink_map[value] + 1
            else:
                outlink_map[value] = 1


# populates the initial pagerank for all the pages
def calculate_startup_pagerank ():
    N = len (page_list)
    for page in page_list:
        last_page_rank_map[page] = float (1) / N
    populate_sink_pagelist ()


# populates sink_page_list with the sink pages
def populate_sink_pagelist ():
    for page in page_list:
        if page not in outlink_map.keys ():
            sink_page_list.insert (0, page)


# calculates the page rank
def pagerank_calculation ():
    iteration = 0
    calculate_startup_pagerank ()
    while iteration < 4:
        sink_page_rank = 0
        for page in sink_page_list:
            sink_page_rank = sink_page_rank + last_page_rank_map[page]
        for page in page_list:
            new_page_rank_map[page] = float (1 - d) / len (page_list)
            new_page_rank_map[page] += d * float (sink_page_rank / len (page_list))
            for inlink_page in inlink_map[page]:
                new_page_rank_map[page] = new_page_rank_map[page] + (
                        d * float (last_page_rank_map[inlink_page]) / float (outlink_map[inlink_page]))
        for page in page_list:
            last_page_rank_map[page] = new_page_rank_map[page]
        iteration = iteration + 1


# sorts and prints pages by their URL and PageRank Score (all pages)
def sort_page_rank_URL (page_rank_map):
    count=0
    file_page_rank = open (str(file_name)+"_SortedPageRank_URL_4iter_d" +str(d) + ".txt", "w+")
    file_page_rank.write ("******************PageRank******************" + "\n")
    file_page_rank.write ("The pages as per their URL and scores are : " + "\n")
    for docId in page_rank_map.keys ():
        new_key = base_url + str (docId)
        url_page_rank_map[new_key] = page_rank_map[docId]
    sorted_url_pagerank = sorted (url_page_rank_map.items (), key=operator.itemgetter (1), reverse=True)
    while count < len(sorted_url_pagerank):
        file_page_rank.write (str (sorted_url_pagerank[count]))
        file_page_rank.write ("\n")
        count=count+1
    file_page_rank.close()

# sorts and prints pages by their docID and PageRank Score
def sort_page_rank_docID (last_page_rank_map):
    count = 0
    sort_page_rank_URL(last_page_rank_map)
    sorted_dict = sorted (last_page_rank_map.items (), key=operator.itemgetter (1), reverse=True)
    file_page_rank = open (str (file_name) + "_SortedPageRank_docID_4iter_d" + str (d) + ".txt", "w+")
    file_page_rank.write ("******************PageRank******************" + "\n")
    file_page_rank.write ("The pages as per their docID and scores are : " + "\n")
    while count < len (sorted_dict):
        file_page_rank.write (str (sorted_dict[count]))
        file_page_rank.write ("\n")
        count = count + 1
    file_page_rank.close ()


# sorts and prints top 20 pages by their docID and inlink counts
def sort_in_link (inlink):
    temp_dict = {}
    file_in_link = open (str(file_name)+"_Sorted_Inlink_4iter_d"+str(d) + ".txt", "w+")
    file_in_link.write ("*******************InlinkStats*******************" +"\n")
    file_in_link.write ("The pages sorted in descending order of the Inlink count are :" +"\n")
    for page in inlink.keys ():
        temp_dict[page] = len (inlink.get (page))
    sorted_dict = sorted (temp_dict.items (), key=operator.itemgetter (1), reverse=True)
    count = 0
    while count < 20 and count < len (sorted_dict):
        file_in_link.write (str (sorted_dict[count]) +"\n")
        count += 1


# counts the number of pages with no in-links (sources) in the given dictionary
def count_sources (inlink_dict):
    counter = 0
    for page in inlink_dict.keys ():
        if not inlink_dict[page]:
            counter += 1
    return counter


# count the maximum in- degree for the graph
def max_in_degree ():
    max_in_degree = 0
    for key in inlink_map.keys ():
        values = inlink_map[key]
        current_length = len (values)
        if max_in_degree < current_length:
            max_in_degree = current_length
    return max_in_degree


# calculate the maximum out-degree for the graph
def max_out_degree ():
    max_out_degree = 0
    for key in outlink_map.keys ():
        value = outlink_map[key]
        if max_out_degree < value:
            max_out_degree = value
    return max_out_degree


# main method
def main ():
    graph = input ('Enter the filename containing the graph: ')
    global file_name
    file_name = graph.split (".")[0]
    parse_graph (str (graph))
    pagerank_calculation ()
    sort_page_rank_docID (new_page_rank_map)
    sort_in_link (inlink_map)


if __name__ == "__main__": main ()
