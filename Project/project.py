import sys
import random
import inflect
from mlconjug3 import Conjugator
import language_tool_python


SENTENCE_STRUCTURES = (
    ("adjective", "noun"),
    # ("adjective", "noun", "verb"),
    ("adjective", "noun", "verb", "noun"),
    # ("adjective", "noun", "adverb", "verb"),
    ("adjective", "noun", "adverb", "verb", "noun"),
    # ("noun", "verb"),
    ("noun", "verb", "noun"),
    ("noun", "adverb", "verb"),
    # ("adverb", "verb"),
)

 
VERB_ENDINGS = ('ing', 's')

ENGINE = inflect.engine()
CONJUGATOR = Conjugator(language="en")


def main() -> str:
    """ Main function."""

    if len(sys.argv) != 2:
        sys.exit("Usage: python project.py ACRONYM")
  
    acronym = sys.argv[1].lower()

    # carry out the entire process of determining a valid sentence, until a generated sentence makes sense
    while True:

        if not (sentence_structure := select_sentence_structure(acronym)):
            sys.exit("Please try an acronym of a different length.")
    
        unprocessed_words = select_unprocessed_words(acronym, sentence_structure)
        # print(unprocessed_words)

        # process the words to make a grammatically-correct sentence
        # specifically, ensure each noun-verb pair is conjugated correctly
        words_and_structure = list(zip(unprocessed_words, sentence_structure))
        # print(words_and_structure)
        # initialise with None as each value
        processed_words = [None for word in unprocessed_words]
        for idx, (word, word_type) in enumerate(words_and_structure):
            print(idx, word, word_type)
            print(f"{processed_words=}")

            if word_type == "noun":
                # randomly switch the noun to either plural or singular
                grammatical_number = random.choice(["singular", "plural"])
                print(f"{grammatical_number=}")
                new_noun = change_noun_sing_plural(word, grammatical_number)
                processed_words[idx] = new_noun

                # if this noun is the final word, break the loop (since there won't be a verb after it)
                if idx == len(words_and_structure) - 1:
                    break

                # if the next word is a verb
                if words_and_structure[idx+1][1] == "verb":
                    verb = words_and_structure[idx+1][0]
                    new_verb = change_verb_conjugation(verb, grammatical_number)
                    processed_words[idx+1] = new_verb
                # if the next words are an adverb and verb, respectively
                elif words_and_structure[idx+1][1] == "adverb" and words_and_structure[idx+2][1] == "verb":
                    verb = words_and_structure[idx+2][0]
                    new_verb = change_verb_conjugation(verb, grammatical_number)
                    processed_words[idx+2] = new_verb


            # if not a noun, and this word hasn't been processed already, just leave it as it is
            elif not processed_words[idx]:
                processed_words[idx] = word


        print(f"{sentence_structure=}")
        print(f"{unprocessed_words=}")

        # complete the sentence if every item in processed_words is a word
        if all(isinstance(x, str) for x in processed_words):
            finished_sentence = " ".join(processed_words).title()
            print(f"{finished_sentence=}")

        # now check if the finished_sentence makes sense

        if sentence_makes_sense(finished_sentence):
            return finished_sentence
        else:
            continue



        # sentence_checker = language_tool_python.LanguageToolPublicAPI('en-US')
        # matches = sentence_checker.check(finished_sentence)
    
        # # if the sentence doesn't make sense, try the whole process again
        # if matches:
        #     continue
        # else: # otherwise, return the sentence and break the loop
        #     return finished_sentence


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
            print(f"{reader=}")
            filtered_words = filter_lines(reader, starting_letter)
            print(f"{filtered_words=}")
            # print(filtered_words)
            random_word = random.choice(filtered_words)
            # print(random_word)
            selected_words.append(random_word)

    return selected_words


def filter_lines(reader, letter) -> list:
    """ Return a list of all the lines in the 'reader' that begin with 'letter' """

    filtered_reader = filter(lambda line: line[0].lower() == letter, reader)
    return [line.strip() for line in filtered_reader]


def change_noun_sing_plural(word: str, grammatical_number: str) -> str | bool:
    if grammatical_number == "plural":
        return ENGINE.plural_noun(word)

    if (new_word := ENGINE.singular_noun(word)):
        return new_word
    return word


def change_verb_conjugation(verb: str, grammatical_number: str) -> str | bool:
    verb_results = CONJUGATOR.conjugate(verb)
    if grammatical_number == "singular":
        grammar_val = "he/she/it"
    elif grammatical_number == "plural":
        grammar_val = "they"
    
    try:
        new_verb = verb_results["indicative"]["indicative present"][grammar_val]
    except KeyError:
        return False
    else:
        return new_verb


def sentence_makes_sense(sentence) -> bool:
    sentence_checker = language_tool_python.LanguageToolPublicAPI('en-US')
    matches = sentence_checker.check(sentence)

    # if matches are found, this means errors were found in the sentence
    if matches:
        return False
    
    return True


if __name__ == "__main__":
    main()