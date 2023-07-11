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
  def __init__(self, model_name='pguess'):
    self.lemmatizer = WordNetLemmatizer()
    self.stop_words = stopwords.words('english')
    self.ignore_letters = ['?', '!', '.', ',']

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
    self.pguess = ModelLoader('pguess')
    self.qtype = ModelLoader('qtype')
    self.ptype = ModelLoader('ptype')
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
  
  def filter_pokemon_by_ptype(self, ptype):
    return [pokemon for pokemon in list(pokemons_csv) if pokemon["type1"] == ptype or pokemon["type2"] == ptype]

  def ans_suggestions(self, ptype):
    pokemons = self.filter_pokemon_by_ptype(ptype)
    pokemons = [pokemon["name"].capitalize() for pokemon in pokemons]
    pokemons = ', '.join(pokemons)
    return f"Pokemon that are {ptype} type are {pokemons}."
  
  def ans_type(self, pok):
    type1 = pok["type1"].capitalize()
    type2 = pok["type2"].capitalize()
    types = type1
    if type2 != "":
      types += f"/{type2}"
    return f"{pok['name'].capitalize()} is {types} type."
  
  def ans_abilities(self, pok):
    abilities = pok["abilities"].replace("[", "").replace("]", "").replace("'", "").split(r",\s?")
    if len(abilities) == 1:
      abilities = abilities[0]
    else:
      abilities = ', '.join(abilities[:-1]) + f" and {abilities[-1]}"

    return f"{pok['name'].capitalize()} has {abilities} abilities."
  
  def ans_legendary(self, pok):
    legendary_comp = "" if pok["is_legendary"] == "1" else " not"
    return f"{pok['name'].capitalize()} is{legendary_comp} a legendary pokemon."

  def ans_classification(self, pok):
    classification = pok["classification"]
    return f"{pok['name'].capitalize()} is a {classification}."
  
  def ans_weak_against(self, pok, ptype):
    is_weak = "" if float(pok[f"against_{ptype}"]) > 1 else " not"
    return f"{pok['name'].capitalize()} is{is_weak} weak against {ptype}."
  
  def ans_strong_against(self, pok, ptype):
    is_strong = "" if float(pok[f"against_{ptype}"]) < 1 else " not"
    return f"{pok['name']} is{is_strong} strong against {ptype}."
  
  def ans_evolutions(self, pokemon):
    evolutions = pokemon['evolutions'].split(',')
    if len(evolutions) == 1:
      return f"{pokemon['name']} does not evolve."

    evolutions = [evolution.capitalize() for evolution in evolutions]

    if (pokemon['name'].lower() == 'eevee'):
      evolutions = ', '.join(evolutions[1:-1]) + f" and {evolutions[-1]}"
      return f"{pokemon['name']} evolves into one of the following: {evolutions}."

    evolutions = ', '.join(evolutions[:-1]) + f" and {evolutions[-1]}"
    return f"The evolution chain that {pokemon['name']} is part of is: {evolutions}."

  def talking_about(self, question):
    pguess = self.pguess.get_response(question)
    pokemon_name, pname_prob = pguess['intent'], float(pguess['probability'])
    pname_found = self.message_has_some_pname(question)
    if pname_found:
      pokemon_name = pname_found
      pname_prob = 1.0

    qtype = self.qtype.get_response(question)
    qtype, qtype_prob = qtype['intent'], float(qtype['probability'])

    ptype = self.ptype.get_response(question)
    ptype, ptype_prob = ptype['intent'], float(ptype['probability'])


    return {
      'qtype': qtype,
      'qtype_prob': qtype_prob,
      'pguess': pokemon_name,
      'pguess_prob': pname_prob,
      'ptype': ptype,
      'ptype_prob': ptype_prob,
    }
  
  def answer(self, question):
    tab = self.talking_about(question)
    pokemon_name, pname_prob = tab['pguess'], tab['pguess_prob']
    ptype, ptype_prob = tab['ptype'], tab['ptype_prob']
    qtype, qtype_prob = tab['qtype'], tab['qtype_prob']

    pokemon = self.find_pokemon(pokemon_name)
    pokemon_name = pokemon_name.capitalize()

    infos = {
      'pokemon_name': pokemon_name,
      'pokemon_name_prob': pname_prob,
      'pokemon_type': ptype,
      'pokemon_type_prob': ptype_prob,
      'question_type': qtype,
      'question_type_prob': qtype_prob,
    }

    res = ''
    if qtype_prob < 0.4:
      res = "I don't know what you're asking about."

    elif qtype == "suggestions":
      if ptype != "none":
        res = self.ans_suggestions(ptype)
      else:
        res = self.ans_classification(pokemon) # try to guess the pokemon

    elif pname_prob < 0.4:
      res = "I don't know which pokemon you're talking about."
    
    elif qtype == "type":
      res = self.ans_type(pokemon)
    elif qtype == "abilities":
      res = self.ans_abilities(pokemon)
    elif qtype == "is_legendary":
      res = self.ans_legendary(pokemon)
    elif qtype == "weak_against":
      res = self.ans_weak_against(pokemon, ptype)
    elif qtype == "strong_against":
      res = self.ans_strong_against(pokemon, ptype)
    elif qtype == "classification":
      res = self.ans_classification(pokemon)
    elif qtype == "evolutions":
      res = self.ans_evolutions(pokemon)

    return {
      'question': question,
      'answer': res,
      'statistics': infos,
    }




questionAnswerer = PokeQuestionAnswerer()

print("Welcome to the Pokemon Chatbot!")
while True:
  message = input("You > ")
  res = questionAnswerer.answer(message)
  print(f"Bot > {res['answer']}\n{res['statistics']}\n{'-'*50}")

