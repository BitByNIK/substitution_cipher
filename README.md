# Substitution Cipher Decoder

This project is a Python-based implementation of a substitution cipher decoder. It uses **hill climbing**, a search optimization algorithm, to iteratively improve decryption keys. By analyzing patterns in the ciphertext and comparing them with English language characteristics, the script deciphers encrypted text.

---

## How It Works

A substitution cipher replaces each letter in plaintext with a specific character (e.g., numbers, symbols, or other letters). To decrypt such a cipher, the script finds the mapping between ciphertext characters and plaintext letters.

### Steps in the Decryption Process

1. **Initial Setup:**

   - The script starts with a **random key**, mapping ciphertext characters to plaintext letters.
   - A key represents how each ciphertext character translates into a plaintext letter.

2. **Fitness Calculation:**

   - The script evaluates how good the current key is by calculating a **fitness score**.
   - This score measures how similar the decrypted text is to English using the frequency of groups of four letters (called **quadgrams**).
   - Formula used for fitness:
     $$\text{Fitness} = \sum_{\text{quadgram}} \log(\text{QF}[\text{quadgram}])$$
     - **QF** represents the frequency of quadgrams in standard English text.
     - Taking the logarithm ensures to avoid underflow because frequencies can be small.

3. **Heuristic-Based Key Selection:**

   - A **heuristic function** is used to prioritize which parts of the key to adjust.
   - The heuristic identifies ciphertext characters whose frequencies differ the most from expected English frequencies.
   - Formula for the heuristic:
     $$H(b) = \max(1, |\text{FC}(b) - \text{FE}(\text{E}^{-1}(b))|)$$
     Where:

     - $$H(b)$$: Heuristic score for a ciphertext letter $$b$$.
     - $$\text{FC}(b)$$: Rank of $$b$$ in ciphertext frequencies.
     - $$\text{FE}(a)$$: Rank of the corresponding plaintext letter $$a$$ in English frequencies.

   - A ciphertext letter $$b$$ with a large heuristic value is **more likely to be swapped** because it is far from its expected frequency rank. The goal is to quickly minimize these differences.
   - Once a character $$b$$ is selected, it is swapped with another randomly chosen character in the key.

4. **Key Evaluation:**

   - The script decrypts the text using the modified key.
   - If the fitness score improves, the new key is kept. Otherwise, it is discarded.

5. **Stopping Condition:**
   - If the fitness score does not improve after \( T \) iterations, the process stops.
   - The entire procedure is repeated multiple times, and the best key across all attempts is chosen.

---

## Why Use a Heuristic?

The heuristic focuses on ciphertext letters whose observed frequencies differ the most from expected English frequencies. This:

- **Speeds Up Convergence:** Quickly minimizes large frequency mismatches.
- **Improves Accuracy:** Guides the algorithm to better keys, especially for longer ciphertexts where frequency distributions are more reliable.

---

## Features

- **Hill Climbing Optimization:** Iteratively improves the decryption key using fitness scoring.
- **Quadgram-Based Scoring:** Evaluates how "English-like" the decrypted text is.
- **Heuristic Guidance:** Targets the most impactful key adjustments to improve efficiency.

---

## Requirements

- **Python 3.6 or Higher**
- A file containing a large sample of English text is required to calculate the letter and quadgram frequencies. Here, we have used big.txt, which should be a plain text file with diverse English content (e.g., books, articles). The quality of decryption improves with a larger and more representative reference text.

### Dependencies:

- Built-in Python libraries: `collections`, `math`, `random`.

---
