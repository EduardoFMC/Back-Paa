print('Initializing...')

import random
import json
import pickle
import numpy as np
import os

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

from timeit import default_timer as timer


filedir = os.path.dirname(os.path.realpath(__file__))

lemmatizer = WordNetLemmatizer()

try:
  lemmatizer.lemmatize('word')
  nltk.word_tokenize('test')
  stopwords.words('english')
except LookupError:
  print('Downloading NLTK packages...')
  nltk.download('wordnet')
  nltk.download('punkt')
  nltk.download('stopwords')

print('NLTK packages loaded.')

print('Expects intents.json to be in the following format:')
print('''
[
  {
    "tag": "type",
    "patterns": [
      "what type is pokemon_name?",
      "what type of pokemon is pokemon_name?",
    ],
    "responses": [
      "pokemon_name is type."
    ]
  }
]
''')
      

intents_filename = input('Intents path (eg. ./data/intents.json): ')
output_foldername = input('Output folder name (eg. mymodel): ')
epochs = input('Epochs (default 30): ')
learning_rate = input('Learning rate (default 0.01): ')
batch_size = input('Batch size (default 16): ')

t_start = timer()

epochs = 30 if epochs == '' else int(epochs)
learning_rate = 0.01 if learning_rate == '' else float(learning_rate)
batch_size = 16 if batch_size == '' else int(batch_size)

print('=' * 50)
print('Loading data...')

model_folder = f'{filedir}/models/{output_foldername}'

intents_file = open(f'{filedir}/{intents_filename}', mode="r", encoding="utf-8").read()
intents = json.loads(intents_file)

words, classes, documents = [], [], []
ignore_letters = ['?', '!', '.', ',']
stop_words = stopwords.words('english')

for intent in intents:
  for pattern in intent['patterns']:
    word_list = nltk.word_tokenize(pattern)
    word_list = [word.split('-') for word in word_list]
    word_list = [item for sublist in word_list for item in sublist] # flatten list
    word_list = [word.split('/') for word in word_list]
    word_list = [item for sublist in word_list for item in sublist] # flatten list
    word_list = [word for word in word_list if word.lower() not in stop_words]
    words.extend(word_list)
    documents.append((word_list, intent['tag']))

    if intent['tag'] not in classes:
      classes.append(intent['tag'])

print('Data loaded.')
print('=' * 50)
print('Creating training data...')

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

if not os.path.exists(f'{model_folder}'):
  os.makedirs(f'{model_folder}')

pickle.dump(words, open(f'{model_folder}/words.pkl', mode="wb"))
pickle.dump(classes, open(f'{model_folder}/classes.pkl', mode="wb"))

training = []
output_empty = [0] * len(classes)

for document in documents:
  bag = []
  word_patterns = document[0]
  word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
  for word in words:
    bag.append(1 if word in word_patterns else 0)

  output_row = list(output_empty)
  output_row[classes.index(document[1])] = 1
  training.append(bag + output_row)

random.shuffle(training)

training = np.array(training)

train_x = training[:, :len(words)]
train_y = training[:, len(words):]

print('Training data created.')
print('=' * 50)
print('Creating model...')

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(learning_rate=learning_rate, weight_decay=1e-6, momentum=.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(train_x, train_y, epochs=epochs, batch_size=batch_size, verbose=2)
model_path = f'{model_folder}/model.keras'
model.save(model_path, hist)

execution_time = int(timer() - t_start)
minutes = execution_time // 60
seconds = execution_time % 60
exec_time_str = f'{minutes}m {seconds}s'

print(f'Training completed in {exec_time_str} seconds with {len(train_x)} training samples.')
print(f'Model saved to {model_path}')

# pguess_intents_backup
# lr: 0.01, batch: 8, epochs: 1000 = 0.65
# lr: 0.01, batch: 12, epochs: 1000 = 0.74
# lr: 0.01, batch: 16, epochs: 1000 = 0.76
# lr: 0.0025, batch: 16, epochs: 1000 = 0.77
# lr: 0.003, batch: 10, epochs: 1000 = 0.78
# lr: 0.004, batch: 12, epochs: 1000 = 0.78
# lr: 0.0045, batch: 20, epochs: 1000 = loss: 0.9343 - accuracy: 0.7734
# lr: 0.0045, batch: 8, epochs: 1000 = 0.76
# lr: 0.005, batch: 16, epochs: 1000 = 0.79
# lr: 0.00525, batch: 16, epochs: 1000 = loss: 0.9149 - accuracy: 0.7818 - 109ms/epoch
# lr: 0.0055, batch: 16, epochs: 1000 = loss: 0.8965 - accuracy: 0.7894 - 171ms/epoch
# lr: 0.005525, batch: 16, epochs: 1000 = loss: 0.9197 - accuracy: 0.7869 - 174ms/epoch
# lr: 0.0056375, batch: 16, epochs: 1000 = loss: 0.9071 - accuracy: 0.7869 - ms/epoch
# lr: 0.00575, batch: 16, epochs: 1000 = loss: 0.8899 - accuracy: 0.7928 - 109ms/epoch
# lr: 0.005875, batch: 16, epochs: 1000 = loss: 0.9178 - accuracy: 0.7902 - 174ms/epoch
# lr: 0.006, batch: 16, epochs: 1000 = loss: 0.9222 - accuracy: 0.7784 - 170ms/epoch
# lr: 0.0062, batch: 16, epochs: 1000 = loss: 0.9269 - accuracy: 0.7810 - ms/epoch
# lr: 0.0066, batch: 16, epochs: 1000 = loss: 0.9035 - accuracy: 0.7894 - 189ms/epoch
# lr: 0.0068, batch: 16, epochs: 1000 = loss: 0.9156 - accuracy: 0.7810 - ms/epoch
# lr: 0.007, batch: 16, epochs: 1000 = loss: 0.8810 - accuracy: 0.7953 - 109ms/epoch
# lr: 0.0071, batch: 16, epochs: 1000 = loss: 0.9192 - accuracy: 0.7860 - 109ms/epoch

# lr: 0.007, batch: 5, epochs: 1000 = loss: 1.4793 - accuracy: 0.6622 - 491ms/epoch
# lr: 0.007, batch: 8, epochs: 1000 = loss: 1.0925 - accuracy: 0.7439 - 315ms/epoch - 2ms/step
# lr: 0.007, batch: 14, epochs: 1000 = loss: 0.9506 - accuracy: 0.7683 - 125ms/epoch
# lr: 0.007, batch: 20, epochs: 1000 = loss: 0.9317 - accuracy: 0.7767 - 94ms/epoch

# lr: 0.007, batch: 16, epochs: 3000 = loss: 0.8362 - accuracy: 0.8155 - 109ms/epoch


# qtype_intents
# lr: 0.01, batch: 16, epochs: 10 = loss: 5.2128e-04 - accuracy: 0.9999 - 4s/epoch

