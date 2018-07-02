'''
Created on Jul 2, 2018

@author: rachel
'''

import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from collections import Counter
import string
from _collections import defaultdict
import heapq

class Frequifier(object):
    '''
    summarize word frequencies in a text
    '''
    
    def __init__(self, min_cut=0.1, max_cut=0.9):
        self._min_cut = min_cut
        self._max_cut = max_cut
        # minimum list of words to be removed. may be extended
        self._stopwords = set(stopwords.words('english')
                              +list(string.punctuation)
                              + ["'s'", '"'])
        # stemm endings like "ing", "ly", ...
        self._stemmer = SnowballStemmer('english')
        # make words alike: dogs -> dog; are, is -> be
        self._lemmatizer = WordNetLemmatizer()
        

    def set_stop_words(self, custom_stop_words):
        if custom_stop_words is None:
            stopwords = set(self._stopwords)
        else:
            stopwords = set(custom_stop_words).union(self._stopwords)
        return stopwords

    def compute_frequencies_text(self, text, custom_stop_words=None):
        freq = Counter()
        stopwords = self.set_stop_words(custom_stop_words)
        for sentence in nltk.sent_tokenize(text.lower()):
            for word in nltk.word_tokenize(sentence):
                word = self._stemmer.stem(word)
                word = self._lemmatizer.lemmatize(word)
                word = self._lemmatizer.lemmatize(word, pos='v')
                if word not in self._stopwords:
                    freq[word] += 1
        m = max(freq.values())
        deletables = []
        for word, freqs in freq.items():
            freq_ratio = freqs/m
            if word in stopwords or freq_ratio>self._max_cut or freq_ratio<self._min_cut:
                deletables.append(word)
        for word in deletables:
            del freq[word]
        return freq
    
    def compute_frequencies_sentences(self, sentences, custom_stop_words=None):
        freq = Counter()
        stopwords = self.set_stop_words(custom_stop_words)
        for sentence in sentences:
            for word in nltk.word_tokenize(sentence):
                word = self._stemmer.stem(word)
                word = self._lemmatizer.lemmatize(word)
                word = self._lemmatizer.lemmatize(word, pos='v')
                if word not in self._stopwords:
                    freq[word] += 1
        m = max(freq.values())
        deletables = []
        for word, freqs in freq.items():
            freq_ratio = freqs/m
            if word in stopwords or freq_ratio>self._max_cut or freq_ratio<self._min_cut:
                deletables.append(word)
        for word in deletables:
            del freq[word]
        return freq
    
    def compute_frequencies_words(self, words, custom_stop_words=None):
        stopwords = self.set_stop_words(custom_stop_words)
        freq = Counter(words)
        deletables = []
        for word in freq.keys():
            if word in stopwords:
                deletables.append(word)
        for word in deletables:
            del freq[word]
        return freq
    
    def summarize(self, text, n):
        sentences = nltk.sent_tokenize(text.lower())
        assert n < len(sentences)
        freq = self.compute_frequencies_sentences(sentences)
        rank = defaultdict(int)
        for i, sentence in enumerate(sentences):
            for word in sentence:
                if word in freq:
                    rank[i] += freq[word] 
            rank[i] /= len(sentence)
        sents_idx = heapq.nlargest(n, rank, rank.get)
        return [sentences[i] for i in sents_idx]
            