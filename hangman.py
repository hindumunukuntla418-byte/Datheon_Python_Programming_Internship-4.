
import random

# ASCII art for each stage of Hangman
HANGMAN_ART = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========
    """
]

# Words used in the game
WORDS = [
    "python",
    "computer",
    "programming",
    "keyboard",
    "developer",
    "science",
    "machine",
    "learning",
    "internet",
    "software"
]


def display_word(secret_word, guessed_letters):
    """Display guessed letters and hide the remaining letters."""
    return " ".join(
        letter.upper() if letter in guessed_letters else "_"
        for letter in secret_word
    )


def play_game():
    secret_word = random.choice(WORDS)
    guessed_letters = set()
    wrong_guesses = set()
    max_attempts = 6

    print("\n================================")
    print("       HANGMAN WORD GAME")
    print("================================")
    print("Guess the hidden word!")
    print("You have 6 incorrect guesses allowed.\n")

    while len(wrong_guesses) < max_attempts:

        print(HANGMAN_ART[len(wrong_guesses)])

        print("Word:", display_word(secret_word, guessed_letters))
        print("Guessed letters:",
              " ".join(sorted(guessed_letters | wrong_guesses)))
        print("Attempts left:", max_attempts - len(wrong_guesses))

        guess = input("\nEnter a letter: ").lower().strip()

        # Validate input
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter only one alphabet letter!")
            continue

        # Prevent duplicate guesses
        if guess in guessed_letters or guess in wrong_guesses:
            print("You already guessed that letter. Try another!")
            continue

        if guess in secret_word:
            guessed_letters.add(guess)
            print("Correct guess!")

            # Check victory
            if all(letter in guessed_letters for letter in secret_word):
                print("\n" + display_word(secret_word, guessed_letters))
                print("\nCONGRATULATIONS! YOU WON!")
                print("You guessed the correct word!")
                return

        else:
            wrong_guesses.add(guess)
            print("Wrong guess!")

    # Defeat screen
    print(HANGMAN_ART[max_attempts])
    print("\nGAME OVER! YOU LOST!")
    print("The correct word was:", secret_word.upper())


def main():
    while True:
        play_game()

        again = input("\nWould you like to play again? (yes/no): ").lower()

        if again not in ("yes", "y"):
            print("\nThank you for playing Hangman!")
            break


if __name__ == "__main__":
    main()
