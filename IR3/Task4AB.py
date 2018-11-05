import glob
import operator
import os


# Task 4A and 4B

# inverted index for unigrams
def inverted_index_unigram ():
    inverted_index = {}


    dir_name = os.getcwd ()
    path = os.path.join (dir_name, 'ProcessedFiles')
    for filename in glob.glob (os.path.join (path, '*.txt')):
        with open (filename) as current_file:
            head, tail = os.path.split (filename)
            file_key = tail.split (".")[0]
            doc = current_file.read ()
            tokens = doc.split ()
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
    return inverted_index


# inverted index for bigrams
def inverted_index_bigram ():
    inverted_index = {}

    dir_name = os.getcwd ()
    path = os.path.join (dir_name, 'ProcessedFiles')
    for filename in glob.glob (os.path.join (path, '*.txt')):
        with open (filename) as f:
            doc = f.read ()
            head, tail = os.path.split (filename)
            file_key = tail.split (".")[0]
            word_list = doc.split ()
            for i in range (len (word_list) - 1):
                word = word_list[i] + " " + word_list[i + 1]
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
        f.close ()
    return inverted_index


#  creates inverted index for trigrams
def inverted_index_trigram ():
    inverted_index = {}


    dir_name = os.getcwd ()
    path = os.path.join (dir_name, 'ProcessedFiles')
    for filename in glob.glob (os.path.join (path, '*.txt')):
        with open (filename) as f:
            doc = f.read ()
            head, tail = os.path.split (filename)
            file_key = tail.split (".")[0]
            word_list = doc.split ()
            for i in range (len (word_list) - 2):
                word = word_list[i] + " " + word_list[i + 1] + " " + word_list[i + 2]
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
        f.close ()
    return inverted_index


# build the term frequency for n-grams
def build_term_freq_table (inverted_index, ngram):
    term_freq = {}
    for term in inverted_index.keys ():
        freq = 0
        doc_dict = inverted_index[term]
        for doc_id in doc_dict.keys ():
            freq = freq + doc_dict.get (doc_id)
        term_freq[term] = freq
    sorted_term_freq = sorted (term_freq.items (), key=operator.itemgetter (1), reverse=True)
    write_term_freq (sorted_term_freq, ngram)
    return sorted_term_freq


# write term frequency to file
def write_term_freq (sorted_term_freq, ngram):
    out_file_name = "term_freq_table" + "_" + str (ngram) + ".txt"
    term_freq_table = open (out_file_name, 'w')
    term_freq_table.write ("Term " + " : " + "Term-Frequency" + "\n")
    for list in sorted_term_freq:
        term_freq_table.write (str (list[0]) + " : ")
        term_freq_table.write (str (list[1]))
        term_freq_table.write ("\n")
    term_freq_table.close ()


# build doc frequency and sorts lexicographically on term
def generate_doc_freq_table (inverted_index, ngram):
    doc_freq = {}
    for term in inverted_index:
        doc_list = []
        doc_dict = inverted_index[term]
        for doc_id in doc_dict:
            doc_list.append (doc_id)
        doc_freq[term] = doc_list
    sorted_doc_freq = sorted (doc_freq.items (), key=operator.itemgetter (0))
    write_doc_freq (sorted_doc_freq, ngram)
    return sorted_doc_freq


# write document frequency to file
def write_doc_freq (sorted_doc_freq_dict, ngram):
    out_file_name = "doc_freq_table" + "_" + str (ngram) + ".txt"
    doc_freq_table = open (out_file_name, 'w')
    doc_freq_table.write ("Term " + " : " + "Document-Id(s)" + " : " + " Document-Frequency" + "\n")
    for list in sorted_doc_freq_dict:
        doc_freq_table.write (str (list[0]) + " : ")
        doc_freq_table.write (str (list[1]) + " : ")
        list_length = len (list[1])
        doc_freq_table.write (str (list_length))
        doc_freq_table.write ("\n")
    doc_freq_table.close ()


# main function
def main ():
    n = input ('Enter value of n for n-grams: ')

    if int (n) == 1:
        index_unigram = inverted_index_unigram ()
        term_freq_table_unigram = build_term_freq_table (index_unigram, "unigram")
        doc_freq_table_unigram = generate_doc_freq_table (index_unigram, "unigram")
    elif int (n) == 2:
        index_bigram = inverted_index_bigram ()
        term_freq_table_bigram = build_term_freq_table (index_bigram, "bigram")
        doc_freq_table_unigram = generate_doc_freq_table (index_bigram, "bigram")
    elif int (n) == 3:
        index_trigram = inverted_index_trigram ()
        term_freq_table_trigram = build_term_freq_table (index_trigram, "trigram")
        doc_freq_table_trigram = generate_doc_freq_table (index_trigram, "trigram")
    else:
        print ("Please enter either 1 or 2 or 3!")


if __name__ == "__main__": main ()
