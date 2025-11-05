"""
Text Analyzer Program
This program demonstrates string manipulation functions.
"""

def count_characters(text):
    """Count the total number of characters in the text."""
    return len(text)

def count_words(text):
    """Count the number of words in the text."""
    if not text.strip():
        return 0
    return len(text.split())

def count_sentences(text):
    """Count the number of sentences in the text."""
    sentence_endings = '.!?'
    count = 0
    for char in text:
        if char in sentence_endings:
            count += 1
    return count

def count_vowels(text):
    """Count the number of vowels in the text."""
    vowels = 'aeiouAEIOU'
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count

def count_consonants(text):
    """Count the number of consonants in the text."""
    consonants = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
    count = 0
    for char in text:
        if char in consonants:
            count += 1
    return count

def reverse_text(text):
    """Reverse the text."""
    return text[::-1]

def to_uppercase(text):
    """Convert text to uppercase."""
    return text.upper()

def to_lowercase(text):
    """Convert text to lowercase."""
    return text.lower()

def capitalize_words(text):
    """Capitalize the first letter of each word."""
    return text.title()

def find_longest_word(text):
    """Find the longest word in the text."""
    if not text.strip():
        return ""
    
    words = text.split()
    longest = ""
    for word in words:
        # Remove punctuation from word for length comparison
        clean_word = ''.join(char for char in word if char.isalnum())
        if len(clean_word) > len(longest):
            longest = clean_word
    return longest

def main():
    """Main function to analyze text."""
    print("Text Analyzer")
    print("=" * 15)
    
    # Get text from user
    text = input("Enter some text to analyze: ")
    
    if not text.strip():
        print("No text entered.")
        return
    
    # Analyze the text
    print("\nText Analysis:")
    print("-" * 20)
    print(f"Original text: {text}")
    print(f"Character count: {count_characters(text)}")
    print(f"Word count: {count_words(text)}")
    print(f"Sentence count: {count_sentences(text)}")
    print(f"Vowel count: {count_vowels(text)}")
    print(f"Consonant count: {count_consonants(text)}")
    print(f"Longest word: {find_longest_word(text)}")
    
    # Text transformations
    print("\nText Transformations:")
    print("-" * 20)
    print(f"Reversed: {reverse_text(text)}")
    print(f"Uppercase: {to_uppercase(text)}")
    print(f"Lowercase: {to_lowercase(text)}")
    print(f"Capitalized: {capitalize_words(text)}")
    
    # Interactive section
    print("\nInteractive Text Operations:")
    while True:
        print("\nChoose an operation:")
        print("1. Count specific character")
        print("2. Replace word")
        print("3. Count specific word")
        print("4. Exit")
        
        choice = input("Enter choice (1-4): ")
        
        if choice == '4':
            break
            
        if choice == '1':
            char = input("Enter character to count: ")
            count = text.count(char)
            print(f"The character '{char}' appears {count} times.")
        elif choice == '2':
            old_word = input("Enter word to replace: ")
            new_word = input("Enter replacement word: ")
            new_text = text.replace(old_word, new_word)
            print(f"Modified text: {new_text}")
        elif choice == '3':
            word = input("Enter word to count: ")
            words = text.lower().split()
            clean_words = [w.strip('.,!?;:"') for w in words]
            count = clean_words.count(word.lower())
            print(f"The word '{word}' appears {count} times.")
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()