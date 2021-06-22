#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pickle
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
import requests
import re
import string


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
"""

courseList = ['CS-102', 'CS-104', 'CS-175', 'CS-175L', 'CS-176', 'CS-176L', 'CS-205', 'CS-205L', 'CS-286', 'CS-305', 'CS-310', 'CS-325', 'CS-414', 'CS-418', 'CS-432', 'CS-450', 'CS-490', 'CS-492A', 'CS-492B']
urlList = [l.replace('-','') for l in courseList]


"""

#SYLLABUS
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
    print()
    print(u)
    print(words)
    
    file_name = u + "Syllabus.txt"

    open_file = open(file_name, "wb")
    pickle.dump(words, open_file)
    open_file.close()

    open_file = open(file_name, "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()

    #print(loaded_list)

"""


def desc(cc, start):
    desc = []
    desc.append(cc[start])
    desc.append(cc[start + 1])
    start += 2
    while not cc[start].startswith("CS-"):
        desc.append(cc[start])
        start += 1
    print(desc)
    print()   
    
    
#COURSE CATALOG
print()
cataURL = "https://raw.githubusercontent.com/annanardelli/SRP2021/main/UndergraduateCourseCatalog.txt"
cataPage = requests.get(cataURL)
cataData = cataPage.text
cataData = cataData.splitlines()


course = 0
for index, item in enumerate(cataData):
    #print(index, item)
    if item.startswith(courseList[course]):
        if "Credits: " in cataData[index + 1]:
            desc(cataData, index) 
        course += 1

           





"""
    
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
wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='white', colormap='Accent', collocations=False, stopwords = STOPWORDS).generate(syllabusData)
# Plot
plot_cloud(wordcloud)

"""


# In[ ]:





# In[ ]:





# In[ ]:




