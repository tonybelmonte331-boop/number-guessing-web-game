import random

DIFFICULTIES = {
    "1": {"name": "Easy", "digits": 3, "guesses": 6},
    "2": {"name": "Medium", "digits": 5, "guesses": 6},
    "3": {"name": "Hard", "digits": 6, "guesses": 7}
}

def choose_difficulty():
    print("Choose a difficulty:")
    for key, value in DIFFICULTIES.items():
        print(f" {key}. {value['name']} ({value['digits']} digits, {value['guesses']} guesses)")

    choice = input("Enter 1, 2, or 3: ")
    while choice not in DIFFICULTIES:
        choice = input("Invalid choice. Enter 1, 2, or 3: ")

    return DIFFICULTIES[choice]

def play_game(settings):
    digits = settings["digits"]
    max_guesses = settings["guesses"]

    secret = [random.randint(0, 9) for _ in range(digits)]

    print(f"\nI have generated a {digits}-digit secret number.")
    print(f"You have {max_guesses} guesses.\n")

    guesses_used = 0

    while guesses_used < max_guesses:
        guess = input(f"Guess {guesses_used + 1}: Enter {digits} digits: ")

        if len(guess) != digits or not guess.isdigit():
            print("❌ Invalid input.\n")
            continue

        guesses_used += 1
        guess_digits = [int(d) for d in guess]

        feedback = [""] * digits
        secret_copy = secret.copy()
        guess_copy = guess_digits.copy()

        # Pass 1: correct digit & position
        for i in range(digits):
            if guess_copy[i] == secret_copy[i]:
                feedback[i] = "✅ correct position"
                secret_copy[i] = None
                guess_copy[i] = None

        # Pass 2: correct digit, wrong position
        for i in range(digits):
            if guess_copy[i] is not None and guess_copy[i] in secret_copy:
                feedback[i] = "🔄 wrong position"
                secret_copy[secret_copy.index(guess_copy[i])] = None
            elif feedback[i] == "":
                feedback[i] = "❌ not in number"

        # Show feedback
        print("Feedback:")
        for i in range(digits):
            print(f" Digit {i + 1} ({guess_digits[i]}): {feedback[i]}")
        print()

        if all(f == "✅ correct position" for f in feedback):
            print(f"🎉 You won in {guesses_used} guesses!")
            return

    print("💀 Game over!")
    print("The secret number was:", "".join(map(str, secret)))

def main():
    while True:
        settings = choose_difficulty()
        play_game(settings)

        again = input("\nPlay again? (y/n): ").lower()
        if again != "y":
            print("Thanks for playing!")
            break

main()