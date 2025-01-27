import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()


def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def stem(alpha):
    return stemmer.stem(alpha.lower())


def bag_of_words(tokenized_sentence, words):
   
   
    sentence_words = [stem(alpha) for alpha in tokenized_sentence]
   
    bag = np.zeros(len(words), dtype=np.float32)
    for ffx, f in enumerate(words):
        if f in sentence_words: 
            bag[ffx] = 1

    return bag
