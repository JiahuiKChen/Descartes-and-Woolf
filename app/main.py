from flask import Flask, render_template, request
import pickle
import json
import markovify

app = Flask(__name__)


# Loading all sentences and word sets for authors
text_dicts_dir = "AuthorTextDicts/"
with open(text_dicts_dir + "Woolf-Sentences.pickle", 'rb') as woolf_file:
    woolf_sentences = pickle.load(woolf_file)

with open(text_dicts_dir + "Woolf-WordSets.pickle", 'rb') as woolf_file:
    woolf_wordsets = pickle.load(woolf_file)

with open(text_dicts_dir + "Descartes-Sentences.pickle", 'rb') as d_file:
    descartes_sentences = pickle.load(d_file)

with open(text_dicts_dir + "Descartes-WordSets.pickle", 'rb') as d_file:
    descartes_wordsets = pickle.load(d_file)

# Loading in Markov Chain models for text bots
with open('TextGeneratorModels/descartes-bot.json') as json_file:
    d_model_json = json.load(json_file)
descartes_bot = markovify.Text.from_json(d_model_json)

with open('TextGeneratorModels/woolf-bot.json') as json_file:
    w_model_json = json.load(json_file)
woolf_bot = markovify.Text.from_json(w_model_json)

# Gets sentences containing the given phrase from the given wordsets and sentences
def get_author_sentences(phrase, wordsets, sentences):
    found_ids = []
    found_sentences = []
    for s_id in wordsets:
        words = phrase.split(' ')
        for word in words:
            if word in wordsets[s_id]:
                found_ids.append(s_id)

    for s_id in found_ids:
        found_sentences.append(sentences[s_id])
    return found_sentences

# Searches for an input phrase, returns sentences found from each author (as one big string each)
def text_search(phrase):
    txt_input = phrase.strip()
    woolf_result = ""
    descartes_result = ""
    if len(txt_input) == 0:
        woolf_result = "Input was empty! Try again"
        descartes_result = "Input was empty! Try again"
    else:
        woolf_result = get_author_sentences(txt_input, woolf_wordsets, woolf_sentences)
        descartes_result = get_author_sentences(txt_input, descartes_wordsets, descartes_sentences)
        if len(woolf_result) == 0:
            woolf_result = ["None of Woolf's writing contains this phrase..."]
        if len(descartes_result) == 0:
            descartes_result = ["None of Descartes' writing contains this phrase..."]
    return descartes_result, woolf_result

# Generate sentences from the Markov Chain models that contain the given phrase
def bot_talk(phrase):
    words = phrase.split()
    descartes_bot_res = []
    woolf_bot_res = []
    # Creates 100 sentences (randomly) for both models
    for i in range(100):
        d_sen = descartes_bot.make_sentence()
        w_sen = woolf_bot.make_sentence()
        # Only include in generated results if sentence has (any word in) given phrase
        for w in words:
            if (' ' + w + ' ') in (' ' + d_sen + ' '):
                descartes_bot_res.append(d_sen)
            if (' ' + w + ' ') in (' ' + w_sen + ' '):
                woolf_bot_res.append(w_sen)
    return descartes_bot_res, woolf_bot_res


# HOME/SEARCH PAGE #############################################################
@app.route('/')
def main_page():
    return render_template('text-search.html')

# Gets input from user and returns strings found from text
@app.route('/', methods=['POST'])
def get_results():
    search_input = request.form['text-input']
    descartes_result, woolf_result = text_search(search_input)
    if not (isinstance(descartes_result, list) and isinstance(woolf_result, list)):
        return render_template('text-search-error.html', issue=descartes_result)
    return render_template('text-results.html', descartes_result=descartes_result,
        woolf_result=woolf_result, search_input=search_input)


# TEXTBOTS PAGE ################################################################
@app.route('/textbots')
def textbots_page():
    return render_template('text-bots.html')

# Gets input from user and returns generated text
@app.route('/textbots', methods=['POST'])
def gen_text():
    gen_input = request.form['text-input']
    descartes_bot_res, woolf_bot_res = bot_talk(gen_input)
    return render_template('text-bots-results.html', descartes_result=descartes_bot_res,
        woolf_result=woolf_bot_res, gen_input=gen_input)


# ABOUT PAGE ###################################################################
@app.route('/about')
def about_page():
    return render_template('about.html')


# UNCOMMENT FOR LOCAL RUN ONLY
# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=8080, debug=True)
