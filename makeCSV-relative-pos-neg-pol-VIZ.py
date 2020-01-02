#! /usr/bin/python

from textblob import TextBlob
import pandas as pd
import io
import matplotlib.pyplot as plt
import sys
import re
#import numpy as np


print ("You are currently running %s" % (sys.argv[0]))

if len(sys.argv) < 2:
    print("You should supply the name of a textfile that should be converted to a CSV")
    sys.exit()
else:
    text = open(sys.argv[1],"r")

txt = text.read()
print("Reading in %s " % str(sys.argv[1]))
#remove new lines
txt = txt.replace('\n', ' ').replace('\r', ' ')
#replace periods with newlines, convert to file object, read in lines
txt = txt.replace('. ','\n')
txt = unicode(txt,'utf-8')
f = io.StringIO(txt)
numbered = f.readlines()

rows_list = []
i=1
for line in numbered:
    new_row = {'line':i, 'text':line.strip()}
    rows_list.append(new_row)
    i+=1


def get_polarity(text):
    try:
        return TextBlob(text).sentiment.polarity
    except Exception:
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




df = pd.DataFrame(rows_list,columns=['line','text'])
#polarity and subjectivity don't need to be declared
#the following methods create them
df['polarity'] = df['text'].apply(get_polarity)
df['subjectivity'] = df['text'].apply(get_subjectivity)
#cumulative sum for a behavioral look at the textdump
#https://pandas.pydata.org/pandas-docs/version/0.19.2/generated/pandas.DataFrame.cumsum.html
df['polsum']= df['polarity'].cumsum()
df['pos'] = df['polarity'].apply(is_pos)
df['neg'] = df['polarity'].apply(is_neg)
df['possum']= df['pos'].cumsum()
df['negsum']= df['neg'].cumsum()

"""
#Useful for debugging
for index, row in df.iterrows():
    #print(df['polarity'])
    print(row[5])
"""

#subset the df
df2 = df[['line', 'polsum', 'possum','negsum']]

#general plot title from file name
#plottitle = str(sys.argv[1]).split('.')[0] + "\n Cumulative Polarity"

#vv kludge for stealing the network to print chapter number
chnum = re.findall(r'\d+', str(sys.argv[1]))
if (len(chnum) > 0):
    plottitle = "Statement Polarities \nStealing the Network: Chapter " + str(chnum[0])
    #print(chnum)
else:
    plottitle = "Statement Polarities \n " +  str(sys.argv[1])
    print("This has no chapter number")

#xkcd colors here: https://xkcd.com/color/rgb/
#nice description of making multiple graphs with matplotlib
#https://matplotlib.org/3.1.1/gallery/color/color_demo.html#sphx-glr-gallery-color-color-demo-py
#see also https://blog.graphiq.com/finding-the-right-color-palettes-for-data-visualizations-fcd4e707a283

fig, ax = plt.subplots(facecolor='grey')
ax.set_facecolor('#a6a6a6')
ax.set_title(plottitle, color='black')
ax.set_xlabel('Line Number', color='black')
ax.set_ylabel('Occurences', color='black')
ax.plot(df2['line'], df2['polsum'], '#808080', label='Overall Polarity')
ax.plot(df2['line'], df2['possum'], 'xkcd:darkgreen', label='Positive statements')
ax.plot(df2['line'], df2['negsum'], 'xkcd:crimson', linestyle='--',label='Negative statements')
ax.tick_params(labelcolor='grey')
plt.legend()


#plt.show()

pngname = str(sys.argv[1]).split('.')[0] + "_pos-neg.png"
#v to actually save the plot
plt.savefig(pngname)
print("The png %s has been written." % pngname)
