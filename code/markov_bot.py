import collections
import numpy as np

def get_word_list(input_text):
    word_list = []
    cur_word = ""

    for char in input_text.strip():
        if char in " \n\t": # get rid of whitespace
            if len(cur_word) > 0:
                word_list.append(cur_word)
            cur_word = ""
        elif char in ",;!?.": # treat punctuation as a token
            if len(cur_word) > 0:
                word_list.append(cur_word)

            word_list.append(char)
            cur_word = ""
        else:
            cur_word += char

    return word_list

def main():
    filepath = "data/shakespeare_sonnets.txt"
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
        sent = "From fairest"
        cur_memory = tuple(sent.split())

        ### Generate sentence ###
        num_iters = 0
        while cur_memory[-1] not in ("!?."): # stop after reaching a natural sentence ending
            transitions = freq_dict[cur_memory]
            available_states = list(transitions.keys())
            transition_probs = [transitions[s] for s in available_states]

            next_word = np.random.choice(available_states, p = transition_probs) # randomly choose next state

            if next_word not in ",;!?.":
                sent += " "
            sent += next_word

            cur_memory = tuple((list(cur_memory) + [next_word])[1:]) # update value of current state

            if num_iters >= 300: # Failsafe
                break
            num_iters += 1

        print(sent)
        #print(freq_dict)

if __name__ == "__main__":
    main()
