""" Helper functions for the test_project.py file """


def check_valid_acronym(list_of_words, acronym) -> bool:
    """ Check if a list of words is congruent with a given acronym. """
    if len(acronym) != len(list_of_words):
        return False

    for idx, letter in enumerate(acronym):
        if list_of_words[idx][0].lower() != letter.lower():
            return False
        
    return True