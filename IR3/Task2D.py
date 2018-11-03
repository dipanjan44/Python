import os

# Generate a unigram index storing the positions
corpus_location = "/Users/dipanjan/PycharmProjects/Python/IR3/TestFiles/"
unigram_Location = "/Users/dipanjan/PycharmProjects/Python/IR3/N-Grams/PositionalUnigram"


# Read the contents of the corpus to create an index
def generate_positional_unigram (corpus_location):
    for filename in os.listdir (corpus_location):
        current_file = open (corpus_location + filename)
        tokens = generate_tokens (current_file)
        current_file.close ()
        positional_unigram = n_grams_gaps (tokens, filename)
        generate_file_positional_unigram (positional_unigram, filename)

# Generate tokens from the file
def generate_tokens (file):
    content = file.read ()
    tokens = content.split (" ")
    return tokens

# n_grams with positions encoded with gaps
def n_grams_gaps (tokens, filename):
    corpus_map_with_positions = build_positional_n_grams (tokens, filename)
    for token in corpus_map_with_positions.keys ():
        d_gap_list = []
        docID, count, position = corpus_map_with_positions[token]
        # print("Before D Gap" + str(position))
        for i in range (0, len(position)):
            if (i == 0):
                value = position[0]
                d_gap_list.append (value)
            else:
                value = position[i] - position[i - 1]
                d_gap_list.append (value)
        corpus_map_with_positions[token]=[docID,count,d_gap_list]
        # print("After D Gap" + str(d_gap_list))
    return corpus_map_with_positions


# n-grams with positions
def build_positional_n_grams (tokens, filename):
    corpus_map_with_positions = {}
    for index, token in enumerate (tokens):
        if token in corpus_map_with_positions.keys ():
            docID, count, position = corpus_map_with_positions[token]
            count = count + 1
            position.append (index)
            corpus_map_with_positions[token] = [docID, count, position]
        else:
            corpus_map_with_positions[token] = [filename, 1, [index]]
    return corpus_map_with_positions


# Write the inverted Index with positions encoded with gaps to file
def generate_file_positional_unigram (corpus_map_with_positions, filename):
    # outfile format (Term : documentID : term frequency : [positions in the document])
    folder = os.path.join (unigram_Location, filename)
    current_file = open (folder, "a+")
    current_file.write("Term : documentID : term frequency : [positions in the document]" +"\n")
    for term in corpus_map_with_positions.keys():
        documentId, count, positions = corpus_map_with_positions[term]
        term = str (term)
        current_file.write (term)
        current_file.write (" : ")
        documentId = str (documentId)
        current_file.write (documentId)
        current_file.write (" : ")
        count = str (count)
        current_file.write (count)
        current_file.write (" : ")
        current_file.write("[")
        for position in positions:
            current_file.write (" ")
            position = str (position)
            current_file.write (position)
        current_file.write (" ]")
        current_file.write ("\n")
    current_file.close ()


# Main Function
def main ():
    generate_positional_unigram (corpus_location)


if __name__ == "__main__":
    main ()
