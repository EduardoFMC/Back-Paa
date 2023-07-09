import csv
import os
import json

filedir = os.path.dirname(os.path.realpath(__file__))

pokemons = {
  # pokemon_name: [{ tag: "type", patterns: ["What is the type of pokemon_name?"], responses: [pokemon_type] }]
}

with open(f'{filedir}/data/1st_gen.csv', mode="r", encoding="utf-8") as csv_file:
  csv_reader = csv.DictReader(csv_file)

  for i, row in enumerate(csv_reader):
    pokemon_name = row["name"]
    pokemons[pokemon_name] = []
    
    types = row["type1"] + ("" if row["type2"] == "" else " and " + row["type2"])
    pokemons[pokemon_name].append({
      "tag": f"{pokemon_name} - type",
      "patterns": [
        f"what type is {pokemon_name}?",
        f"what type of pokemon is {pokemon_name}?",
        f"what is {pokemon_name}'s type?",
        f"{pokemon_name}'s type?",
        f"type of {pokemon_name}?",
        f"what elemental type is {pokemon_name}?",
        f"what is the elemental type of {pokemon_name}?",
        f"{pokemon_name} elemental type?",
        f"elemental type of {pokemon_name}?",
        f"what category does {pokemon_name} belong to?",
        f"{pokemon_name} belongs to what category?",
        f"what is the category of {pokemon_name}?",
        f"category of {pokemon_name}?",
        f"{pokemon_name} category?",
        f"{pokemon_name}'s category?",
        f"{pokemon_name}'s elemental type?"
      ],
      "responses": [
        f"{pokemon_name} is a {types} type pokemon.",
        f"It is a {types} type pokemon.",
      ]
    })

    abilities = row["abilities"].replace("[", "").replace("]", "").replace("'", "").split(r",\s?")
    abilities = ', '.join(abilities)
    pokemons[pokemon_name].append({
      "tag": f"{pokemon_name} - abilities",
      "patterns": [
        f"What are the abilities of {pokemon_name}?",
        f"what are {pokemon_name}'s abilities?",
        f"what abilities does {pokemon_name} have?",
        f"what abilities does {pokemon_name} possess?",
        f"what abilities does {pokemon_name} know?",
        f"abilities of {pokemon_name}?",
        f"What are the abilities of {pokemon_name}?",
        f"What abilities does {pokemon_name} have?",
        f"What are {pokemon_name}'s abilities?",
        f"What are the special abilities of {pokemon_name}?",
        f"List the abilities of {pokemon_name}."
      ],
      "responses": [
        f"{pokemon_name} has {abilities} abilities.",
        f"It has {abilities} abilities.",
      ]
    })

    legendary = "yes" if row["is_legendary"] == "1" else "no"
    legendary_comp = "" if row["is_legendary"] == "1" else "not"
    pokemons[pokemon_name].append({
      "tag": f"{pokemon_name} - is legendary",
      "patterns": [
        f"Is {pokemon_name} legendary?",
        f"is {pokemon_name} a legendary pokemon?",
        f"is {pokemon_name} considered a legendary?",
        f"is {pokemon_name} a legendary?",
        f"is {pokemon_name} a legendary pokemon?",
        f"is {pokemon_name} considered as a legendary pokemon?",
        f"is {pokemon_name} one of the legendary pokemon?",
        f"does {pokemon_name} belong to the legendary pokemon?",
        f"is {pokemon_name} classified as a legendary pokemon?",
        f"is {pokemon_name} part of the legendary pokemon group?",
        f"is {pokemon_name} included in the legendary pokemon category?",
        f"is {pokemon_name} in the list of legendary pokemon?",
        f"is {pokemon_name} among the legendary pokemon?",
        f"is {pokemon_name} recognized as a legendary pokemon?"
      ],
      "responses": [
        legendary,
        f"{pokemon_name} is {legendary_comp} legendary.",
        f"It is {legendary_comp} legendary.",
      ]
    })

    # weight = row["weight_kg"]
    # pokemons[pokemon_name].append({ 
    #   "tag": f"{pokemon_name} - weight",
    #   "patterns": [f"What is the weight of {pokemon_name}?"],
    #   "responses": [weight +" kg"]
    # })
    
    # pokedex_number = row["pokedex_number"]
    # pokemons[pokemon_name].append({
    #   "tag": f"{pokemon_name} - pokedex number",
    #   "patterns": [f"What is the pokedex number of {pokemon_name}?"],
    #   "responses": [f"{pokemon_name} is the pokemon number {pokedex_number} in the pokedex."]
    # })
    
    # height = row["height_m"]
    # pokemons[pokemon_name].append({
    #   "tag": f"{pokemon_name} - height",
    #   "patterns": [f"What is the height of {pokemon_name}?"],
    #   "responses": [height + " meters"]
    # })

    classification = row["classfication"]
    pokemons[pokemon_name].append({
      "tag": f"{pokemon_name} - classification",
      "patterns": [
        f"What is the classification of {pokemon_name}?",
        f"how is {pokemon_name} classified?",
        f"what is {pokemon_name} classified as?",
        f"what is {pokemon_name}?",
        f"what {pokemon_name}?",
        f"what is the classification of {pokemon_name}?",
        f"what is the category of {pokemon_name}?",
        f"how is {pokemon_name} classified?",
        f"what group does {pokemon_name} belong to?",
        f"what is the classification of {pokemon_name} pokemon?",
        f"what is the categorization of {pokemon_name}?",
        f"what is the class of {pokemon_name}?",
        f"what is the designation of {pokemon_name}?",
        f"how is {pokemon_name} categorized?",
        f"what is the type of {pokemon_name}?"
      ],
      "responses": [
        f"{pokemon_name} is a {classification}.",
        f"It is a {classification}.",
      ]
    })

    types = ['bug', 'dark', 'dragon', 'electric', 'fairy', 'fight', 'fire', 'flying', 'ghost', 'grass', 'ground', 'ice', 'normal', 'poison', 'psychic', 'rock', 'steel', 'water']
    for t in types:
      is_weak = "yes" if float(row[f"against_{t}"]) > 1 else "no"
      is_weak_comp = "" if float(row[f"against_{t}"]) > 1 else "not"
      pokemons[pokemon_name].append({
        "tag": f"{pokemon_name} - weak against",
        "patterns": [
          f"Is {pokemon_name} weak against {t}?",
          f"Is {t} strong against {pokemon_name}?",
          f"{t} type is strong against {pokemon_name}?",
          f"is {pokemon_name} weak to {t}?",
          f"is {t} type effective against {pokemon_name}?",
          f"does {pokemon_name} have a weakness to {t}?",
          f"is {pokemon_name} vulnerable to {t} attacks?",
          f"can {t} moves do extra damage to {pokemon_name}?",
          f"is {pokemon_name} easily defeated by {t} type moves?",
          f"is {pokemon_name} susceptible to {t} type attacks?",
          f"is {pokemon_name} disadvantageous against {t} type pokemon?",
          f"does {t} type have an advantage over {pokemon_name}?"
        ],
        "responses": [
          is_weak,
          f"{pokemon_name} is {is_weak_comp} weak against {t}.",
          f"It is {is_weak_comp} weak against {t}.",
        ]
      })

      is_strong = "yes" if float(row[f"against_{t}"]) < 1 else "no"
      is_strong_comp = "" if float(row[f"against_{t}"]) < 1 else "not"
      pokemons[pokemon_name].append({
        "tag": f"{pokemon_name} - strong against",
        "patterns": [
          f"Is {pokemon_name} strong against {t}?",
          f"Is {t} weak against {pokemon_name}?",
          f"{t} type is weak against {pokemon_name}?",
          f"is {pokemon_name} strong against {t}?",
          f"is {pokemon_name} resistant to {t}?",
          f"does {pokemon_name} have an advantage against {t} type?",
          f"is {pokemon_name} immune to {t} attacks?",
          f"can {pokemon_name} take less damage from {t} moves?",
          f"is {pokemon_name} effective in battling {t} type pokemon?",
          f"is {pokemon_name} powerful against {t} type moves?",
          f"is {pokemon_name} advantageous against {t} type pokemon?",
          f"does {pokemon_name} have a type advantage over {t} type?",
          f"is {pokemon_name} good at countering {t} type attacks?"
        ],
        "responses": [
          is_strong,
          f"{pokemon_name} is {is_strong_comp} strong against {t}.",
          f"It is {is_strong_comp} strong against {t}.",
        ]
      })


# build questions_answers
questions_answers = []
for pokemon_name, questions in pokemons.items():
  for q in questions:
    questions_answers.append({
      "tag": q["tag"],
      "patterns": q["patterns"],
      "responses": q["responses"],
    })

intents_json = {"intents": []}

if os.path.exists(f'{filedir}/data/intents.json'):
  intents_file = open(f'{filedir}/data/intents.json', mode="r", encoding="utf-8").read()
  intents_json = json.loads(intents_file)

intents_json["intents"].extend(questions_answers)

with open(f'{filedir}/data/intents.json', mode="w", encoding="utf-8") as intents_file:
  json.dump(intents_json, intents_file, indent=2)

print(f"Added {len(questions_answers)} questions to intents.json")
