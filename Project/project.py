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
    # ("noun", "verb", "noun"),
    ("noun", "adverb", "verb"),
    ("adverb", "verb"),
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

    ### implement logic to deal with grammar and word endings
    # for word in unprocessed_words:
    #     print(ENGINE.plural(word))


    words_and_structure = list(zip(unprocessed_words, sentence_structure))
    print(words_and_structure)
    # initialise with False as each value
    processed_words = [False for word in unprocessed_words]
    for idx, (word, word_type) in enumerate(words_and_structure):
        print(processed_words)
        # check if a verb proceeds a noun - if so, ensure the grammar between the two works
        if word_type == "noun" and idx < len(words_and_structure) - 1 and words_and_structure[idx+1][1] == "verb":
            # randomly decide if it should be singular or plural
            grammatical_number = random.choice(["singular", "plural"])
            new_noun = change_sing_plural(word, grammatical_number)

            verb = words_and_structure[idx+1][0]
            new_verb = change_verb(verb, grammatical_number)

            print(f"{grammatical_number=}, {word=}, {new_noun=}, {new_verb=}")

            # if the result is False, this means there was a keyerror
            # in this event, just return the unprocessed words
            if not new_verb:
                processed_words = unprocessed_words
                break

            processed_words[idx] = new_noun
            processed_words[idx+1] = new_verb

        # check for noun, adverb, verb
        elif word_type == "noun" and idx < len(words_and_structure) - 2 and words_and_structure[idx+1][1] == "adverb" and words_and_structure[idx+2][1] == "verb":
            # randomly decide if it should be singular or plural
            grammatical_number = random.choice(["singular", "plural"])
            new_noun = change_sing_plural(word, grammatical_number)

            verb = words_and_structure[idx+2][0]
            new_verb = change_verb(verb, grammatical_number)

            print(f"{grammatical_number=}, {word=}, {new_noun=}, {new_verb=}")

            # if the result is False, this means there was a keyerror
            # in this event, just return the unprocessed words
            if not new_verb:
                processed_words = unprocessed_words
                break

            processed_words[idx] = new_noun
            processed_words[idx+2] = new_verb           

        elif word_type == "noun" and idx == len(words_and_structure) - 1:
            grammatical_number = random.choice(["singular", "plural"])
            new_noun = change_sing_plural(word, grammatical_number)   

            print(f"{grammatical_number=}, {word=}, {new_noun=}")    

            processed_words[idx] = new_noun

            # if singular_or_plural(word) == "singular":

            # print("yes")

        # if no changes have been made, and there are no words in the relevant spot in processed_words, add the word
        elif not processed_words[idx]:
            processed_words[idx] = word

        print(idx, word, word_type)

    print(f"{unprocessed_words=}")
    print(f"{processed_words=}")


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


def singular_or_plural(word) -> str:
    """ Determine whether a word is singular or plural """
    return "singular" if not ENGINE.singular_noun(word) else "plural"


def change_sing_plural(word: str, grammatical_number: str) -> str | bool:
    if grammatical_number == "plural":
        return ENGINE.plural_noun(word)

    if (new_word := ENGINE.singular_noun(word)):
        return new_word
    return word


def change_verb(verb: str, grammatical_number: str) -> str | bool:
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


if __name__ == "__main__":

    # checking if noun is plural or singular
    # words = ["man", "people", "cats", "cat", "dogs"]
    # for word in words:
    #     print(singular_or_plural(word))
        # print(f"is {word} singular? {engine.singular_noun(word) == word} ")


    # checking verb conjugations
    # conjugator = Conjugator(language="en")
    # results = conjugator.conjugate("educate")
    # print(results.iterate())
    # print("----------")
    # print(results["indicative"]["indicative present"]["he/she/it"])
    # print(results["indicative"]["indicative present"]["they"])
    # print(results["indiecative"]["indicative present"]["he/she/it"])
    # print(results["indicative"]["we"]["I"])

    # print(change_verb("educate", "plural"))


    main()