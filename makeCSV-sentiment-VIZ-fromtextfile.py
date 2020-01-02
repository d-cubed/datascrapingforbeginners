#! /usr/bin/python

#for more information on creating and using dataframes in Pandas
# https://www.tutorialspoint.com/python_pandas/python_pandas_dataframe.htm
# https://medium.com/dunder-data/selecting-subsets-of-data-in-pandas-6fcd0170be9c

from textblob import TextBlob
import pandas as pd
import io
import matplotlib.pyplot as plt
import sys
import re

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

#cf https://stackoverflow.com/questions/10715965/add-one-row-to-pandas-dataframe
#a list of dictionaries
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

df = pd.DataFrame(rows_list,columns=['line','text','polarity','subjectivity'])
#polarity and subjectivity don't need to be declared
#the following methods would create them as well
df['polarity'] = df['text'].apply(get_polarity)
df['subjectivity'] = df['text'].apply(get_subjectivity)
#cumulative sum for a behavioral look at the textdump
#https://pandas.pydata.org/pandas-docs/version/0.19.2/generated/pandas.DataFrame.cumsum.html
df['polsum']= df['polarity'].cumsum()
"""
for index, row in df.iterrows():
    #print(df['polarity'])
    print(row[4])
"""

#subset the df
df2 = df[['line', 'polsum']]

#general plot title from file name
#plottitle = str(sys.argv[1]).split('.')[0] + "\n Cumulative Polarity"

#vv kludge for stealing the network to print chapter number
chnum = re.findall(r'\d+', str(sys.argv[1]))
if (len(chnum) > 0):
    plottitle = "Cumulative Polarity \nStealing the Network: Chapter " + str(chnum[0])
    print(chnum)
else:
    plottitle = "Cumulative Polarity \nStealing the Network: Chapter " + str(sys.argv[1])
    print("This has no chapter number")

pplot = df2.plot(x='line', y='polsum',linestyle='-', markevery=100, marker='o', markerfacecolor='black', title=plottitle)
pplot.set(xlabel="Line Number", ylabel="Polarity")
pplot.set_facecolor("grey")
pplot.legend(["Polarity Sum"]);
#v to actually show the plot
#plt.show()

pngname = str(sys.argv[1]).split('.')[0] + "_polsum.png"
#v to actually save the plot
plt.savefig(pngname)
print("The png %s has been written." % pngname)
