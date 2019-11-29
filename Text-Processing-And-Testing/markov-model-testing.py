import markovify
import json

with open('descartes-bot.json') as json_file:
    d_model_json = json.load(json_file)

d_model = markovify.Text.from_json(d_model_json)

# Print five randomly-generated sentences
for i in range(5):
    print(d_model.make_sentence())
