import glob
import json
import pandas as pd
import nltk
import wordcloud
import re


file_list = glob.glob("*.json")

print(file_list)


allFilesDict = {v:k for v, k in enumerate(file_list, 1)}
print(allFilesDict)

data = []

for k,v in allFilesDict.items():
    if 1 <= k <= 272:
        with open(v, 'r') as d:
            jdata = json.load(d)
            if jdata:
                data.append(jdata)


# Create a data frame 'dfnlp' from the JSON files and remove extraneous columns.
dfnlp = pd.DataFrame(data)
del dfnlp['back_matter']
del dfnlp['bib_entries']
del dfnlp['ref_entries']
del dfnlp['metadata']
del dfnlp['paper_id']

# Convert 'body_text' and 'abstract' to type String
dfnlp['body_text'] = dfnlp['body_text'].astype(str)
dfnlp['abstract'] = dfnlp['abstract'].astype(str)

# Create a new column consisting of 'all_text' by concatenating 'body_text' and 'abstract'
dfnlp['all_text'] = dfnlp['body_text'] + dfnlp['abstract']

# Convert all_text to lower case
dfnlp['all_text'] = dfnlp['all_text'].str.lower()

# Remove all integers in 'all_text'
dfnlp['all_text'] = dfnlp['all_text'].str.replace('\d+', '')

# Remove all specified special characters and punctuation from 'all_text'
spec_chars = ["!",'"',"#","%","&","'",
              "*","+",",","-",".","/",":",";","<",
              "=",">","?","@","[","\\","]","^","_",
              "`","{","|","}","~","(",")",'′','•']
for char in spec_chars:
    dfnlp['all_text'] = dfnlp['all_text'].str.replace(char, '')

spec_words = ["section","spans","cite","refid","start","text",
              "bibref","none","were","four","three","seven","five",
              "used","using","also","figref","tabref","figure","table",
              "data","studies","study","control","however","results","different",
              "number","analysis","information","found","shown","activity","many","high",
              "cases","observed","could","well","first","system","although","sequence",
              "including","within","time","important","associated","days","test","samples",
              "among","development","assay","specific","group","role","based","several","compared",
              "model","addition","described","similar","type","showed","would","performed",".","thus",
              "small","large","case","years","present","therefore","following","known","early","level",
              "rate","less"]
for str in spec_words:
    dfnlp['all_text'] = dfnlp['all_text'].str.replace(str, '')

# Remove all words of length three characters or less.
dfnlp['all_text'] = dfnlp['all_text'].str.replace(r'\b(\w{1,3})\b', '')

pd.options.display.max_columns = None
print(dfnlp.head(10))

# Tokenize all words.
def nlp_tokenize(text):
    if not text:
        print('There is no text to tokenize')
        text = ''
    return nltk.word_tokenize(text)
dfnlp['tokenized_words'] = dfnlp['all_text'].apply(nlp_tokenize)
tokens = dfnlp['tokenized_words']

allWords = []
for wordList in tokens:
    allWords += wordList

# Remove All Stopwords
from nltk.corpus import stopwords
stop_words=set(stopwords.words("english"))
allWordsFinal=[]
for w in allWords:
    if w not in stop_words:
        allWordsFinal.append(w)


# Run frequency distribution of words and plot on a graph.
from nltk.probability import FreqDist
fdist = FreqDist(allWordsFinal)

import matplotlib.pyplot as plt
fdist.plot(80)
plt.show()
#last_75 = FreqDist(dict(fdist.most_common()[-480:]))
#last_75.plot()

# Create and generate a word cloud image of most frequent words.
from wordcloud import WordCloud
words=(" ").join(allWordsFinal)
wc = WordCloud(width=1600, height=800, background_color="white", max_words=200, contour_width=3).generate(words)
# Display the generated image
plt.figure(figsize = (10,10), facecolor = None)
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.savefig('wordcloud.png', facecolor='k', bbox_inches='tight')
print(fdist.most_common())
plt.show()