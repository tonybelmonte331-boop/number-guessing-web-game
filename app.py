from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Difficulty settings
DIFFICULTIES = {
    "easy": {"digits": 3, "max_guesses": 8},
    "medium": {"digits": 5, "max_guesses": 6},
    "hard": {"digits": 6, "max_guesses": 5}
}

# Global game state
game_state = {}

def start_game(difficulty):
    settings = DIFFICULTIES[difficulty]
    game_state["secret"] = [random.randint(0, 9) for _ in range(settings["digits"])]
    game_state["digits"] = settings["digits"]
    game_state["max_guesses"] = settings["max_guesses"]
    game_state["guesses_used"] = 0
    game_state["history"] = []
    game_state["won"] = False
    game_state["difficulty"] = difficulty

@app.route("/", methods=["GET", "POST"])
def index():
    feedback = None

    # Start a new game
    if request.method == "POST" and "difficulty" in request.form:
        start_game(request.form["difficulty"])

    # Process a guess
    elif request.method == "POST" and "guess" in request.form:
        if not game_state:
            return render_template("index.html", game=None, feedback=["Start a new game first!"])

        guess = request.form["guess"]
        digits = game_state["digits"]

        if len(guess) != digits or not guess.isdigit():
            feedback = ["❌ Invalid input."]
        else:
            game_state["guesses_used"] += 1
            guess_digits = [int(d) for d in guess]

            secret_copy = game_state["secret"].copy()
            guess_copy = guess_digits.copy()
            feedback = [""] * digits

            # Correct digit & correct position
            for i in range(digits):
                if guess_copy[i] == secret_copy[i]:
                    feedback[i] = "✅ correct position"
                    secret_copy[i] = None
                    guess_copy[i] = None

            # Correct digit, wrong position
            for i in range(digits):
                if guess_copy[i] is not None and guess_copy[i] in secret_copy:
                    feedback[i] = "🔄 wrong position"
                    secret_copy[secret_copy.index(guess_copy[i])] = None
                elif feedback[i] == "":
                    feedback[i] = "❌ not in number"

            game_state["history"].append((guess, feedback))

            # Check if the player won
            if all(f == "✅ correct position" for f in feedback):
                game_state["won"] = True

    return render_template("index.html", game=game_state if game_state else None, feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True)