from collections import Counter
import math
import random

SF = {}
QF = {}

SR = {}
CR = {}

ciphertext_chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '@', '#', '$',
                    'z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n']
lowercase_alphabets = [chr(i) for i in range(ord('a'), ord('z') + 1)]


def swap_mappings(d, pd):
    n_d = d.copy()

    key1 = random.choices(list(pd.keys()), weights=pd.values())[0]
    key2 = random.choice(list(pd.keys()))
    while key2 == key1:
        key2 = random.choice(list(pd.keys()))

    temp = n_d[key1]
    n_d[key1] = n_d[key2]
    n_d[key2] = temp

    return n_d


def frequency_analysis():
    global SF
    global QF

    with open("big.txt", "r", encoding="utf-8") as file:
        text = file.read()
        filtered_text = ''.join([char.lower()
                                for char in text if char.isalpha()])

        quadgrams = [tuple(filtered_text[i:i+4])
                     for i in range(len(filtered_text) - 3)]

        letter_count = Counter(filtered_text)
        quadgram_count = Counter(quadgrams)

        total_letters = sum(letter_count.values())
        total_quadgrams = sum(quadgram_count.values())

        SF = {letter: (count / total_letters) for letter,
              count in letter_count.items()}
        QF = {quadgram: (count / total_quadgrams) for quadgram,
              count in quadgram_count.items()}


def pd_preprocessing(ciphertext):
    global SR
    global CR

    text = ciphertext.lower()
    ciphertext_letter_count = Counter(
        char for char in text if char in ciphertext_chars)
    total_ciphertext_letters = sum(ciphertext_letter_count.values())

    for char in ciphertext_chars:
        if char not in ciphertext_letter_count:
            ciphertext_letter_count[char] = 0

    CF = {letter: (count / total_ciphertext_letters)
          for letter, count in ciphertext_letter_count.items()}

    sorted_SF = sorted(SF.keys(), key=lambda x: SF[x])
    sorted_CF = sorted(CF.keys(), key=lambda x: CF[x])

    SR = {letter: rank for rank, letter in enumerate(sorted_SF, start=1)}
    CR = {letter: rank for rank, letter in enumerate(sorted_CF, start=1)}


def generate_probability_distribution(current_key):
    heuristic_values = {}
    for letter in CR:
        decrypted_letter = current_key[letter]
        heuristic_values[letter] = max(
            1, abs(CR[letter] - SR[decrypted_letter]))

    total_heuristics = sum(heuristic_values.values())
    if total_heuristics == 0:
        return {k: 1 / len(heuristic_values) for k in heuristic_values}
    return {k: v / total_heuristics for k, v in heuristic_values.items()}


def getFitness(text):
    filtered_text = ''.join([char.lower() for char in text if char.isalpha()])
    quadgrams = [tuple(filtered_text[i:i+4])
                 for i in range(len(filtered_text) - 3)]

    fitness = 0
    for quadgram in quadgrams:
        if quadgram in QF:
            fitness += math.log(QF[quadgram])
        else:
            fitness += math.log(1e-10)

    return fitness


def get_decrypted_text(ciphertext, current_key):
    return ''.join(current_key[char.lower()].upper() if char.isupper() else current_key[char.lower()]
                   if char.lower() in current_key else char
                   for char in ciphertext)


def get_key_and_fitness(ciphertext):
    random.shuffle(lowercase_alphabets)

    key = {key: value for key, value in zip(
        ciphertext_chars, lowercase_alphabets)}
    fitness = getFitness(get_decrypted_text(ciphertext, key))

    return key, fitness


def substitution_decipher(ciphertext):
    frequency_analysis()

    best_key, best_key_fitness = get_key_and_fitness(ciphertext)

    pd_preprocessing(ciphertext)

    for _ in range(100):
        checks = 0

        best_iteration_key, best_iteration_key_fitness = get_key_and_fitness(
            ciphertext)

        pd = generate_probability_distribution(best_iteration_key)

        while True:
            new_key = swap_mappings(best_iteration_key, pd)
            new_key_fitness = getFitness(
                get_decrypted_text(ciphertext, new_key))

            checks = checks + 1

            if new_key_fitness > best_iteration_key_fitness:
                best_iteration_key, best_iteration_key_fitness = new_key.copy(), new_key_fitness
                pd = generate_probability_distribution(best_iteration_key)
                checks = 0

            if checks >= 600:
                break

        if best_iteration_key_fitness > best_key_fitness:
            best_key, best_key_fitness = best_iteration_key, best_iteration_key_fitness

        print(f"\nIteration: {_ + 1}, Fitness: {best_key_fitness}")
        print("Current Decrypted Text:",
              get_decrypted_text(ciphertext, best_key), "\n")

    sorted_key = sorted(best_key.items(), key=lambda item: item[1])
    print("Final Key:", "".join(k for k, v in sorted_key))
    print("Final Decrypted Text:", get_decrypted_text(ciphertext, best_key))


if __name__ == "__main__":
    substitution_decipher(input("Enter Ciphertext: "))
