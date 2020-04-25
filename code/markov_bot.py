import collections
import numpy as np

def get_token_list(input_text):
    token_list = []
    cur_token = ""

    for char in input_text.strip():
        if char in " ": # get rid of spaces between tokens
            if len(cur_token) > 0:
                token_list.append(cur_token)
            cur_token = ""
        elif char in ",;!?.\n\t": # treat punctuation, decorative whitespace as a token
            if len(cur_token) > 0:
                token_list.append(cur_token)

            token_list.append(char)
            cur_token = ""
        else:
            cur_token += char

    return token_list

def is_valid_start(prev_char, key, mode):
    if mode == "shakespeare":
        return (prev_char in " \n\t" and key[0][0] != "\n")
    elif mode == "freedom":
        return (key[0][0].isupper())

    print("Something went wrong...")
    raise ValueError

def token_list_to_string(token_list):
    sent = token_list[0]
    if len(token_list) > 1:
        for token in token_list[1:]:
            if token not in ",;!?.\n\t":
                sent += " "
            sent += token
    return sent

def main():
    #filepath = "data/shakespeare_sonnets.txt"
    #mode = "shakespeare"

    filepath = "data/declaration_of_independence.txt"
    mode = "freedom"

    memory_size = 1

    with open(filepath, "r") as file:
        input_text = file.read()

        ### Get list of token
        all_tokens_list = get_token_list(input_text)

        ### Get counts, potential sentence beginnings ###
        freq_dict = {}
        sentence_heads = []
        for i in range(len(all_tokens_list)-memory_size):
            key = tuple(all_tokens_list[i:(i+memory_size)])

            ## Collect potential sentence starts
            if i > 0 and is_valid_start(all_tokens_list[i-1], key, mode):
                sentence_heads.append(key)

            ## Increment counts
            if key in freq_dict:
                if all_tokens_list[i+memory_size] in freq_dict[key]:
                    freq_dict[key][all_tokens_list[i+memory_size]] += 1
                else:
                    freq_dict[key][all_tokens_list[i+memory_size]] = 1
            else:
                freq_dict[key] = {all_tokens_list[i+memory_size]: 1}

        ### Get frequencies ###
        for key in freq_dict:
            total_count = sum(freq_dict[key].values())
            for inner_key in freq_dict[key]:
                freq_dict[key][inner_key] /= total_count

        ### Get start of sentence ###
        cur_memory = sentence_heads[np.random.randint(len(sentence_heads))]
        token_list = list(cur_memory)

        ### Generate sentence ###
        num_iters = 0
        while cur_memory[-1] not in ("!?."): # stop after reaching a natural sentence ending
            transitions = freq_dict[cur_memory]
            available_states = list(transitions.keys())
            transition_probs = [transitions[s] for s in available_states]

            next_token = np.random.choice(available_states, p = transition_probs) # randomly choose next state
            token_list.append(next_token)

            cur_memory = tuple((list(cur_memory) + [next_token])[1:]) # update value of current state

            if num_iters >= 300: # Failsafe
                break
            num_iters += 1

        sent = token_list_to_string(token_list)
        print("\n", sent, "\n", sep = "")

if __name__ == "__main__":
    main()
