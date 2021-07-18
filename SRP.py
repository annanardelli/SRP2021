#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pickle
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
import requests
import re
import string

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def wordFrequency(syl, cc, string, count):
    data = []
    syllabus = []
    catalog = []
    for word in cc:
        if word in syl:
            data.append(word)
    for word in syl:
        if word in data:
            syllabus.append(word)     
    for word in cc:
        if word in data:
            catalog.append(word)
    seriesSyl = pd.Series(syllabus)
    seriesCC = pd.Series(catalog)
    syllabusCount = seriesSyl.value_counts().sort_index()
    catalogCount = seriesCC.value_counts().sort_index()
    #print(syllabusCount)
    #print(catalogCount)
    
    maximum = 0
    max1 = max(syllabusCount)
    max2 = max(catalogCount)
    if max1 > max2:
        maximum = max1
    else:
        maximum = max2
        
    fileName = " "
    if string == "outcomes":
        legendLabel = "Outcomes"
        title = courses[count] + " Syllabus vs. Outcomes"
        wordSimilarity(syllabusCount, catalogCount, "outcomes")
        fileName = courses[count] + 'Outcomes.png'
    else:
        legendLabel = "Course Catalog"
        title = courses[count] + " Syllabus vs. Course Catalog"
        wordSimilarity(syllabusCount, catalogCount, "cc")
        fileName = courses[count] + 'CC.png'
    
    
    plt.figure(figsize=(12,8))
    plt.plot(syllabusCount, label = "Syllabus", color = colors[0])
    plt.plot(catalogCount, label = legendLabel, color = colors[1])
    plt.xticks(rotation=90)
    plt.xlabel("Words")
    plt.yticks(np.arange(1, maximum+1, 1))
    plt.ylabel("Frequency")
    plt.legend(loc="upper left")
    plt.title(title)
    plt.savefig(fileName)
    plt.show()
    

    
wordSimCC = []
wordSimOut = []
def wordSimilarity(syl, cc, string):
    #WORD SIMILARITY = (CC WORD COUNT / CC TOTAL WORD COUNT) * (LESSER OF SYL WORD COUNT AND CC WORD COUNT)\
    syl = syl.tolist()
    cc = cc.tolist()
    total = 0
    lesser = 0
    ccLength = 0
    count = 0
    for ccWord in cc:
        ccLength += ccWord
    for ccWord in cc:
        if syl[count] < ccWord:
            lesser = syl[count]
        else:
            lesser = ccWord
        count+=1
        wordSim = ((ccWord/(ccLength)) * (lesser))
        total = wordSim + total
    #print(total)
    if string == "outcomes":
        wordSimOut.append(total)
    else:
        wordSimCC.append(total)
    
def descSplit(desc):
    descText = " ".join(desc)
    tokens = word_tokenize(descText) 
    #convert to lower case
    tokens = [w.lower() for w in tokens]
    #remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    #remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    #filter out stop words
    stop_words = set(stopwords.words('english'))
    new_stopwords = ['ł']
    new_stopwords_list = stop_words.union(new_stopwords)
    words = [w for w in words if not w in new_stopwords_list]
    return words
    


def desc(cc, start):
    desc = []
    desc.append(cc[start])
    desc.append(cc[start + 1])
    start += 2
    while not cc[start].startswith("CS-"):
        desc.append(cc[start])
        start += 1
    desc = descSplit(desc)
    return desc



courses = ['CS-102', 'CS-104', 'CS-175', 'CS-175L', 'CS-176', 'CS-176L', 'CS-205', 'CS-205L', 'CS-286', 'CS-305', 'CS-310', 'CS-325', 'CS-414', 'CS-418', 'CS-432', 'CS-450', 'CS-490', 'CS-492A']
urlList = [l.replace('-','') for l in courses]

colors = ["#4285f4", "#ea4335"]

