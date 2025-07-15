from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import requests

app = Flask(__name__)

# Setup ChatterBot
bot = ChatBot("MarvelBot", read_only=True)

# English + Marvel custom training
corpus_trainer = ChatterBotCorpusTrainer(bot)
corpus_trainer.train("chatterbot.corpus.english")

custom_trainer = ListTrainer(bot)
custom_marvel_data = [
    "Who plays Iron Man?",
    "Robert Downey Jr. plays Iron Man in the MCU.",
    "What is the first Marvel movie?",
    "Iron Man (2008) was the first film in the MCU.",
    "Is Deadpool part of the MCU?",
    "Deadpool is expected to join the MCU, especially with Deadpool 3."
]
custom_trainer.train(custom_marvel_data)

# OMDb integration
OMDB_API_KEY = "abaebb89"

def get_movie_info(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    res = requests.get(url).json()
    if res.get("Response") == "True":
        title = res.get("Title")
        year = res.get("Year")
        director = res.get("Director")
        actors = res.get("Actors")
        plot = res.get("Plot")
        return f"{title} ({year}) — Directed by {director}. Cast: {actors}. Plot: {plot}"
    else:
        return "Sorry, I couldn't find that movie on OMDb."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data["message"]

    # Use OMDb if it's a movie query
    trigger_phrases = ["tell me about", "plot of", "who directed", "info about"]
    if any(phrase in user_message.lower() for phrase in trigger_phrases):
        movie_name = user_message
        for phrase in trigger_phrases:
            movie_name = movie_name.lower().replace(phrase, "")
        response = get_movie_info(movie_name.strip())
    else:
        response = str(bot.get_response(user_message))

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
