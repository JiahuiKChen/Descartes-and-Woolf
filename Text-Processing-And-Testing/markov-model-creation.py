import markovify
import json

# Descartes corpus/model
d_text = open("Texts/Descartes-Corpus.txt", encoding="utf-8").read()

d_model = markovify.Text(d_text)

# Print five randomly-generated sentences
# for i in range(5):
#     print(d_model.make_sentence())

# Save the model
d_model_json = d_model.to_json()
with open('descartes-bot.json', 'w') as outfile:
    json.dump(d_model_json, outfile)
