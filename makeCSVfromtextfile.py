#! /usr/bin/python

#for more information on creating and using dataframes in Pandas
# https://www.tutorialspoint.com/python_pandas/python_pandas_dataframe.htm

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
    new_row = {'LineNumber':i, 'Text':line.strip()}
    rows_list.append(new_row)
    i+=1

df = pd.DataFrame(rows_list,columns=['LineNumber','Text'])

csvname = str(sys.argv[1]).split('.')[0] + "_num-only.csv"
## This is actually silly - storing the DF as a CSV with index would accomplish basically the same thing
df.to_csv(csvname, encoding='utf-8', index=False)
print("The CSV %s has been written." % csvname)
