import markovify
import json

# Descartes corpus/model
d_text = open("Texts/Descartes-Corpus.txt", encoding="utf-8").read()

d_model = markovify.Text(d_text)

# # Print five randomly-generated sentences
# # for i in range(5):
# #     print(d_model.make_sentence())

# Save the model
d_model_json = d_model.to_json()
with open('descartes-bot.json', 'w') as outfile:
    json.dump(d_model_json, outfile)

# Woolf corpus/model
w_text = open("Texts/Woolf-Corpus.txt", encoding="utf-8").read()

w_model = markovify.Text(w_text)

# Print five randomly-generated sentences
# for i in range(5):
#     print(w_model.make_sentence())

# Save the model
w_model_json = w_model.to_json()
with open('woolf-bot.json', 'w') as outfile:
    json.dump(w_model_json, outfile)
