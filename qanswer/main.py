import json
import pickle
import numpy as np
import os
import csv

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from tensorflow.keras.models import load_model

filedir = os.path.dirname(os.path.realpath(__file__))

csv_file = open(f'{filedir}/data/1st_gen.csv', mode="r", encoding="utf-8")
pokemons_csv = list(csv.DictReader(csv_file))

try:
  nltk.word_tokenize('test')
  stopwords.words('english')
except LookupError:
  print('Downloading NLTK packages...')
  nltk.download('punkt')
  nltk.download('stopwords')


class ModelLoader:
  def __init__(self, model_name='pguess', intents_file='pguess_intents_backup.json'):
    self.lemmatizer = WordNetLemmatizer()
    self.stop_words = stopwords.words('english')
    self.ignore_letters = ['?', '!', '.', ',']

    intents_file = open(f'{filedir}/data/pguess_intents_backup.json', mode="r", encoding="utf-8").read()
    self.list_of_intents = json.loads(intents_file)

    self.words = pickle.load(open(f'{filedir}/models/{model_name}/words.pkl', mode="rb"))
    self.classes = pickle.load(open(f'{filedir}/models/{model_name}/classes.pkl', mode="rb"))
    self.model = load_model(f'{filedir}/models/{model_name}/model.keras')

  def clean_up_sentence(self, sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [word for word in sentence_words if word.lower() not in self.stop_words]
    sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words if word not in self.ignore_letters]
    return sentence_words


  def bag_of_words(self, sentence):
    sentence_words = self.clean_up_sentence(sentence)
    bag = [0] * len(self.words)
    for w in sentence_words:
      for i, word in enumerate(self.words):
        if word == w:
          bag[i] = 1
    return np.array(bag)


  def predict_class(self, sentence):
    bow = self.bag_of_words(sentence)
    res = self.model.predict(np.array([bow]), verbose=0)[0]
    results = [[i, r] for i, r in enumerate(res)]

    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": self.classes[r[0]], "probability": str(r[1])} for r in results]


  def get_response(self, message):
    intents_list = self.predict_class(message)
    return intents_list[0] # {'intent': 'tag', 'probability': '0.9999999'}


class PokeQuestionAnswerer:
  def __init__(self):
    self.pguess = ModelLoader('pguess2', 'pguess_intents_merged_backup.json')
    self.qtype = ModelLoader('qtype', 'qtype_intents.json')
    self.pokemon_names = [pokemon["name"].lower().strip() for pokemon in pokemons_csv]

  def message_has_some_pname(self, message):
    sentence_words = self.pguess.clean_up_sentence(message)
    for word in sentence_words:
      if word in self.pokemon_names:
        return word
    return None
  
  def find_pokemon(self, pokemon_name):
    for pokemon in list(pokemons_csv):
      if pokemon["name"].lower().strip() == pokemon_name.lower().strip():
        return pokemon
    return None

  def talking_about(self, question):
    pguess = self.pguess.get_response(question)
    pokemon_name, pname_prob = pguess['intent'], float(pguess['probability'])
    pname_found = self.message_has_some_pname(question)
    if pname_found:
      pokemon_name = pname_found
      pname_prob = 1.0

    qtype = self.qtype.get_response(question)
    qtype, qtype_prob = qtype['intent'], float(qtype['probability'])

    return {
      'qtype': qtype,
      'qtype_prob': qtype_prob,
      'pguess': pokemon_name,
      'pguess_prob': pname_prob
    }
  
  def answer(self, question):
    tab = self.talking_about(question)
    pokemon_name, pname_prob = tab['pguess'], tab['pguess_prob']
    qtype, qtype_prob = tab['qtype'], tab['qtype_prob']

    pokemon = self.find_pokemon(pokemon_name)
    pokemon_name = pokemon_name.capitalize()

    stats = {
      'pokemon_name': pokemon_name, 
      'pokemon_name_probability': pname_prob,
      'question_type': qtype,
      'question_type_probability': qtype_prob
    }

    if pname_prob < 0.4:
      return {'answer': "I don't know which pokemon you're talking about.", 'statistics': stats}
    if qtype_prob < 0.4:
      return {'answer': "I don't know what you're asking about.", 'statistics': stats}
    
    response = ''
    if qtype == "type":
      type1 = pokemon["type1"].capitalize()
      type2 = pokemon["type2"].capitalize()
      types = type1
      if type2 != "":
        types += f"/{type2}"
      response += f"{pokemon_name} is {types} type."
    elif qtype == "abilities":
      abilities = pokemon["abilities"].replace("[", "").replace("]", "").replace("'", "").split(r",\s?")
      abilities = ', '.join(abilities)
      response += f"{pokemon_name} has {abilities} abilities."
    elif qtype == "is_legendary":
      legendary_comp = "" if pokemon["is_legendary"] == "1" else " not"
      response += f"{pokemon_name} is{legendary_comp} a legendary pokemon."
    elif qtype == "classification":
      classification = pokemon["classification"]
      response += f"{pokemon_name} is a {classification}."

    return {'answer': response, 'statistics': stats}



pokeQuestionAnswerer = PokeQuestionAnswerer()
pokeQuestionAnswerer.answer("What type is Pikachu?") # initialize the model
