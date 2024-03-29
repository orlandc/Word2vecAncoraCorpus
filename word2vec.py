import os
import sys
import nltk
import multiprocessing
from gensim.models import Word2Vec

#nltk.download('punkt')

path = os.getcwd() + '/raw'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))

sentences = []
diccionario = dict()

for i, f in enumerate(files):
    archivo = open(f, "r")
    fl = archivo.readlines()
    for x in fl:
        tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
        tokens = nltk.word_tokenize(x.decode("utf-8"))
        sentences.append(tokens)
        for word in tokens:
            if word not in diccionario:
                diccionario[word] = 1
            else:
                diccionario[word] += 1

print ("numero de oraciones presentes en el corpus " + str(len(sentences)))
print ("numero de palabras únicas " + str(len(diccionario)))


num_features = 100                        #Dimensionality of the resulting word vectors
min_word_count = 1                        #Minimum word count threshold
num_workers = multiprocessing.cpu_count() #Number of threads to run in parallel
context_size = 5                          #Context window length
seed = 1                                  #Seed for the RNG, to make the result reproducible

word2vec_model = Word2Vec(
    sentences=sentences,
    sg=1,
    seed=seed,
    workers=num_workers, 
    size=num_features, 
    min_count=min_word_count, 
    window=context_size)

word2vec_model.wv.save_word2vec_format('model/word2vec_model_ancora.txt', binary=False)