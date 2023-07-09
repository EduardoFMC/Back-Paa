import csv
import os
import json

filedir = os.path.dirname(os.path.realpath(__file__))

intents = {
  # tag_name: ["What is the type of pokemon_name?"] <- patterns
  "type": [],
  "abilities": [],
  "is_legendary": [],
  "classification": [],
}

with open(f'{filedir}/data/1st_gen.csv', mode="r", encoding="utf-8") as csv_file:
  csv_reader = csv.DictReader(csv_file)

  for i, row in enumerate(csv_reader):
    pokemon_name = row["name"]
    
    types = row["type1"] + ("" if row["type2"] == "" else " and " + row["type2"])
    intents["type"].extend([
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
      f"{pokemon_name} category?",
      f"{pokemon_name} type?",
      f"type of {pokemon_name}?",
      f"Which type characterize {pokemon_name}?",
      f"What is {pokemon_name}'s predominant type?",
      f"Provide the main type for {pokemon_name}.",
      f"{pokemon_name} is associated with which elemental type?",
      f"Tell me the elemental affinity of {pokemon_name}.",
      f"What type define {pokemon_name}?",
      f"Give me the primary elemental type of {pokemon_name}.",
      f"Which type represent {pokemon_name}?",
      f"List the predominant type of {pokemon_name}.",
      f"What is the elemental typing of {pokemon_name}?",
      f"Tell me the primary elemental type of {pokemon_name}.",
      f"What type is {pokemon_name} mainly classified as?",
      f"Which elemental type is {pokemon_name} attributed to?",
      f"Name the core type of {pokemon_name}.",
      f"{pokemon_name} is primarily associated with which type?",
      f"Tell me the key type of {pokemon_name}.",
      f"What elemental attribute does {pokemon_name} have?",
      f"Provide the elemental classification of {pokemon_name}.",
      f"{pokemon_name} is characterized by which type?",
      f"What is {pokemon_name}'s elemental category?",
      f"Tell me the elemental nature of {pokemon_name}.",
      f"Which type does {pokemon_name} primarily possess?",
      f"What type is {pokemon_name} typically known for?",
      f"List the typical type of {pokemon_name}.",
      f"What is {pokemon_name}'s typical elemental type?",
      f"Tell me the commonly seen type of {pokemon_name}.",
      f"Which type are commonly associated with {pokemon_name}?",
      f"What type are frequently found in {pokemon_name}?",
      f"List the often-encountered type of {pokemon_name}.",
      f"What type are usually linked to {pokemon_name}?",
      f"Tell me the usual type of {pokemon_name}.",
      f"Which type does {pokemon_name} commonly possess?",
      f"What type are commonly observed in {pokemon_name}?",
      f"List the frequently seen type of {pokemon_name}.",
      f"What type are typically associated with {pokemon_name}?",
      f"Tell me the general type of {pokemon_name}.",
      f"Which type does {pokemon_name} generally belong to?",
      f"What type are typically found in {pokemon_name}?",
      f"List the commonly encountered type of {pokemon_name}.",
      f"What type are generally linked to {pokemon_name}?",
      f"Tell me the general type of {pokemon_name} typically observed.",
      f"Which type does {pokemon_name} generally possess?",
      f"What type are generally observed in {pokemon_name}?",
      f"List the commonly known type of {pokemon_name}.",
      f"What is {pokemon_name}'s usual elemental type?",
      f"Tell me the typically seen type of {pokemon_name}.",
      f"Which type does {pokemon_name} usually possess?",
      f"What type are usually observed in {pokemon_name}?",
      f"List the frequently identified type of {pokemon_name}.",
      f"What type are usually associated with {pokemon_name}?",
      f"Tell me the common type of {pokemon_name}.",
      f"Which type does {pokemon_name} typically fall under?",
      f"What type are typically observed in {pokemon_name}?",
      f"List the commonly recognized type of {pokemon_name}.",
      f"What type are typically linked to {pokemon_name}?"
    ])

    abilities = row["abilities"].replace("[", "").replace("]", "").replace("'", "").split(r",\s?")
    abilities = ', '.join(abilities)
    intents["abilities"].extend([
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
      f"List the abilities of {pokemon_name}.",
      f"{pokemon_name} abilities are?",
      f"{pokemon_name} abilities?",
      f"List the general abilities of {pokemon_name} typically observed.",
      f"What abilities are usually associated with {pokemon_name}?",
      f"Tell me the common abilities of {pokemon_name}.",
      f"Which abilities does {pokemon_name} usually possess?",
      f"What are the common abilities of {pokemon_name}?",
      f"List the common abilities of {pokemon_name}.",
      f"Tell me the common abilities of {pokemon_name} typically observed.",
      f"What abilities are usually observed in {pokemon_name}?",
      f"Which abilities does {pokemon_name} commonly possess?",
      f"What are {pokemon_name}'s usual abilities?",
      f"List the frequently seen abilities of {pokemon_name}.",
      f"Tell me the abilities commonly associated with {pokemon_name}.",
      f"Which abilities does {pokemon_name} frequently have?",
      f"List the usual abilities of {pokemon_name}.",
      f"What abilities are commonly found in {pokemon_name}?",
      f"Tell me the abilities typically seen in {pokemon_name}.",
      f"Which abilities does {pokemon_name} often possess?",
      f"What are the typical abilities of {pokemon_name}?",
      f"List the abilities typically associated with {pokemon_name}.",
      f"Tell me the abilities frequently found in {pokemon_name}.",
      f"Which abilities does {pokemon_name} typically possess?",
      f"What are the abilities generally observed in {pokemon_name}?",
      f"List the abilities commonly recognized in {pokemon_name}.",
      f"Tell me the abilities usually linked to {pokemon_name}.",
      f"Which abilities does {pokemon_name} generally have?",
      f"What are {pokemon_name}'s general abilities?",
      f"List the abilities generally found in {pokemon_name}.",
      f"Tell me the general abilities of {pokemon_name} typically observed."
    ])

    legendary = "yes" if row["is_legendary"] == "1" else "no"
    legendary_comp = "" if row["is_legendary"] == "1" else "not"
    intents["is_legendary"].extend([
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
      f"Does {pokemon_name} have the status of a legendary Pokémon?",
      f"Is {pokemon_name} designated as a legendary Pokémon?",
      f"Tell me if {pokemon_name} is identified as a legendary Pokémon.",
      f"Is {pokemon_name} considered one of the legendary Pokémon species?",
      f"Does {pokemon_name} possess the characteristics of a legendary Pokémon?",
      f"Is {pokemon_name} part of the legendary Pokémon group?",
      f"Tell me if {pokemon_name} is counted among the legendary Pokémon.",
      f"Is {pokemon_name} a legendary Pokémon or a regular Pokémon?",
      f"Does {pokemon_name} have the distinction of being a legendary Pokémon?",
      f"Is {pokemon_name} known as a legendary Pokémon or a regular Pokémon?",
      f"Tell me if {pokemon_name} is classified as a legendary or regular Pokémon.",
      f"Is {pokemon_name} included in the legendary Pokémon category or regular Pokémon category?",
      f"Does {pokemon_name} possess the characteristics of a legendary or regular Pokémon?",
      f"Is {pokemon_name} confirmed to be a legendary or regular Pokémon?",
      f"Tell me if {pokemon_name} is acknowledged as a legendary or regular Pokémon.",
      f"Is {pokemon_name} recognized as a legendary or regular Pokémon?",
      f"Does {pokemon_name} have the status of a legendary or regular Pokémon?",
      f"Is {pokemon_name} designated as a legendary or regular Pokémon?",
      f"Tell me if {pokemon_name} is identified as a legendary or regular Pokémon.",
      f"Is {pokemon_name} considered one of the legendary or regular Pokémon species?",
      f"Does {pokemon_name} have the characteristics of a legendary or regular Pokémon?",
      f"Is {pokemon_name} part of the legendary or regular Pokémon group?",
      f"Tell me if {pokemon_name} is counted among the legendary or regular Pokémon.",
      f"Is {pokemon_name} a legendary Pokémon or an ordinary Pokémon?",
      f"Does {pokemon_name} have the distinction of being a legendary Pokémon or an ordinary Pokémon?",
      f"Is {pokemon_name} known as a legendary Pokémon or an ordinary Pokémon?",
      f"Tell me if {pokemon_name} is classified as a legendary Pokémon or an ordinary Pokémon.",
      f"Is {pokemon_name} included in the legendary Pokémon category or ordinary Pokémon category?",
      f"Does {pokemon_name} possess the characteristics of a legendary Pokémon or an ordinary Pokémon?",
      f"Is {pokemon_name} confirmed to be a legendary Pokémon or an ordinary Pokémon?",
      f"Tell me if {pokemon_name} is acknowledged as a legendary Pokémon or an ordinary Pokémon.",
      f"Is {pokemon_name} recognized as a legendary Pokémon or an ordinary Pokémon?",
      f"Does {pokemon_name} have the status of a legendary Pokémon or an ordinary Pokémon?",
      f"Is {pokemon_name} designated as a legendary Pokémon or an ordinary Pokémon?",
      f"Tell me if {pokemon_name} is identified as a legendary Pokémon or an ordinary Pokémon.",
      f"Is {pokemon_name} considered one of the legendary Pokémon species or ordinary Pokémon species?",
      f"Does {pokemon_name} have the characteristics of a legendary Pokémon or an ordinary Pokémon?",
      f"Is {pokemon_name} part of the legendary Pokémon group or ordinary Pokémon group?",
      f"Tell me if {pokemon_name} is counted among the legendary Pokémon or ordinary Pokémon.",
      f"Is {pokemon_name} a legendary or non-legendary Pokémon?",
      f"Does {pokemon_name} have the distinction of being a legendary or non-legendary Pokémon?",
      f"Is {pokemon_name} known as a legendary or non-legendary Pokémon?",
      f"Tell me if {pokemon_name} is classified as a legendary or non-legendary Pokémon.",
      f"Is {pokemon_name} included in the legendary Pokémon category or non-legendary Pokémon category?",
      f"Does {pokemon_name} possess the characteristics of a legendary or non-legendary Pokémon?",
      f"Is {pokemon_name} confirmed to be a legendary or non-legendary Pokémon?",
      f"Tell me if {pokemon_name} is acknowledged as a legendary or non-legendary Pokémon.",
      f"Is {pokemon_name} recognized as a legendary or non-legendary Pokémon?",
      f"Does {pokemon_name} have the status of a legendary or non-legendary Pokémon?",
      f"Is {pokemon_name} designated as a legendary or non-legendary Pokémon?",
      f"Tell me if {pokemon_name} is identified as a legendary or non-legendary Pokémon.",
      f"Is {pokemon_name} considered one of the legendary or non-legendary Pokémon species?",
      f"Does {pokemon_name} have the characteristics of a legendary or non-legendary Pokémon?",
      f"Is {pokemon_name} part of the legendary or non-legendary Pokémon group?",
      f"Tell me if {pokemon_name} is counted among the legendary or non-legendary Pokémon."
    ])

    classification = row["classfication"]
    intents["classification"].extend([
      f"What is the classification of {pokemon_name}?",
      f"how is {pokemon_name} classified?",
      f"what is {pokemon_name} classified as?",
      f"what is {pokemon_name}?",
      f"what {pokemon_name}?",
      f"what is the classification of {pokemon_name}?",
      f"how is {pokemon_name} classified?",
      f"what is the classification of {pokemon_name}?",
      f"what is the class of {pokemon_name}?",
      f"what is the designation of {pokemon_name}?",
      f"how is {pokemon_name} categorized?",
      f"Which designation does {pokemon_name} possess?",
      f"Give me the class label of {pokemon_name}.",
      f"Tell me the designation assigned to {pokemon_name}.",
      f"What is the class designation of {pokemon_name}?",
      f"Provide the classification category of {pokemon_name}.",
      f"What class is {pokemon_name} grouped into?",
      f"Tell me the class assignment of {pokemon_name}.",
      f"Which designation is associated with {pokemon_name}?",
      f"Give me the class designation of {pokemon_name}.",
      f"Tell me the designation category of {pokemon_name}.",
      f"What is the classification class of {pokemon_name}?",
      f"Provide the class designation of {pokemon_name}.",
      f"What class is {pokemon_name} classified as?",
      f"Tell me the class designation of {pokemon_name}.",
      f"Which class is assigned to {pokemon_name}?",
      f"Give me the class classification of {pokemon_name}.",
      f"Tell me the designation class of {pokemon_name}.",
      f"What is the classification class of {pokemon_name}?",
      f"Provide the class category of {pokemon_name}.",
      f"What class is {pokemon_name} categorized as?",
      f"Tell me the class type of {pokemon_name}.",
      f"Which designation does {pokemon_name} possess?",
      f"Give me the class label of {pokemon_name}.",
      f"Tell me the designation assigned to {pokemon_name}.",
      f"What is the class designation of {pokemon_name}?",
      f"Provide the classification category of {pokemon_name}.",
      f"What class is {pokemon_name} grouped into?",
      f"Tell me the class assignment of {pokemon_name}.",
      f"Which designation is associated with {pokemon_name}?"
    ])


# build questions_answers
formatted_intents = []
for tag, patterns in intents.items():
  formatted_intents.append({
    "tag": tag,
    "patterns": patterns,
    "responses": [tag],
  })


if os.path.exists(f'{filedir}/data/intents.json'):
  intents_file = open(f'{filedir}/data/intents.json', mode="r", encoding="utf-8").read()

filename = 'qtype_intents.json'

with open(f'{filedir}/data/{filename}', mode="w", encoding="utf-8") as intents_file:
  json.dump(formatted_intents, intents_file, indent=2)

print(f"Added {len(formatted_intents)} questions to {filename}")