#SYLLABUS
sylList = []
for u in urlList:
    sylURL = "https://raw.githubusercontent.com/annanardelli/SRP2021/main/CS%20ABET/" + u + ".txt"
    sylPage = requests.get(sylURL)
    sylData = sylPage.text

    if "\n" in sylData:
        sylData = sylData.replace("\r", "")
    else:
        sylData = sylData.replace("\r", "\n")

    tokens = word_tokenize(sylData) 
    #convert to lower case
    tokens = [w.lower() for w in tokens]
    #remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    #remove remaining tokens that are not alphabetic
    words = [word for word in stripped if word.isalpha()]
    #filter out stop words
    stop_words = set(stopwords.words('english'))
    new_stopwords = ['ł']
    new_stopwords_list = stop_words.union(new_stopwords)
    words = [w for w in words if not w in new_stopwords_list]
    sylList.append(words)
    
    file_name = u + "Syllabus.txt"
    open_file = open(file_name, "wb")
    pickle.dump(words, open_file)
    open_file.close()
    open_file = open(file_name, "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()
    
    
#COURSE CATALOG
cataURL = "https://raw.githubusercontent.com/annanardelli/SRP2021/main/UndergraduateCourseCatalog.txt"
cataPage = requests.get(cataURL)
cataData = cataPage.text
cataData = cataData.splitlines()

descList = []
course = 0
for index, item in enumerate(cataData):
    #print(index, item)
    if item.startswith(courses[course]):
        if ("Credits: " in cataData[index + 1]) or ("Credits: " in cataData[index]):
            descList.append(desc(cataData, index)) 
        if course < (len(courses) - 2):
            course += 1

count = -1
courseLength = len(courses)
for i in range(courseLength):
    count += 1
    wordFrequency(sylList[i],descList[i],"cc",count)


#OUTCOMES   
outcomesURL = "https://raw.githubusercontent.com/annanardelli/SRP2021/main/CSSEOutcomesText/CSOutcomesForSRP.txt"
outcomesPage = requests.get(outcomesURL)
outcomesData = outcomesPage.text
outcomesList = []
tokens = word_tokenize(outcomesData) 
#convert to lower case
tokens = [w.lower() for w in tokens]
#remove punctuation from each word
table = str.maketrans('', '', string.punctuation)
stripped = [w.translate(table) for w in tokens]
#remove remaining tokens that are not alphabetic
words = [word for word in stripped if word.isalpha()]
#filter out stop words
stop_words = set(stopwords.words('english'))
new_stopwords = ['ł']
new_stopwords_list = stop_words.union(new_stopwords)
words = [w for w in words if not w in new_stopwords_list]
outcomesList.append(words)      
count = -1
for i in range(courseLength):
    count += 1
    wordFrequency(sylList[i],outcomesList[0], "outcomes", count) 



plt.figure(figsize=(20,8)) 
x_axis = np.arange(len(courses))
  
plt.bar(x_axis - 0.2, wordSimCC, 0.35, label = 'Syllabus vs. CC', align = 'center', color = colors[0])
plt.bar(x_axis + 0.2, wordSimOut, 0.35, label = 'Syllabus vs. Outcomes', align = 'center', color = colors[1])
  
plt.xticks(x_axis, courses)
plt.xticks(rotation=90)
plt.xlabel("Courses")
plt.ylabel("Word Similarity Measure")
plt.title("Word Similarity for Each Course")
plt.legend()
plt.savefig('WordSimilarity.png')
plt.show()


#average 
wordSimAverages = []
count = 0
for i in wordSimCC:
    avg = 0
    total = 0
    total += i
    total += wordSimOut[count]
    count += 1
    avg = total / 2
    wordSimAverages.append(avg)

df = pd.DataFrame(wordSimAverages, index=courses, columns= ['Average'])
df = df.sort_values(by=['Average'],ascending=False)
#print(df)
x = df.plot.barh(rot=0, figsize=(12,8), title = "Average Word Similarity for Each Course", xticks = df['Average'], width = 0.7, color = colors)
x.set_ylabel("Course")
x.set_xlabel("Average Word Similarity Measure")
maxVal = max(df['Average']+0.1)
x.xaxis.set_ticks(np.arange(0, maxVal, 0.2))
x.get_legend().remove()
fig = x.get_figure()
fig.savefig('AverageWordSimilarity.png')


# In[ ]:





# In[ ]:





# In[ ]:




