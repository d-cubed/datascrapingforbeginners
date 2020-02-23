#!/usr/bin/python3

from textblob import TextBlob
import pandas as pd
import io
import matplotlib.pyplot as plt
import sys
import re
import json

print ("You are currently running %s" % (sys.argv[0]))

if len(sys.argv) < 2:
    print("You should supply the name of a textfile that should be converted to a CSV")
    sys.exit()
else:
    text = open(sys.argv[1],"r")

source = str(sys.argv[1])

#this make cleans emojis and whatnot from the comments
#if emojis were important we'd use a more UTF-8 friendly approach
def guder(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def get_polarity(text):
    try:
        return TextBlob(text).sentiment.polarity
    except Exception:more
    print("An exception occurred.")
    return 'n/a'

def get_subjectivity(text):
    try:
        return TextBlob(text).sentiment.subjectivity
    except Exception:
        print("An exception occurred.")
        return 'n/a'

def is_pos(pol):
    if (pol > 0):
        return 1
    else:
        return 0

def is_neg(pol):
    if (pol < 0):
        return 1
    else:
        return 0

filename=sys.argv[1]
with open(filename, encoding="utf8") as f:
    data = f.readlines()
    data = [json.loads(guder(line)) for line in data] #convert string to dict format

df = pd.DataFrame(data)
"""
#to see if the columns are listed
for key in df:
    print(key)
"""
df['source'] =  source
df['polarity'] = df['text'].apply(get_polarity)
df['subjectivity'] = df['text'].apply(get_subjectivity)
df['polsum'] = df['polarity'].cumsum()
df['pos'] = df['polarity'].apply(is_pos)
df['neg'] = df['polarity'].apply(is_neg)
df['possum'] = df['pos'].cumsum()
df['negsum'] = df['neg'].cumsum()

#for row in df:
    #print(str(df['author']).strip())
    #print(str(df['text']).strip())

csvname = str(sys.argv[1]).split('.')[0] + ".csv"
df.to_csv(csvname)


#to graph - uncomment below vvvvvv
plottitle = "Statement Polarities \n "+ str(sys.argv[1])
fig, ax = plt.subplots(facecolor='grey')
ax.set_facecolor('#a6a6a6')
ax.set_title(plottitle, color='black')
ax.set_xlabel('Time', color='black')
ax.set_ylabel('Occurences', color='black')
i=0
df['line']=df.index
for row in df:
    #df['line']=str(row.index)
    print(df['line'])
    #print(df['time'])
count_row = df.shape[0]  # gives number of row count
count_col = df.shape[1]  # gives number of col count
print("rows {}".format(count_row))
print("cols {}".format(count_col))

x = df['line']
ax.plot(x, df['polsum'], 'black', label='Overall Polarity')
ax.plot(x, df['possum'], 'xkcd:brown', label='Positive Statements')
ax.plot(x, df['negsum'], 'xkcd:red', linestyle='--', label='Negative Statements')
#ax.plot(x, df['polsum'], 'gray', label='Heros Overall Polarity')
#ax.plot(x, df['possum'], 'xkcd:purple', label='Heros Positive Statements')
#ax.plot(x, df['negsum'], 'xkcd:blue', linestyle='--', label='Heros Negative Statements')
ax.tick_params(labelcolor = 'grey')
plt.legend()

#vvv vvv
#plt.show()

pngname = str(sys.argv[1]).split('.')[0] + "_fromJSON.png"
#v to actually save the plot
plt.savefig(pngname)
print("The png %s has been written." % pngname)
