import sys
import random
import inflect
from mlconjug3 import Conjugator


SENTENCE_STRUCTURES = (
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

ENGINE = inflect.engine()
CONJUGATOR = Conjugator(language="en")


def main():
    """ Main function."""

    if len(sys.argv) != 2:
        sys.exit("Usage: python project.py ACRONYM")
  
    acronym = sys.argv[1].lower()
    if not (sentence_structure := select_sentence_structure(acronym)):
        sys.exit("Please try an acronym of a different length.")
  
    unprocessed_words = select_unprocessed_words(acronym, sentence_structure)
    print(unprocessed_words)


    # selected_words = []
    # for starting_letter, word_type in starting_letter_and_types:
    #     with open(f"word-lists/english-{word_type}s.txt", 'r', encoding='utf-8') as f:
    #         reader = f.readlines()
    #         filtered_words = filter_lines(reader, starting_letter)
    #         num_lines = len(filtered_words)
    #         random_number = random.randint(0, num_lines-1)
    #         random_word = filtered_words[random_number].strip().capitalize()
    #         if word_type == "verb":
    #             random_word += random.choice(VERB_ENDINGS)
    #             if random_word[-4:] == 'eing':
    #                 random_word = random_word.replace('eing', 'ing')

    #         selected_words.append(random_word)

    # acronym_meaning = " ".join(selected_words)

    # print(acronym_meaning)


def select_sentence_structure(acronym: str) -> tuple | None:
    """ Determine a random sentence structure from the given acronym """
    
    possible_sentence_structures = [combination for combination in SENTENCE_STRUCTURES if len(combination) == len(acronym)]
    # if no possible sentence structures have been found, the acronym is of the wrong length
    if not possible_sentence_structures:
        return None
    
    sentence_structure = random.choice(possible_sentence_structures)
    return sentence_structure


def select_unprocessed_words(acronym, sentence_structure) -> list[str]:
    """ Select a word for each of the letters in the given acronym,
    using the sentence structure provided."""
    
    structure_and_letters = list(zip(acronym, sentence_structure))

    selected_words = []
    for starting_letter, word_type in structure_and_letters:
        with open(f"word-lists/english-{word_type}s.txt", 'r', encoding='utf-8') as f:
            reader = f.readlines()
            filtered_words = filter_lines(reader, starting_letter)
            print(filtered_words)
            random_word = random.choice(filtered_words)
            print(random_word)
            selected_words.append(random_word)

            # num_lines = len(filtered_words)
            # random_number = random.randint(0, num_lines-1)
            # random_word = filtered_words[random_number].strip().capitalize()

            ### REPLACE THIS
            # if word_type == "verb":
            #     random_word += random.choice(VERB_ENDINGS)
            #     if random_word[-4:] == 'eing':
            #         random_word = random_word.replace('eing', 'ing')

    return selected_words


def filter_lines(reader, letter) -> list:
    """ Return a list of all the lines in the 'reader' that begin with 'letter' """

    filtered_reader = filter(lambda line: line[0].lower() == letter, reader)
    return [line.strip() for line in filtered_reader]


# def select_random_word(words) -> str:
#         """ Select a random word from the list of words passed in"""
#         # if no words are passed in
#         if not words:
#             return ""
#         return random.choice(words)


def singular_or_plural(word) -> str:
    """ Determine whether a word is singular or plural """
    return "singular" if not ENGINE.singular_noun(word) else "plural"


if __name__ == "__main__":

    # checking if noun is plural or singular
    # words = ["man", "people", "cats", "cat", "dogs"]
    # for word in words:
    #     print(singular_or_plural(word))
        # print(f"is {word} singular? {engine.singular_noun(word) == word} ")


    # checking verb conjugations
    # conjugator = Conjugator(language="en")
    # results = conjugator.conjugate("mix")
    # print(results.iterate())

    # print(results["indicative"]["he/she/it"]["I"])
    # print(results["indicative"]["we"]["I"])


    main()