#! /usr/bin/python

#for more information on creating and using dataframes in Pandas
# https://www.tutorialspoint.com/python_pandas/python_pandas_dataframe.htm

from textblob import TextBlob
import pandas as pd
import io
import matplotlib.pyplot as plt
import sys

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

df = pd.DataFrame(rows_list,columns=['line','text','polarity','subjectivity'])
#df['textblob'] = df['text'].apply(TextBlob)

#the extra steps are added for transparency

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


df['polarity'] = df['text'].apply(get_polarity)
df['subjectivity'] = df['text'].apply(get_subjectivity)


"""
#iterating through DF in Pandas is not recommended
#this is for demonstration only
#https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
#https://planspace.org/20150607-textblob_sentiment/
#our options for sentiment are polarity and subjectivity
#this is left for testing purposes
for index, row in df.iterrows():
    #print(df['polarity'])
    print(row[2])
"""

csvname = str(sys.argv[1]).split('.')[0] + "_pol_sub.csv"
df.to_csv(csvname, encoding='utf-8', index=False)
print("The CSV %s has been written." % csvname)
