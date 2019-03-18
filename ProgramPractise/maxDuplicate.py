

import operator
word_dict={}


def max_duplicate_word(filepath):
    with open(filepath, "r") as f:
        lines=f.readlines()
        for line in lines:
            word_list=line.strip().split(" ")
            for word in word_list:
                if word in word_dict.keys():
                    word_dict[word]=word_dict[word]+1
                else:
                    word_dict[word]=1
    print (word_dict)
    sorted_wordlist= sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_wordlist[0]


def main():
    filepath = '/Users/dipanjan/Desktop/test.txt'
    print(max_duplicate_word(filepath))


if __name__=="__main__": main()
