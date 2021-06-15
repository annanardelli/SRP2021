file = open("C:\\users\\gil\\downloads\\CS104ABETSyllabus.txt", 'r')
lines = file.readlines()
#print(lines)
words = []
for l in lines:
    l=l.replace("\n","")
    sp = l.split(" ")
    for w in sp:
        words.append(w)
        
print(words)
