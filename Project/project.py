import sys
import random


WORD_COMBINATIONS = (
    ("adjective", "noun"),
    ("adjective", "noun", "verb"),
    ("adjective", "noun", "verb", "noun"),
    ("adjective", "noun", "adverb", "verb"),
    ("adjective", "noun", "adverb", "verb", "noun"),
    ("noun", "verb"),
    ("noun", "verb", "noun"),
    ("noun", "adverb", "verb"),
    ("noun", "adverb", "noun"),
    ("adverb", "verb")
)


VERB_ENDINGS = ('ing', 's')


def main():
    """ Main function."""

    print("hello")

    if len(sys.argv) != 2:
        sys.exit("Usage: python project.py ACRONYM")
  
    acronym = sys.argv[1].lower()
    possible_word_combinations = [combination for combination in WORD_COMBINATIONS if len(combination) == len(acronym)]

    if not possible_word_combinations:
        sys.exit("Please try an acronym of a different length.")

    # print(possible_word_combinations)

    selected_combination = random.choice(possible_word_combinations)
    print(selected_combination)

    starting_letter_and_types = list(zip(acronym, selected_combination))
    # print(starting_letter_and_types)

    selected_words = []
    for starting_letter, word_type in starting_letter_and_types:
        with open(f"word-lists/english-{word_type}s.txt", 'r', encoding='utf-8') as f:
            reader = f.readlines()
            filtered_lines = filter_lines(reader, starting_letter)
            num_lines = len(filtered_lines)
            random_number = random.randint(0, num_lines-1)
            random_word = filtered_lines[random_number].strip().capitalize()
            if word_type == "verb":
                random_word += random.choice(VERB_ENDINGS)
                if random_word[-4:] == 'eing':
                    random_word = random_word.replace('eing', 'ing')

            selected_words.append(random_word)

    acronym_meaning = " ".join(selected_words)

    print(acronym_meaning)


def filter_lines(reader, letter) -> list:
    """ Return a list of all the lines in the 'reader' that begin with 'letter' """

    filtered_reader = filter(lambda line: line[0].lower() == letter, reader)
    return [line.strip() for line in filtered_reader]


if __name__ == "__main__":
    main()