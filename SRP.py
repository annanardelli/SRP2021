#!/usr/bin/env python
# coding: utf-8

# In[23]:


import PyPDF2
import pickle

file = open("/Users/isabellachiaravalloti/Downloads/CS104ABETSyllabus.pdf","rb")
fileReader = PyPDF2.PdfFileReader(file)
#print(fileReader.numPages)
#print(fileReader.getDocumentInfo())
print()




numPages = fileReader.numPages
pageList = []

for page in range(0, numPages):
    pageObj = fileReader.getPage(page)
    text = pageObj.extractText()
    currentPage = text.split()
    pageList.append(currentPage)
    
#print(pageList)


file_name = "sample.txt"

open_file = open(file_name, "wb")
pickle.dump(pageList, open_file)
open_file.close()

open_file = open(file_name, "rb")
loaded_list = pickle.load(open_file)
open_file.close()

print(loaded_list)



# In[ ]:





# In[ ]:




