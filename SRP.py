#!/usr/bin/env python
# coding: utf-8

# In[45]:


import PyPDF2
import pickle

from nltk.tokenize import word_tokenize

import nltk
from nltk.corpus import stopwords


file = open("/Users/isabellachiaravalloti/Downloads/CS104ABETSyllabus.pdf","rb")
fileReader = PyPDF2.PdfFileReader(file)
#print(fileReader.numPages)
#print(fileReader.getDocumentInfo())

#url = "https://drive.google.com/file/d/1XWOX5YjK2PZo5LjiphYVJEQyBC5BIERj/view?usp=sharing"


numPages = fileReader.numPages
pageList = []


for page in range(0, numPages):
    pageObj = fileReader.getPage(page)
    text = pageObj.extractText()
    tokens = word_tokenize(text)
    # convert to lower case
    tokens = [w.lower() for w in tokens]
    # remove punctuation from each word
    import string
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    new_stopwords = ['ł']
    new_stopwords_list = stop_words.union(new_stopwords)
    words = [w for w in words if not w in new_stopwords_list]
    pageList.append(words)

    
print(pageList)

    
file_name = "sample.txt"

open_file = open(file_name, "wb")
pickle.dump(pageList, open_file)
open_file.close()

open_file = open(file_name, "rb")
loaded_list = pickle.load(open_file)
open_file.close()

#print(loaded_list)


#pip install wordcloud
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Define a function to plot word cloud
def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud) 
    # No axis details
    plt.axis("off");
# Import package
from wordcloud import WordCloud, STOPWORDS
# Generate word cloud
wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords = STOPWORDS).generate(text)
# Plot
plot_cloud(wordcloud)




# In[ ]:





# In[ ]:




