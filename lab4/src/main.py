import threading
from collections import defaultdict
import string
import os

def clean_word(word):
    """Convert to lowercase and remove punctuation."""
    word = word.lower()
    return word.translate(str.maketrans('', '', string.punctuation))

def count_words_in_file(filename, word_count_map, map_lock):
    """Count words in a file and update the global word count map."""
    try:
        with open(filename, 'r') as file:
            local_map = defaultdict(int)

            # Read words from the file
            for line in file:
                words = line.split()
                for word in words:
                    cleaned_word = clean_word(word)
                    if cleaned_word:
                        local_map[cleaned_word] += 1

            # Merge local map into the global map in a thread-safe manner
            with map_lock:
                for word, count in local_map.items():
                    word_count_map[word] += count
    except FileNotFoundError:
        print(f"Could not open file: {filename}")

def save_word_count_to_file(output_folder, word_count_map):
    """Save the word count to a file in the specified output folder."""
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "word_count_result.txt")
    with open(output_file, 'w') as file:
        for word, count in sorted(word_count_map.items()):
            file.write(f"{word}: {count}\n")
    print(f"Word count results saved to {output_file}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(f"Usage: {os.path.basename(sys.argv[0])} <file1> <file2> ...")
        sys.exit(1)

    # Global word count map and lock for thread safety
    word_count_map = defaultdict(int)
    map_lock = threading.Lock()

    # Create threads for each file
    threads = []
    for filename in sys.argv[1:]:
        thread = threading.Thread(target=count_words_in_file, args=(filename, word_count_map, map_lock))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Save the results to the output folder
    output_folder = "output"
    save_word_count_to_file(output_folder, word_count_map)
