import collections

def get_word_list(input_text):
    word_list = []
    cur_word = ""

    for char in input_text.strip():
        if char in " \n\t" and len(cur_word) > 0:
            word_list.append(cur_word)
            cur_word = ""
        elif char in ",!?.":
            if len(cur_word) > 0:
                word_list.append(cur_word)

            word_list.append(char)
            cur_word = ""
        else:
            cur_word += char

    return word_list

def main():
    filepath = "data/declaration_of_independence.txt"

    with open(filepath, "r") as file:
        input_text = file.read()

        word_list = get_word_list(input_text)

        freq_dict = collections.defaultdict(int)
        for tuple in (zip(word_list[:-2], word_list[1:-1], word_list[2:])):
            freq_dict[tuple] += 1

        for key in freq_dict:


        print(freq_dict)


if __name__ == "__main__":
    main()
