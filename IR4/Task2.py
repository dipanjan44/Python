import glob
import os
import math
import operator

queryFile = "/Users/dipanjan/PycharmProjects/Python/IR4/QueryFile.txt"

doc_map = {}
term_freq = {}
constant=1500


# inverted index for unigrams
def inverted_index_unigram ():
    inverted_index = {}
    dir_name = os.getcwd ()
    path = os.path.join (dir_name, 'TestFiles')
    for filename in glob.glob (os.path.join (path, '*.txt')):
        with open (filename) as current_file:
            head, tail = os.path.split (filename)
            file_key = tail.split (".")[0]
            doc = current_file.read ()
            tokens = doc.split ()
            doc_map[file_key] = len (tokens)
            for word in tokens:
                if word not in inverted_index.keys ():
                    doc_dict = {file_key: 1}
                    inverted_index[word] = doc_dict
                elif file_key in inverted_index[word]:
                    doc_dict = inverted_index[word]
                    value = doc_dict.get (file_key)
                    value = value + 1
                    doc_dict[file_key] = value
                else:
                    doc_dict = {file_key: 1}
                    inverted_index[word].update (doc_dict)
        current_file.close ()
    # print(inverted_index)
    # print (doc_map)
    return inverted_index


def read_query (queryFile):
    query_map = {}
    with open (queryFile) as current_file:
        for line in current_file:
            tokens = line.strip ().split (" ")
            query_map[tokens[0]] = tokens[1:]
    #print(query_map)
    return query_map


def find_scores ():
    query_map = read_query (queryFile)
    index_map = inverted_index_unigram ()
    doc_score_query={}
    for k, v in query_map.items ():
        # get the query terms  from the query map
        search_query = query_map.get (k)
        doc_score_term = {}
        print(search_query)
        # pick each query term and check whether it exists in the corpus
        document_score_query=0
        for term in search_query:
            if term not in index_map.keys ():
                break
            else:
                doc_list={}
                doc_map={}
                # if query term exists , fetch the inverted list for that term
                print (" The search term is : " + str (term))
                inverted_list_search_term = index_map.get (term)
                print ("The inverted list for the search term : " + str (inverted_list_search_term))
                # print("The inverted list for search term:->   :" +word +" : " +str(inverted_list_search_term))
                all_doc_score_word=0
                for docId in inverted_list_search_term.keys():
                    document_length = calculate_doc_length (docId)
                    print ("The document length for documentId : " + str (
                        docId) + " is : " + str (document_length))
                    search_term_frequency_in_document = inverted_list_search_term.get (docId)
                    print ("The search term frequency in document :" + str (search_term_frequency_in_document))
                    search_term_frequency_in_corpus = term_frequency_in_corpus (term)
                    print ("The search term frequency in corpus :" + str (search_term_frequency_in_corpus))
                    corpus_length = get_corpus_length ()
                    print ("The corpus length :" + str (corpus_length))
                    numerator=(search_term_frequency_in_document + (search_term_frequency_in_corpus/corpus_length)*constant)
                    denominator=document_length+constant
                    curr_score_for_term=math.log(numerator/denominator)
                    print("The current score is : " + str(term) + " : " +str(curr_score_for_term))
                    # add curr_score for the doc in a map with the docid
                    doc_map[docId]=curr_score_for_term
                # Make a list with all the documents for a given term
                doc_list.update(doc_map)
            # create a map with all the list of documents and their score for a given term
            doc_score_term[term]=doc_list
            print("This is the doc_store_map : " +str(doc_score_term))
        # Logic to add the document score for the terms of the same query
        add_doc_score={}
        for entry in doc_score_term.keys():
            temp_map= doc_score_term.get(entry)
            for item in temp_map.keys():
                if item in add_doc_score.keys():
                    value= add_doc_score.get(item)
                    value = value+temp_map.get(item)
                    add_doc_score[item]=value
                else:
                    add_doc_score[item]=temp_map.get(item)
        doc_score_query[k]=add_doc_score
        print("The doc score for the query is : " +str(doc_score_query))
    return doc_score_query


def rank_docs():
    doc_score_query_map=find_scores()
    final_scored_map_in_order={}
    print("This is the latest method :" +str(doc_score_query_map))
    for queryId,values in doc_score_query_map.items():
        doc_val_map=doc_score_query_map.get(queryId)
        sorted_doc_val_map=sorted(doc_val_map.items(), key=operator.itemgetter(1),reverse=True)
        final_scored_map_in_order[queryId]=sorted_doc_val_map
    print("The final sorted output is : " +str(final_scored_map_in_order))
    return final_scored_map_in_order


def write_to_file_ranked_documents():
    ranked_docs=rank_docs()
    print("The ranked docs map is : "+str(len(ranked_docs)))
    for k in ranked_docs.keys():
        print("The value of k is :" +k)
        doc_list=ranked_docs.get(k)
        print("The doc list is " +str(doc_list))
        count=0
        file = open ("query_" + k + "_outfile.txt", "w+")
        while(count < len(doc_list) and count < 100):
            file.write(k +" , Q0 , " +str(doc_list[count]) +" , " +"LMD" +"\n")
            count=count+1
        file.close()

# calculate the document length for a given docId
def calculate_doc_length (docId):
    if docId in doc_map.keys ():
        doc_length = doc_map.get (docId)
    return doc_length


# Calculate the frequency of a given term from the query in the corpus
def term_frequency_in_corpus (word):
    if word in term_freq.keys ():
        frequency = term_freq.get (word)
    return frequency


# Calculate the total numbers of words on the entire corpus
def get_corpus_length ():
    # Calculate the total no of words in the corpus = |C|
    value = 0
    for term in term_freq.keys ():
        value = value + term_freq.get (term)
    return value


# build the term frequency for n-grams
def build_term_freq_table (inverted_index, ngram):
    for term in inverted_index.keys ():
        freq = 0
        doc_dict = inverted_index[term]
        for doc_id in doc_dict.keys ():
            freq = freq + doc_dict.get (doc_id)
        term_freq[term] = freq
    return term_freq


# main function
def main ():
    n = 1
    if int (n) == 1:
        index_unigram = inverted_index_unigram ()
        build_term_freq_table (index_unigram, "unigram")
        find_scores()
        rank_docs()
        write_to_file_ranked_documents()


if __name__ == "__main__": main ()
