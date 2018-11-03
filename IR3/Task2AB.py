import glob
import os

unigram_location = "/Users/dipanjan/PycharmProjects/Python/IR3/N-Grams/Unigram"
bigram_location = "/Users/dipanjan/PycharmProjects/Python/IR3/N-Grams/Bigram"
trigram_location = "/Users/dipanjan/PycharmProjects/Python/IR3/N-Grams/Trigram"


# inverted index for unigrams
def inverted_index_unigram ():
    inverted_index = {}
    final_inverted_list = {}

    dir_name = os.getcwd ()
    path = os.path.join (dir_name, 'TestFiles')
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
    for key, value in inverted_index.items ():
        temp_list = []
        [temp_list.extend ([k, v]) for k, v in value.items ()]
        final_inverted_list[key] = temp_list
        length = (len (temp_list)) // 2
        write_to_N_gram_file (key, temp_list, length, unigram_location)


# inverted index for bigrams
def inverted_index_bigram ():
    inverted_index = {}
    final_inverted_list = {}
    dir_name = os.getcwd ()
    path = os.path.join (dir_name, 'TestFiles')
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
        for k, v in inverted_index.items ():
            temp_list = []
            [temp_list.extend ([k, v]) for k, v in v.items ()]
            final_inverted_list[k] = temp_list
            length = (len (temp_list)) // 2
            write_to_N_gram_file (k, temp_list, length, bigram_location)


#  creates inverted index for trigrams
def inverted_index_trigram ():
    inverted_index = {}
    final_inverted_list = {}

    dir_name = os.getcwd ()
    path = os.path.join (dir_name, 'TestFiles')
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
    for k, v in inverted_index.items ():
        temp_list = []
        [temp_list.extend ([k, v]) for k, v in v.items ()]
        final_inverted_list[k] = temp_list
        length = (len (temp_list)) // 2
        write_to_N_gram_file (k, temp_list, length, trigram_location)


def write_to_N_gram_file (k, temp_list, length, location):
    # output format (Term: ['docId', frequency, 'docId', frequency,......,'docId',frequency]:Length of Inverted List)
    write_location = os.path.join (location, "result.txt")
    file_f = open (write_location, "a+")
    file_f.write (k + " : " + str (temp_list) + " : " + str (length))
    file_f.write ("\n")
    file_f.close ()


# main function
def main ():
    n = input ('Enter value of n for n-grams: ')

    if int (n) == 1:
        inverted_index_unigram ()
    elif int (n) == 2:
        inverted_index_bigram ()
    elif int (n) == 3:
        inverted_index_trigram ()
    else:
        print ("Please enter either 1 or 2 or 3!")


if __name__ == "__main__": main ()
