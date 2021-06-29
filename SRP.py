#!/usr/bin/env python
# coding: utf-8

# In[164]:


import pickle
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
import requests
import re
import string

import matplotlib.pyplot as plt
from nltk import FreqDist
import pandas as pd
from collections import Counter
 


def wordFrequency(syl, cc):
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
    print(syllabusCount)
    print(catalogCount)
    #print(seriesSyl.value_counts().sort_index())
    #print(seriesCC.value_counts().sort_index())
    
    print()
    print()
    
    plt.figure(figsize=(12,8))
    plt.plot(syllabusCount)
    plt.plot(catalogCount)
    plt.xticks(rotation=90)

    #display plot
    plt.show()
    


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
    #print()
    #print(u)
    #print(words)
    sylList.append(words)
    
    
    file_name = u + "Syllabus.txt"

    open_file = open(file_name, "wb")
    pickle.dump(words, open_file)
    open_file.close()

    open_file = open(file_name, "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()

    #print(loaded_list)


#COURSE CATALOG
print()
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

        

courseLength = len(courses)
for i in range(courseLength):
    wordFrequency(sylList[i],descList[i])


    

    
    
    
    
    

        
"""
#CURRICULUM CHART
#gets list of courses from curriculum chart
ccURL = "https://raw.githubusercontent.com/annanardelli/SRP2021/main/CurriculumChart/b-s-in-computer-science-3.txt"
ccPage = requests.get(ccURL)
ccData = ccPage.text
#searches for courses in data
ccSubstr = re.compile('CS-\d{3}\w{0,1}')
courses = ccSubstr.findall(ccData)
#edits courses in list
courseList = []
for c in courses:
    if c not in courseList:
        courseList.append(c)
addCourses = ["CS-102", "CS-418", "CS-490"]
delCourses = ["CS-201", "CS-212", "CS-222", "CS-288", "CS-289", "CS-302", "CS-312", "CS-316", "CS-320", "CS-322", "CS-330", "CS-388", "CS-389", "CS-488", "CS-489", "CS-438"]
courseList.extend(addCourses)
courseList = [c for c in courseList if c not in delCourses]
courseList.sort()
print(courseList)
urlList = [l.replace('-','') for l in courseList]
#print(urlList)

#pip install wordcloud
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
wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='white', colormap='Accent', collocations=False, stopwords = STOPWORDS).generate(syllabusData)
# Plot
plot_cloud(wordcloud)


#freqDist = FreqDist(text)
#print(freqDist) 
#freqDist.plot(30)


#syllabus.sort()
    #catalog.sort()
    #d = pd.DataFrame(syllabus, columns = ['Syllabus'])
    
    #print(count)
    
    #series = d.squeeze()

"""


# In[ ]:





# In[ ]:





# In[ ]:




