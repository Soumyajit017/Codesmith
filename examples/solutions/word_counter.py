import sys

def count_words_in_sentence():
    """
    Reads a sentence from stdin and prints the number of words in it.
    Words are separated by spaces.
    """
    line = sys.stdin.readline()
    # Strip leading/trailing whitespace and the newline character
    cleaned_line = line.strip()

    if not cleaned_line:
        # If the line is empty or only contains whitespace, there are no words.
        print(0)
        return

    # Split the string by spaces. `str.split()` without arguments
    # handles multiple spaces between words and leading/trailing spaces
    # correctly, producing a list of actual words.
    words = cleaned_line.split()
    print(len(words))

if __name__ == '__main__':
    count_words_in_sentence()
