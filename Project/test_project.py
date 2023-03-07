""" pytest module for project.py """

# functions to test
from project import select_sentence_structure
from project import filter_lines
from project import select_unprocessed_words
from project import sentence_makes_sense

# functions to help with testing
from helper_test_funcs import check_valid_acronym


def test_select_sentence_structure():
    """ Test to see if the correct sentence structure is selected from a given acronym. 
    Acronyms must be lower case, as it is converted to lower case instantly in project.py, in the main function."""
    assert select_sentence_structure("hello") == ("adjective", "noun", "adverb", "verb", "noun")
    assert select_sentence_structure("mike") == ("adjective", "noun", "verb", "noun")
    assert select_sentence_structure("hey") == ("noun", "verb", "noun") \
    or select_sentence_structure("hey") == ("noun", "adverb", "verb")


def test_filter_lines():
    """ Test to see if a reader object is successfully filtered to include only words starting with a given letter. """
    file_loc = "word-lists/english-nouns.txt"
    starting_letter = "t"
    with open(file_loc, "r", encoding="utf-8") as f:
        reader = f.readlines()
        filtered_words = filter_lines(reader, starting_letter)
        words_starting_with_starting_letter = [word for word in filtered_words if word[0] == starting_letter]
    assert filtered_words == words_starting_with_starting_letter


def test_select_unprocessed_words():
    """ Test to see if the unprocessed words selected from a given acronym, are congruent with the acronym itself. """
    sentence_structure = ("adjective", "noun", "adverb", "verb", "noun")
    acronym = "hello"
    unprocessed_words =  select_unprocessed_words(acronym, sentence_structure)
    assert check_valid_acronym(unprocessed_words, acronym) is True


def test_sentence_makes_sense():
    """ Testing the function that checks if a phrase makes sense."""
    assert sentence_makes_sense("I like apples") is True
    assert sentence_makes_sense("i like apples") is False
    assert sentence_makes_sense("I like appples") is False
    assert sentence_makes_sense("Hello, I like turtles") is True
    assert sentence_makes_sense("Hello I like turtles") is False