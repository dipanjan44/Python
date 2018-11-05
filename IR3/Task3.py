import os


# Task3
corpus_location = "/Users/dipanjan/PycharmProjects/Python/IR3/TestFiles/"
slider = 5  # value of K
term1 = "jump"  # the first search term
term2 = "Billion"  # the second search term


# Read the contents of the corpus to create an index

def generate_positional_unigram_file_list (corpus_location, slider, term1, term2):
    document_set = set ()
    outfile = open ("Proximity_list" + "_" + str (slider) +"_" +term1 + "_" +term2 + ".txt", 'a+')
    outfile.write ("documentID" + " : " + " { term1 : [positions]} , { term2 : [positions]}" +"\n")
    for filename in os.listdir (corpus_location):
        current_file = open (corpus_location + filename)
        tokens = get_tokens (current_file)
        current_file.close ()
        corpus_map_with_positions = build_positional_unigram (tokens, filename)
        # Convert all the tokens  and search terms to lower case to handle case-insensitivity
        corpus_map_with_positions = {k.lower (): v for k, v in corpus_map_with_positions.items ()}
        term1=term1.lower()
        term2=term2.lower()

        if (term1 in corpus_map_with_positions.keys () and term2 in corpus_map_with_positions.keys ()):
            term1_position_list = corpus_map_with_positions[term1].__getitem__ (2)
            term2_position_list = corpus_map_with_positions[term2].__getitem__ (2)
            for element in term1_position_list:
                for item in term2_position_list:
                    if abs (element - item) <= slider:
                        file_key = filename.split (".")[0]
                        document_set.add (str (file_key) + " : " + " { " + str (term1) + " : " + str (
                            term1_position_list) + " } ," + " { " + str (term2) + " : " + str (
                            term2_position_list) + " } ")

    for entry in document_set:
        outfile.write (str (entry) + "\n")


# Generate tokens from the file
def get_tokens (file):
    content = file.read ()
    tokens = content.split (" ")
    return tokens


# n-grams with positions
def build_positional_unigram (tokens, filename):
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


# Main Function
def main ():
    generate_positional_unigram_file_list (corpus_location, slider, term1, term2)


if __name__ == "__main__":
    main ()
