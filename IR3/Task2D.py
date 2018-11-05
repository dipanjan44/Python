import os

# Task2D

corpus_location = "/Users/dipanjan/PycharmProjects/Python/IR3/ProcessedFiles/"
positional_unigram_Location = "/Users/dipanjan/PycharmProjects/Python/IR3/N-Grams/PositionalUnigram"

file_map = {}
corpus_unique_token_set = set ()


# Read the contents of the corpus to create an index
def generate_positional_unigram (corpus_location):
    for filename in os.listdir (corpus_location):
        current_file = open (corpus_location + filename)
        tokens = generate_tokens (current_file)
        current_file.close ()
        n_grams_gaps (tokens, filename)


# Generate tokens from the file
def generate_tokens (file):
    file_content = file.read ()
    tokens = file_content.split (" ")
    for token in tokens:
        corpus_unique_token_set.add (token)
    return tokens


# n_grams with positions encoded with gaps
def n_grams_gaps (tokens, filename):
    corpus_map_with_positions = positional_unigram (tokens, filename)
    for token in corpus_map_with_positions.keys ():
        d_gap_list = []
        docID, count, position = corpus_map_with_positions[token]
        # print("Before D Gap" + str(position))
        for i in range (0, len (position)):
            if (i == 0):
                value = position[0]
                d_gap_list.append (value)
            else:
                value = position[i] - position[i - 1]
                d_gap_list.append (value)
        corpus_map_with_positions[token] = docID, count, d_gap_list
        # print("After D Gap" + str(d_gap_list))
    file_map[filename] = corpus_map_with_positions


# n-grams with positions
def positional_unigram (tokens, filename):
    corpus_map_with_positions = {}
    file_key = filename.split (".")[0]
    for index, token in enumerate (tokens):
        if token in corpus_map_with_positions.keys ():
            docID, count, position = corpus_map_with_positions[token]
            count = count + 1
            position.append (index)
            corpus_map_with_positions[token] = docID, count, position
        else:
            corpus_map_with_positions[token] = file_key, 1, [index]
    return corpus_map_with_positions


# # Write the inverted Index with positions encoded with gaps to individual file
# def write_to_file_positional_unigram (corpus_map_with_positions, filename):
#     # outfile format (Term : documentID : term frequency : [positions in the document])
#     folder = os.path.join (unigram_Location, filename)
#     current_file = open (folder, "a+")
#     current_file.write ("Term : documentID : term frequency : [positions in the document]" + "\n")
#     for term in corpus_map_with_positions.keys ():
#         documentId, count, positions = corpus_map_with_positions[term]
#         term = str (term)
#         current_file.write (term)
#         current_file.write (" : ")
#         documentId = str (documentId)
#         current_file.write (documentId)
#         current_file.write (" : ")
#         count = str (count)
#         current_file.write (count)
#         current_file.write (" : ")
#         current_file.write ("[")
#         for position in positions:
#             current_file.write (" ")
#             position = str (position)
#             current_file.write (position)
#         current_file.write (" ]")
#         current_file.write ("\n")
#     current_file.close ()


def write_to_single_postional_unigram_file ():
    folder = os.path.join (positional_unigram_Location, "Positional_Unigram_gaps.txt")
    current_file_write = open (folder, "a+")
    for token in corpus_unique_token_set:
        current_file_write.write (token + " : ")
        inverted_list_info = []
        for k, v in file_map.items ():
            if token in v.keys ():
                inverted_list_info.append (str (v.get (token)))
                current_file_write.write (str (v.get (token)))
        current_file_write.write ("\n")


# Main Function
def main ():
    generate_positional_unigram (corpus_location)
    write_to_single_postional_unigram_file ()



if __name__ == "__main__":
    main ()
