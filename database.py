import os

path = 'KeyFramesC00_V00'
a = os.listdir(path)
a.sort()
a = [path+'/'+i for i in a]
for j in a:
    k = os.listdir(j)
    k.sort()
    k = [j+'/'+h for h in k]
filter = {'police':k[0:100],'man':k[90:150]}

print(list(set(filter['man'])&set(filter['police'])))