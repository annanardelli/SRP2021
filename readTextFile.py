file = open("C:\\users\\gil\\downloads\\CS104ABETSyllabus.txt", 'r')
lines = file.readlines()
list_word = []
for l in lines:
    l = l.replace("\n","")
    list_word.append(l.split(" "))
print(list_word)    
