from collections import Counter
import nltk
from nltk import ngrams
import math
import random
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
nltk.download("gutenberg", quiet=True)

SF = {}
QF = {}

SR = {}
CR = {}

ignore_chars = {' ', ',', ';', '!', '.'}


def swap_mappings(d, pd):
    if len(d) < 2:
        print("Dictionary must have at least two keys to swap.")
        return d

    key1 = random.choices(list(pd.keys()), weights=pd.values())[0]
    key2 = random.choice(list(d.keys()))

    d[key1], d[key2] = d[key2], d[key1]

    return d


def frequency_analysis():
    global SF
    global QF

    from nltk.corpus import gutenberg
    text = gutenberg.raw()
    filtered_text = ''.join([char.lower()
                            for char in text if 'a' <= char <= 'z'])

    quadgrams = ngrams(filtered_text, 4)

    letter_count = Counter(filtered_text)
    quadgram_count = Counter(quadgrams)

    total_letters = sum(letter_count.values())
    total_quadgrams = sum(quadgram_count.values())

    SF = {letter: (count / total_letters) for letter,
          count in letter_count.items()}
    QF = {quadgram: freq / total_quadgrams for quadgram,
          freq in quadgram_count.items()}


def pd_preprocessing(ciphertext):
    global SR
    global CR

    text = ciphertext.lower()
    ciphertext_letter_count = Counter(
        char for char in text if char not in ignore_chars)
    total_ciphertext_letters = sum(ciphertext_letter_count.values())
    CF = {letter: (count / total_ciphertext_letters)
          for letter, count in ciphertext_letter_count.items()}

    dummy_index = 1
    while len(CF) < 26:
        CF[f"_dummy{dummy_index}"] = 0.0
        dummy_index += 1

    sorted_SF = sorted(SF.keys(), key=lambda x: SF[x])
    sorted_CF = sorted(CF.keys(), key=lambda x: CF[x])

    SR = {letter: rank for rank, letter in enumerate(sorted_SF, start=1)}
    CR = {letter: rank for rank, letter in enumerate(sorted_CF, start=1)}


def generate_probabilty_distribution(current_key):
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
    quadgrams = ngrams(text, 4)
    fitness = 0

    for quadgram in quadgrams:
        if quadgram in QF:
            fitness += math.log10(QF[quadgram])

    return fitness


def get_decrypted_text(ciphertext, current_key):
    return ''.join(current_key[char.lower()].upper() if char.isupper() else current_key[char.lower()]
                   if char.lower() in current_key else char
                   for char in ciphertext)


def substitution_decipher(ciphertext):
    frequency_analysis()

    unique_cipher_chars = list(set(ciphertext.lower()) - ignore_chars)
    lowercase_alphabets = [chr(i) for i in range(ord('a'), ord('z') + 1)]

    dummy_index = 1
    while len(unique_cipher_chars) < 26:
        unique_cipher_chars.append(f"_dummy{dummy_index}")
        dummy_index += 1

    random.shuffle(lowercase_alphabets)
    best_key = {key: value for key, value in zip(
        unique_cipher_chars, lowercase_alphabets)}
    best_key_fitness = getFitness(get_decrypted_text(ciphertext, best_key))

    pd_preprocessing(ciphertext.lower())

    for _ in range(100):
        checks = 0

        random.shuffle(lowercase_alphabets)
        best_iteration_key = {key: value for key, value in zip(
            unique_cipher_chars, lowercase_alphabets)}
        best_iteration_key_fitness = getFitness(
            get_decrypted_text(ciphertext, best_iteration_key))

        pd = generate_probabilty_distribution(best_iteration_key)

        while True:
            new_key = swap_mappings(best_iteration_key, pd)
            new_key_fitness = getFitness(
                get_decrypted_text(ciphertext, new_key))

            if new_key_fitness > best_iteration_key_fitness:
                best_iteration_key, best_iteration_key_fitness = new_key, new_key_fitness
                pd = generate_probabilty_distribution(new_key)
                checks = 0

            checks = checks + 1
            if checks >= 600:
                break

        if best_iteration_key_fitness > best_key_fitness:
            best_key, best_key_fitness = best_iteration_key, best_iteration_key_fitness

    print(get_decrypted_text(ciphertext, best_key))


if __name__ == "__main__":
    substitution_decipher(input())
