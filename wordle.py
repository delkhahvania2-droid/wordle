from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "wordle_secret_key"  # required for sessions

words = [
    "apple", "grape", "house", "water", "smile",
    "happy", "table", "chair", "bread", "green",
    "black", "white", "brown", "cloud", "storm",
    "light", "plant", "grass", "snake", "zebra",
    "horse", "sheep", "tiger", "mouse", "beach",
    "river", "ocean", "stone", "candy", "juice",
    "lemon", "peach", "melon", "mango", "pizza",
    "dance", "music", "story", "sleep", "dream",
    "laugh", "clown", "robot", "train", "truck",
    "plane", "queen", "magic", "heart", "panda"
]

@app.route("/", methods=["GET", "POST"])
def game():
    # initialize session
    if "correct" not in session:
        session["correct"] = random.choice(words).upper()
        session["attempts"] = 0
        session["history"] = []

    correct = session["correct"]
    history = session["history"]
    message = ""

    if request.method == "POST" and session["attempts"] < 6:
        guess = request.form["guess"].upper()

        if len(guess) != 5:
            message = "Please enter exactly 5 letters."
        else:
            result = []

            for i in range(5):
                if guess[i] == correct[i]:
                    result.append(("green", guess[i]))
                elif guess[i] in correct:
                    result.append(("yellow", guess[i]))
                else:
                    result.append(("gray", guess[i]))

            history.append(result)
            session["history"] = history
            session["attempts"] += 1

            if guess == correct:
                message = "CORRECT!"
            elif session["attempts"] == 6:
                message = f"You lost! The word was {correct}."
            else:
                message = f"Attempt {session['attempts']}/6"

    return render_template(
        "index.html",
        history=history,
        message=message,
        attempts=session["attempts"]
    )

@app.route("/reset")
def reset():
    session.clear()
    return "<script>window.location='/'</script>"

if __name__ == "__main__":
    app.run(debug=True)