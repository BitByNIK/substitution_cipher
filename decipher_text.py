from collections import Counter
import nltk
from nltk import bigrams
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context
nltk.download("gutenberg", quiet=True)

SF = {}
SDF = {}
DF = {}
DDF = {}


def frequency_analysis(standard, text=""):
    global SF
    global SDF
    global DF
    global DDF

    if standard:
        from nltk.corpus import gutenberg
        text = gutenberg.raw()

    letters = [char.lower() for char in text if char.isalpha()]
    total_letters = len(letters)

    bigram_list = list(bigrams(letters))

    letter_count = Counter(letters)
    bigram_count = Counter(bigram_list)
    total_bigrams = sum(bigram_count.values())

    temp1 = {letter: (count / total_letters) * 100 for letter,
             count in letter_count.items()}
    temp2 = {bigram: (count / total_bigrams) * 100 for bigram,
             count in bigram_count.items()}

    if standard:
        SF, SDF = temp1, temp2
    else:
        DF, DDF = temp1, temp2


def getFitness():
    letter_diff = sum(abs(SF[chr(i + 97)] - DF.get(chr(i + 97), 0.0))
                      for i in range(26))
    bigram_diff = sum(abs(SDF.get((chr(i + 97), chr(j + 97)), 0.0) - DDF.get((chr(i + 97), chr(j + 97)), 0.0))
                      for i in range(26) for j in range(26))

    return (1 - (letter_diff + bigram_diff) / 4) ** 8


def substitution_decipher(ciphertext):
    frequency_analysis(True)

    ignore_chars = {' ', ',', ';', '!', '.'}
    unique_cipher_chars = list(set(ciphertext) - ignore_chars)
    lowercase_alphabets = [chr(i) for i in range(ord('a'), ord('z') + 1)]

    dummy_index = 1
    while len(unique_cipher_chars) < 26:
        unique_cipher_chars.append(f"_dummy{dummy_index}")
        dummy_index += 1

    cipher_mapping = {
        unique_cipher_chars[i]: lowercase_alphabets[i] for i in range(26)}

    filtered_cipher_mapping = {
        k: v for k, v in cipher_mapping.items() if not re.match(r'^_dummy\d+$', k)}
    translation_table = str.maketrans(filtered_cipher_mapping)

    frequency_analysis(False, ciphertext.translate(translation_table))
    print(filtered_cipher_mapping, DF['e'], DDF.get(('t', 'h'), 0.0))
    print(getFitness())


if __name__ == "__main__":
    substitution_decipher("1981y, $pp1n1yuux oq@ 2@3s5u1n $p 1981y, 1v y n$s9o2x 19 v$soq yv1y. 1o 1v oq@ v@6@9oq uy27@vo n$s9o2x 5x y2@y, oq@ v@n$98 0$vo 3$3su$sv n$s9o2x, y98 oq@ 0$vo 3$3su$sv 8@0$n2ynx 19 oq@ #$2u8. 5$s98@8 5x oq@ 1981y9 $n@y9 $9 oq@ v$soq, oq@ y2y51y9 v@y $9 oq@ v$soq#@vo, y98 oq@ 5yx $p 5@97yu $9 oq@ v$soq@yvo, 1o vqy2@v uy98 5$28@2v #1oq 3yw1voy9 o$ oq@ #@vo; nq19y, 9@3yu, y98 5qsoy9 o$ oq@ 9$2oq; y98 5y97uy8@vq y98 0xy90y2 o$ oq@ @yvo. 19 oq@ 1981y9 $n@y9, 1981y 1v 19 oq@ 61n191ox $p v21 uy9wy y98 oq@ 0yu816@v; 1ov y98y0y9 y98 91n$5y2 1vuy98v vqy2@ y 0y21o10@ 5$28@2 #1oq oqy1uy98, 0xy90y2 y98 198$9@v1y. 7$$8, 9$# os29 p$2 oq@ v@n$98 3y2o $p oq@ 4s@vo1$9, 7$$8 usnw!")
