from keras.models import Sequential
from keras.layers import Dense, Embedding, GRU, LSTM, Activation, Flatten 


from keras.callbacks import LambdaCallback 
from keras.optimizers import RMSprop 
from keras.callbacks import ReduceLROnPlateau 
import random
import sys 


from keras import utils
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

from keras.callbacks import ModelCheckpoint

import numpy as np
import matplotlib.pyplot as plt

def get_sonnets(file):
    sonnet = '';
    sonnets = []
    lines = []

    file_sonnet = open('sonnets.txt','r')

    for line in file_sonnet: 
        lines.append(line)

    i=0;
    while i!=len(lines):
        sonnet = sonnet + lines[i]
        i+=1;
        if i%14==0:
            sonnets.append(sonnet)
            sonnet = ''
    return sonnets

with open('sonnets.txt', 'r') as file:
    text = file.read() 
print('text [10] =  ', text[10])

num_words = 10000

sonnets = get_sonnets('sonnets.txt')
right_sonnets = get_sonnets('sonnets2.txt')

tokenizer = Tokenizer(num_words=num_words)
tokenizer.fit_on_texts(sonnets)
tokenizer.word_index

sequences = tokenizer.texts_to_sequences(sonnets)
sequences_r = tokenizer.texts_to_sequences(right_sonnets)

sequences = pad_sequences(sequences, 100)
sequences_r = pad_sequences(sequences_r, 100)

x_train = pad_sequences(sequences, 100)
y_train = pad_sequences(sequences_r, 100)

x_train = x_train.reshape(x_train.shape[0], x_train.shape[1],1)
y_train = y_train.reshape(y_train.shape[0], y_train.shape[1],1)

char_to_indices = dict((c, i) for i, c in enumerate(tokenizer.word_index))

indices_to_char = dict((i, c) for i, c in enumerate(tokenizer.word_index)) 

print (x_train.shape[0])
print (x_train.shape[1])

X = np.zeros((x_train.shape[0]+1, x_train.shape[1]+1, len(tokenizer.word_index)+1), dtype = np.bool) 
y = np.zeros((y_train.shape[0]+1, len(tokenizer.word_index)+1), dtype = np.bool) 

for i, sonnet in enumerate(sequences): 
    for t, word in enumerate(sonnet):
        X[i, t, word] = 1        
    y[i, sequences_r[i]] = 1

model = Sequential()

model.add(LSTM(128, input_shape =(101, len(tokenizer.word_index)+1)))

model.add(Dense(len(tokenizer.word_index)+1))

model.add(Activation('softmax'))

optimizer = RMSprop(lr = 0.01)

model.compile(loss ='categorical_crossentropy', optimizer = optimizer) 

model.fit(X, y, batch_size = 128, epochs = 500, callbacks = callbacks) 

model.predict(sonnets[1][1])

