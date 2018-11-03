import os
import nltk
from nltk.util import ngrams

# Store the number of terms in each document in a separate data structure

corpus_location = "/Users/dipanjan/PycharmProjects/Python/IR3/TestFiles/"
Unigram_Location = "/Users/dipanjan/PycharmProjects/Python/IR3/N-Grams/Unigram"
Bigram_Location = "/Users/dipanjan/PycharmProjects/Python/IR3/N-Grams/Bigram"
Trigram_Location = "/Users/dipanjan/PycharmProjects/Python/IR3/N-Grams/Trigram"


# Write the contents of the Unigram to files
def write_uni_gram_contents(corpus_map, file_location, filename):
    # Format written to the file(Term, term frequency in the document)
    folder = os.path.join(file_location, filename)
    file_new = open(folder, "a+")
    file_new.write("Term" + " : " +"Term-Frequency" + "\n")
    for key, value in corpus_map.items():
        unigram = key[0] + " : "  + str(value)
        file_new.write(str(unigram))
        file_new.write("\n")
    file_new.close()


# Write the contents of the Bigram to files
def write_bi_gram_contents(corpus_map, file_location, filename):
    # Format written to the file(Term, documentID, term frequency in the document)
    folder = os.path.join(file_location, filename)
    file_new = open(folder, "a+")
    file_new.write ("Term" + " : " + "Term-Frequency" + "\n")
    for key, value in corpus_map.items():
        bigram= ' '.join(str(k) for k in key)
        temp_string = "(" + bigram + ")" + ": " + str(value)
        file_new.write(str(temp_string))
        file_new.write("\n")
    file_new.close()


# Write the contents of the Trigram to files
def write_tri_gram_contents(corpus_map, file_location, filename):
    # Format written to the file(Term, documentID, term frequency in the document)
    folder = os.path.join(file_location, filename)
    file_new = open(folder, "a+")
    file_new.write ("Term" + " : " + "Term-Frequency" + "\n")
    for key, value in corpus_map.items():
        trigram = ' '.join(str(k) for k in key)
        temp_string = "(" + trigram + ")" + " : "  + str(value)
        file_new.write(str(temp_string))
        file_new.write("\n")
    file_new.close()


# Read the contents of the corpus
def read_corpus_contents(file_location):
    for filename in os.listdir(file_location):
        current_file = open(file_location + filename,'r')
        tokens = get_all_tokens(current_file)
        current_file.close()
        build_n_grams(tokens, filename)

# Convert the contents of the file to tokens
def get_all_tokens(current_file):
    file_content = current_file.read()
    file_tokens = file_content.split(" ")
    return file_tokens

# To generate n-grams (where n = 1, 2, 3) from the corpus
def build_n_grams(tokens, filename):
    generate_uni_grams(tokens, filename)
    generate_bi_grams(tokens, filename)
    generate_tri_grams(tokens, filename)

# To generate unigrams from the corpus
def generate_uni_grams(tokens, filename):
    unigrams = ngrams(tokens, 1)
    corpus_map = nltk.FreqDist(unigrams)
    write_uni_gram_contents(corpus_map, Unigram_Location, filename)


# To generate bigrams from the corpus
def generate_bi_grams(tokens, filename):
    bigrams = ngrams(tokens, 2)
    corpus_map = nltk.FreqDist(bigrams)
    write_bi_gram_contents(corpus_map, Bigram_Location, filename)


# To generate trigrams from the corpus
def generate_tri_grams(tokens, filename):
    trigrams = ngrams(tokens, 3)
    corpus_map = nltk.FreqDist(trigrams)
    write_tri_gram_contents(corpus_map, Trigram_Location, filename)

# Main Function
def main():
    read_corpus_contents(corpus_location)

if __name__ == "__main__":
    main()