#type: ignore

import numpy as np
import pandas as pd
import random
import re

import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
from tensorflow import keras
from ast import literal_eval
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import spacy
nlp = spacy.load('pt_core_news_sm')

SEED_VAL = 42
random.seed(SEED_VAL)
np.random.seed(SEED_VAL)


class Preprocessing:
    def lower_text(text):
        pp_text = text.lower()
        return pp_text

    # def remove_punctuation(text):
    #     pp_text = re.sub(r'c/', ' ', text)
    #     pp_text = re.sub(r'C/', ' ', pp_text)
    #     pp_text = re.sub(r'[-|,|;|:|.|_|*|"|\'|#|\(|\)|\/|\\|\[|\]]', ' ', pp_text)
    #     return pp_text


    def tokenize(text):
        pp_text = word_tokenize(text)
        return pp_text


    # def remove_stopwords(text):
    #     pp_text = [word for word in text if word not in stopwords.words('portuguese')]
    #     return pp_text


    # def lemmatize(text):
    #     doc = nlp(str([palavra for palavra in text]))
    #     pp_text = [token.lemma_ for token in doc if token.pos_ == 'NOUN']
    #     return pp_text

    def apply_preprocessing(df):
        pp_desc_q = []
        pp_desc_a = []
        corpus_pp_desc_q = ''
        corpus_pp_desc_a = ''

        for text in df['question']:
            pp_text = Preprocessing.lower_text(text)
            # pp_text = Preprocessing.replace_quantity_values(pp_text)
            # pp_text = Preprocessing.replace_size_values(pp_text)
            # pp_text = Preprocessing.remove_numbers(pp_text)
            # pp_text = Preprocessing.remove_punctuation(pp_text)
            pp_text = Preprocessing.tokenize(pp_text)
            # pp_text = Preprocessing.remove_stopwords(pp_text)
            # pp_text = Preprocessing.lemmatize(pp_text)
            pp_desc_q.append(pp_text)
            corpus_pp_desc_q += text+''

        for text in df['answers']:
            pp_text = Preprocessing.lower_text(text)
            # pp_text = Preprocessing.replace_quantity_values(pp_text)
            # pp_text = Preprocessing.replace_size_values(pp_text)
            # pp_text = Preprocessing.remove_numbers(pp_text)
            # pp_text = Preprocessing.remove_punctuation(pp_text)
            pp_text = Preprocessing.tokenize(pp_text)
            # pp_text = Preprocessing.remove_stopwords(pp_text)
            # pp_text = Preprocessing.lemmatize(pp_text)
            pp_desc_a.append(pp_text)
            corpus_pp_desc_a += text+''

        pp_df = df.copy(deep=True)
        pp_df['question'] = pp_desc_q
        pp_df['answers'] = pp_desc_a

        return pp_df, corpus_pp_desc_q, corpus_pp_desc_a


    def adapt_X_for_input_layer(df_train_text, df_val_text, df_test_text, max_sequence_length):
        tokenizer = keras.preprocessing.text.Tokenizer()
        tokenizer.fit_on_texts(df_train_text)
        vocab_size = len(tokenizer.word_index) + 1

        # train
        X_train_tokens = tokenizer.texts_to_sequences(df_train_text)
        X_train_padded = keras.preprocessing.sequence.pad_sequences(X_train_tokens, maxlen=max_sequence_length)

        # validation
        X_val_tokens = tokenizer.texts_to_sequences(df_val_text)
        X_val_padded = keras.preprocessing.sequence.pad_sequences(X_val_tokens, maxlen=max_sequence_length)

        # test
        X_test_tokens = tokenizer.texts_to_sequences(df_test_text)
        X_test_padded = keras.preprocessing.sequence.pad_sequences(X_test_tokens, maxlen=max_sequence_length)

        return vocab_size, X_train_padded, X_val_padded, X_test_padded


    def print_percentage(self, X, dataset):
        percentage = len(X[dataset])*100 / (len(X['test']) + len(X['train']) + len(X['val']))
        print(f'{dataset}: {round(percentage)}%')
        return


    def split_dataset(self, df, columns, label, seed):
        # Train-val-test split
        X = {}
        y = {}

        X['train'], X['test'], y['train'], y['test'] = train_test_split(df[columns], df[label], test_size=0.2, random_state=seed)
        X['train'], X['val'], y['train'], y['val'] = train_test_split(X['train'], y['train'], test_size=0.125, random_state=seed)
        
        self.print_percentage(X,'train')
        self.print_percentage(X,'val')
        self.print_percentage(X,'test')

        df_train = pd.DataFrame()
        df_train['question'] = X['train']
        df_train['answers'] = y['train']

        df_val = pd.DataFrame()
        df_val['question'] = X['val']
        df_val['answers'] = y['val']

        df_test = pd.DataFrame()
        df_test['question'] = X['test']
        df_test['answers'] = y['test']

        return df_train, df_val, df_test

    def get_sequences_details(col):
        sequence_length = 0
        max_sequence_length = 0

        for text_array in col:
            sequence_length += len(text_array)
            if max_sequence_length < len(text_array):
                max_sequence_length = len(text_array)
            
        mean_sequence_length = sequence_length/len(col)

        return mean_sequence_length, max_sequence_length
