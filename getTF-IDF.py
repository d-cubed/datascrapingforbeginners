#! /usr/bin/python3
# for more examples of textblobs see:
# https://stevenloria.com/tf-idf/
#https://www.freecodecamp.org/news/how-to-process-textual-data-using-tf-idf-in-python-cd2bbc0a94a3/

import matplotlib.pyplot as plt
import math
from textblob import TextBlob
import sys

print ("You are currently running %s" % (sys.argv[0]))

if len(sys.argv) < 2:
    print("You should supply the name of a textfile or files to extract the text from!")
    sys.exit()
else:
    texts = []
    for i in range (1,len(sys.argv)):
        print("Reading in %s " % str(sys.argv[i]))
        texts.append(open(sys.argv[i],"r").read())




##tb1 = TextBlob(texts[0].read())


#methods from stevenloria.com/tf-idf/
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

bloblist = []
for t in texts:
    bloblist.append(TextBlob(t))


for i, blob in enumerate(bloblist):
    print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for word, score in sorted_words[:10]:
        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))


pngname = str(sys.argv[1]).split('.')[0] + "-blackhat.png"
