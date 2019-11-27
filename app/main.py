from flask import Flask
from flask import render_template
import pickle

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

    
def get_author_sentences(phrase, wordsets, sentences):   
    found_ids = []
    found_sentences = []
    for s_id in wordsets:
        if phrase in wordsets[s_id]:
            found_ids.append(s_id)
    
    for s_id in found_ids:
        found_sentences.append(sentences[s_id])
    result_str = "\n\n".join(found_sentences)
    return result_str

# Searches for an input phrase, returns sentences found from each author (as one big string each)
def text_search(phrase):
    txt_input = phrase.strip()
    woolf_results = ""
    descartes_results = ""
    if len(text_input) == 0:
        woolf_results = "Input was empty! Try again"
        descartes_results = "Input was empty! Try again"
    else:
        woolf_result = get_author_sentences(txt_input, woolf_wordsets, woolf_sentences)
        descartes_result = get_author_sentences(txt_input, descartes_wordsets, descartes_sentences)
        
        
@app.route('/')
def main_page():
#     return str(len(descartes_wordsets))
    return render_template('text-search.html')

# Method that gets input from user and returns strings found from text
# @app.route('/', methods=['POST'])
# def get_text():

# UNCOMMENT FOR LOCAL RUN ONLY
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
