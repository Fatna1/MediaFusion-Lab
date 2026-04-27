# Word Frequency Counter 

import os
import re
from collections import Counter
import string

def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    if not os.path.exists('output'):
        os.makedirs('output')

def word_frequency_counter(text):
    """
    Algorithm 7: Count frequency of each word in text
    Principle: Tokenize text into words, count occurrences, sort by frequency
    Formula: frequency(word) = count(word) / total_words (relative frequency)
    """
    # Clean the text: convert to lowercase and remove punctuation
    # Formula: normalized_word = lowercase(remove_punctuation(word))
    cleaned_text = text.lower()
    # Remove punctuation
    for punct in string.punctuation:
        cleaned_text = cleaned_text.replace(punct, ' ')
    
    # Split into words (tokenization)
    words = cleaned_text.split()
    
    # Count word frequencies
    # Formula: frequency(word) = count(word)
    word_counts = Counter(words)
    
    # Get total number of words for relative frequency
    total_words = len(words)
    
    # Sort by frequency (highest first)
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Prepare results
    results = []
    results.append(f"Total words: {total_words}")
    results.append(f"Unique words: {len(word_counts)}")
    results.append("\nTop 20 most frequent words:")
    results.append("-" * 40)
    results.append(f"{'Word':<20} {'Count':<10} {'Frequency (%)':<15}")
    results.append("-" * 40)
    
    for word, count in sorted_words[:20]:
        relative_freq = (count / total_words) * 100
        results.append(f"{word:<20} {count:<10} {relative_freq:<15.2f}")
    
    # Save to file
    ensure_output_dir()
    output_path = 'output/word_frequency.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
    
    result_text = '\n'.join(results)
    explanation = (f"Word frequency analysis complete.\n"
                   f"Mathematical principle: Count occurrences of each unique word.\n"
                   f"Formula: frequency(word) = number of times word appears in text\n"
                   f"Relative frequency = (count / total_words) × 100%\n"
                   f"Saved to {output_path}")
    
    return result_text, explanation

#Caesar Cipher Encryption
def caesar_cipher_encrypt(text, shift=3):
    """
    Algorithm 8: Caesar Cipher encryption
    Principle: Shift each letter by a fixed number of positions in the alphabet
    Formula: C = (P + K) mod 26, where P = plaintext position, K = shift key
    """
    result = []
    
    for char in text:
        if char.isupper():
            # Formula for uppercase: (position + shift) mod 26
            # ord() gets ASCII value, subtract ord('A') to get 0-25 position
            original_pos = ord(char) - ord('A')
            encrypted_pos = (original_pos + shift) % 26
            encrypted_char = chr(encrypted_pos + ord('A'))
            result.append(encrypted_char)
            
        elif char.islower():
            # Formula for lowercase: (position + shift) mod 26
            original_pos = ord(char) - ord('a')
            encrypted_pos = (original_pos + shift) % 26
            encrypted_char = chr(encrypted_pos + ord('a'))
            result.append(encrypted_char)
            
        else:
            # Non-alphabet characters remain unchanged
            result.append(char)
    
    encrypted_text = ''.join(result)
    
    # Save to file
    ensure_output_dir()
    output_path = 'output/encrypted_text.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Original text:\n{text}\n\n")
        f.write(f"Encrypted text (Caesar cipher, shift={shift}):\n{encrypted_text}")
    
    explanation = (f"Caesar cipher encryption complete.\n"
                   f"Mathematical principle: Shift each letter by {shift} positions.\n"
                   f"Formula: C = (P + {shift}) mod 26\n"
                   f"Where P = plaintext position (0-25), C = ciphertext position\n"
                   f"Saved to {output_path}")
    
    return encrypted_text, explanation

def caesar_cipher_decrypt(text, shift=3):
    """
    Decrypt text encrypted with Caesar cipher
    Formula: P = (C - K) mod 26
    """
    return caesar_cipher_encrypt(text, -shift)

# Test functions
if __name__ == "__main__":
    print("Text Algorithms Module")
    print("-" * 30)
    print("Functions available:")
    print("1. word_frequency_counter(text)")
    print("2. caesar_cipher_encrypt(text, shift=3)")
    print("3. caesar_cipher_decrypt(text, shift=3)")