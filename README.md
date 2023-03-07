# Acronym Interpreter - CS50P Final Project

**Video Demo:** https://youtu.be/SzMX_717xH8

---

Acronym Interpreter, ironically known as AI, is a Python script that will attempt to "interpret" a given acronym, effectively reverse-translating it.
<br>Pop in a 2-5 letter string of characters, and the script will provide a randomly-generated phrase that corresponds to the letters in the acronym you provided.

---

**File Breakdown**

- **project.py** - the main script, containing the primary functions and including the `main` function.

- **test_project.py** - the test file, containing four test functions to be executed using `pytest`.

- **helper_test_funcs.py** - a 'helper' file, which contains additional functions for use within `test_project.py`.

- **word-lists/** - a directory containing four text files, each one being a word list of a different type. Namely, `english-adjectives.txt`, `english-adverbs.txt`, `english-nouns.txt` and `english-verbs.txt`.
  <br>Credit for these lists: https://github.com/janester/mad_libs and https://github.com/hugsy/stuff/tree/main/random-word

- **requirements.txt** - a text file containing the dependencies required for this script.

---

**Script Usage**

- First, begin by installing the required dependencies, using `requirements.txt`.
  <br>One way to do this is to use `pip install -r requirements.txt` in a fresh virtual environment.

- Open the terminal in the root directory (containing `project.py` etc), and execute the command as below:

  - `python.exe project.py <acronym>`, where `<acronym>` is a 2-5 letter string of characters.

- The script will then run, and will provide a randomly-generated interpretation of the acronym, using the words from the `word-lists/` (assuming it finds a matching phrase).

---

**How the Script Works**

`project.py` is designed to generate grammatically-correct phrases, using the words found in the `word-lists/`.

The logic is, simply-put, as follows:

1. **Parsing command-line arguments**<br>
   The script first checks the command-line arguments provided. If the total number of arguments provided is anything other than 2 (ie if no additional arguments are provided, or more than 1 additional argument is provided), the script will exit, and will explain the correct usage.

2. **Determining a sentence structure**<br>
   Once an acronym is passed into the script, its length is determined, and this length is compared with the lengths of the tuples found in the global tuple `SENTENCE_STRUCTURES`. This global tuple contains various sentence structure patterns, for example `("noun", "adverb", "verb")`, and ultimately one will be chosen to determine the sentence structure of the generated phrase. If the length of the provided acronym does NOT match the lengths of any of these sentence structure tuples, the program will exit. However, if the length _does_ match the length of one or more of these sentence structures, a valid sentence structure is (randomly) selected.

3. **Selecting random words**<br>
   For each letter in the acronym, a word is randomly selected from the `word-lists/` text files. Each of the selected words must start with the correct letter (given in the acronym), and must be of the word type specified in the selected sentence structure pattern. For example, if the first letter of the acronym is "H", and the first letter in the sentence structure is "noun", a random noun starting with "H" will be selected. As each of these words is selected, they will be appended to a list called `unprocessed_words`.

4. **Brushing up on grammar**<br>
   `unprocessed_words` may very well already make sense, however it still goes through a "processing" phase, and outputting `processed_words`. This phase assigns each noun with a "grammatical number" (ie singular or plural), using the **inflect** library, then properly conjugates any proceeding verbs, using the **mlconjug3** library. This will ideally correct any grammatical errors that could have been generated randomly from the previous step. For example, if `unprocessed_words` is `['man', 'eat', 'burger']`, this "processing" step would change the list to `['man', 'eats', 'burger']`, `['men', 'eat', 'burgers']`, or similar. In effect, it ensures that the phrase makes sentence.

5. **Final check**<br>
   In the majority of cases, `processed_words` will make perfect sense by this point, however, since `mlconjug3` is not 100% accurate in conjugating verbs, one final check is carried out, using the `language_tool_python` library. This is used simply to check for any spelling or grammar errors in the resulting sentence. If no errors are found, the sentence is returned to the user and displayed. However, in the (rare) case that the sentence does not make sense, steps 2-5 are repeated, and another random sentence is generated.
