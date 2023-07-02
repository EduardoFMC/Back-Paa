#type: ignore

import pandas as pd
import numpy as np
import random
from transformers import BertTokenizer, TFBertModel

import sys
sys.path.insert(0,"..")

SEED_VAL = 42
random.seed(SEED_VAL)
np.random.seed(SEED_VAL)


class Bert():
    def __init__(self, model_name):
        self.bert_tokenizer = BertTokenizer.from_pretrained(model_name)
        self.bert_model = TFBertModel.from_pretrained(model_name)


    def create_embeddings(self, train, val, test):
        # Create BERT tf tokens
        tf_tokens = {}
        tf_tokens['train'], tf_tokens['val'], tf_tokens['test'] = self.tokenize_data(train, val, test)
        
        # Create BERT embeddings
        bert_embeddings = {}
        bert_embeddings['train'], bert_embeddings['val'], bert_embeddings['test'] = self.apply_model(tf_tokens['train'], tf_tokens['val'], tf_tokens['test'])
        
        # Return BERT embeddings
        return bert_embeddings['train'], bert_embeddings['val'], bert_embeddings['test']


    def tokenize_data(self, train, val, test):
        # Apply on texts
        train_tf_tokens = [self.bert_tokenizer(''.join(text), return_tensors='tf') for text in train]
        val_tf_tokens   = [self.bert_tokenizer(''.join(text), return_tensors='tf') for text in val]
        test_tf_tokens  = [self.bert_tokenizer(''.join(text), return_tensors='tf') for text in test]
        
        # Return tensors
        return train_tf_tokens, val_tf_tokens, test_tf_tokens


    def apply_model(self, train, val, test):
        # Apply on tf tensors
        train_embeddings = [np.array(self.bert_model(tokens).last_hidden_state).reshape(-1) for tokens in train]
        val_embeddings   = [np.array(self.bert_model(tokens).last_hidden_state).reshape(-1) for tokens in val]
        test_embeddings  = [np.array(self.bert_model(tokens).last_hidden_state).reshape(-1) for tokens in test]
        
        # Return embeddings
        return train_embeddings, val_embeddings, test_embeddings
