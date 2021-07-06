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
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer


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
        
    if string == "outcomes":
        legendLabel = "Outcomes"
        title = courses[count] + " Syllabus vs. Outcomes"
    else:
        legendLabel = "Course Catalog"
        title = courses[count] + " Syllabus vs. Course Catalog"
    
    """
    plt.figure(figsize=(12,8))
    plt.plot(syllabusCount, label = "Syllabus")
    plt.plot(catalogCount, label = legendLabel)
    plt.xticks(rotation=90)
    plt.xlabel("Words")
    plt.yticks(np.arange(1, maximum+1, 1))
    plt.ylabel("Frequency")
    plt.legend(loc="upper left")
    plt.title(title)
    plt.show()
    """
    


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
    sylList.append(words)
    
    file_name = u + "Syllabus.txt"
    open_file = open(file_name, "wb")
    pickle.dump(words, open_file)
    open_file.close()
    open_file = open(file_name, "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()
    
    dictionary = gensim.corpora.Dictionary([words])
    corpus = [dictionary.doc2bow([word]) for word in words]
    #print(corpus)
    tf_idf = gensim.models.TfidfModel(corpus)
    #for doc in tf_idf[corpus]:
        #print([[dictionary[id], np.around(freq, decimals=2)] for id, freq in doc])
    sims = gensim.similarities.Similarity("SRP", tf_idf[corpus],num_features=len(dictionary))
    
    
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
    
count = 0
for desc in descList:
    desc_doc_bow = dictionary.doc2bow(desc)
    query_doc_tf_idf = tf_idf[desc_doc_bow]
    print(count)
    count += 1
    #print(query_doc_tf_idf)
    sims[query_doc_tf_idf]
    
    avg_sims = []
    sum_of_sims =(np.sum(sims[query_doc_tf_idf], dtype=np.float32))
    avg = sum_of_sims / len(descSplit(desc))
    print(f'avg: {sum_of_sims / len(descSplit(desc))}')
    avg_sims.append(avg)
    total_avg = np.sum(avg_sims, dtype=np.float)
    percentage_of_similarity = round(float(total_avg) * 100)
    if percentage_of_similarity >= 100:
            percentage_of_similarity = 100
 
"""
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
"""
