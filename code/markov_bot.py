import collections
import numpy as np

def get_word_list(input_text):
    word_list = []
    cur_word = ""

    for char in input_text.strip():
        if char in " \n\t" and len(cur_word) > 0: # get rid of whitespace
            word_list.append(cur_word)
            cur_word = ""
        elif char in ",!?.": # treat punctuation as a token
            if len(cur_word) > 0:
                word_list.append(cur_word)

            word_list.append(char)
            cur_word = ""
        else:
            cur_word += char

    return word_list

def main():
    filepath = "data/declaration_of_independence.txt"
    memory_size = 2

    with open(filepath, "r") as file:
        input_text = file.read()

        word_list = get_word_list(input_text)

        ### Get counts ###
        freq_dict = {}
        for i in range(len(word_list)-memory_size):
            key = tuple(word_list[i:(i+memory_size)])
            if key in freq_dict:
                if word_list[i+memory_size] in freq_dict[key]:
                    freq_dict[key][word_list[i+memory_size]] += 1
                else:
                    freq_dict[key][word_list[i+memory_size]] = 1
            else:
                freq_dict[key] = {word_list[i+memory_size]: 1}

        ### Get frequencies ###
        for key in freq_dict:
            total_count = sum(freq_dict[key].values())
            for inner_key in freq_dict[key]:
                freq_dict[key][inner_key] /= total_count

        ### Get start of sentence ###

        ### Generate sentence ###

        print(freq_dict)

if __name__ == "__main__":
    main()
