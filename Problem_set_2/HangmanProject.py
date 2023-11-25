# Problem Set 2, hangman.py
# Name:  Nikoloz Aneli
# Collaborators: None
# Time spent: 4 hours

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    return all(letter in letters_guessed for letter in secret_word)


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    result = ["_ "] * len(secret_word)

    for i in range(len(secret_word)):
        for j in range(len(letters_guessed)):
            if secret_word[i] == letters_guessed[j]:
                result[i] = letters_guessed[j]

    return "".join(result)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    lower = 'abcdefghijklmnopqrstuvwxyz'
    available = ''
    for char in lower:
        if char not in letters_guessed:
            available = available + char
            # putting the unguessed letters together

    return available


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guessesLeft = 6
    warning = 3

    print("Welcome to the game Hangman! ")
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
    print("You have " + str(warning) + " warnings left")
    print("-------------")

    letters_guessed = []
    total_score = 0
    unique_char = len(set(secret_word))

    # functionality of game
    while True:

        print("You have " + str(guessesLeft) + " guesses left.")
        print("Available letters: " + get_available_letters(letters_guessed))
        guess = input("Please guess a letter: ").lower()

        # constrains Warnings
        if guess in letters_guessed:
            warning -= 1
            print("Oops! You've already guessed that letter. You have " + str(
                warning) + " warnings left: " + get_guessed_word(secret_word, letters_guessed))
            if warning <= 0:
                warning = 3
                guessesLeft -= 1
            continue
        elif not guess.lower().isalpha():
            warning -= 1
            print("Oops! That is not a valid letter. You have " + str(warning) + " warnings left: " + get_guessed_word(
                secret_word, letters_guessed))
            if warning <= 0:
                warning = 3
                guessesLeft -= 1
            continue
        elif len(guess) > 1:
            warning -= 1
            print("Oops! You should input 1 character only. You have " + str(
                warning) + " warnings left: " + get_guessed_word(secret_word, letters_guessed))
            if warning <= 0:
                warning = 3
                guessesLeft -= 1
            continue

        # guessing a letter or geting penalty
        if guess in secret_word:
            letters_guessed += guess
            print("Good guess: " + get_guessed_word(secret_word, letters_guessed))
        elif (guess in ['a', 'e', 'i', 'o']) and (guess not in secret_word):
            print("Oops! That letter is not in my word wowel: " + get_guessed_word(secret_word, letters_guessed))
            guessesLeft -= 2
        else:
            print("Oops! That letter is not in my word: " + get_guessed_word(secret_word, letters_guessed))
            guessesLeft -= 1

        print("-------------")

        # Ending
        if is_word_guessed(secret_word, letters_guessed):
            total_score = guessesLeft * unique_char
            print("Congratulations, you won! ")
            print("Your total score for this game is: " + str(total_score))
            break
        elif guessesLeft <= 0:
            print("Sorry, you ran out of guesses. The word was: " + secret_word)
            break
        else:
            continue


# -----------------------------------


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''

    my_word = my_word.replace(" ", "")
    if len(my_word) != len(other_word):
        return False

    guessed_letters = []

    for i in range(len(my_word)):
        if my_word[i] != "_" and other_word.count(my_word[i]) != my_word.count(my_word[i]):
            guessed_letters.append(my_word[i])
            return False

    for letter in guessed_letters:
        if letter not in other_word:
            return False

    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''

    my_word = my_word.replace(" ", "")

    matches_found = False

    for word in wordlist:
        # Check if the word has the same length as my_word
        if len(word) == len(my_word):
            match = True

            # Check if guessed letters match corresponding letters
            for i in range(len(my_word)):
                if my_word[i] != '_' and my_word[i] != word[i]:
                    match = False
                    break
                elif my_word[i] == '_' and word[i] in my_word:
                    match = False
                    break

            # If it's a match, print the word
            if match:
                print(word, end=" ")
                matches_found = True

    if not matches_found:
        print("No matches found")


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guessesLeft = 6
    warning = 3

    print("Welcome to the game Hangman!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print(f"You have {warning} warnings left.")
    print("-------------")

    letters_guessed = []
    unique_char = len(set(secret_word))

    # Functionality of the game
    while True:
        print(f"\nYou have {guessesLeft} guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        guess = input("Please guess a letter: ").lower()

        if guess == "*":
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue

        # Constraints and warnings
        elif guess in letters_guessed:
            warning -= 1
            print(f"Oops! You've already guessed that letter. You have {warning} warnings left:",
                  get_guessed_word(secret_word, letters_guessed))
            if warning <= 0:
                warning = 3
                guessesLeft -= 1
                continue
        elif not guess.isalpha():
            warning -= 1
            print(f"Oops! That is not a valid letter. You have {warning} warnings left:",
                  get_guessed_word(secret_word, letters_guessed))
            if warning <= 0:
                warning = 3
                guessesLeft -= 1
                continue
        elif len(guess) > 1:
            warning -= 1
            print(f"Oops! You should input 1 character only. You have {warning} warnings left:",
                  get_guessed_word(secret_word, letters_guessed))
            if warning <= 0:
                warning = 3
                guessesLeft -= 1
                continue

        # Guessing a letter or getting a penalty
        if guess in secret_word and len(guess) == 1:
            letters_guessed.append(guess)
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))
        elif guess in ['a', 'e', 'i', 'o'] and guess not in secret_word:
            print("Oops! That letter is not in my word vowel:", get_guessed_word(secret_word, letters_guessed))
            guessesLeft -= 2
        else:
            print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
            guessesLeft -= 1

        print("-------------")

        # Ending
        if is_word_guessed(secret_word, letters_guessed):
            total_score = guessesLeft * unique_char
            print("Congratulations, you won!")
            print("Your total score for this game is:", total_score)
            break
        elif guessesLeft <= 0:
            print("Sorry, you ran out of guesses. The word was:", secret_word)
            break


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
