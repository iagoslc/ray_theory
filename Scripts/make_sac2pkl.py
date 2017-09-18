# programa para criar os arquivos .pkl 
# Iago Costa

from os import listdir

files = listdir(".")

f = open('processing_files', 'w')

prefix_tables=[]

for lines in files:
	line_prefix=lines[:14]
	if line_prefix not in prefix_tables:
		prefix_tables.append(line_prefix)

teste = len(prefix_tables) 

c = 0

for var in prefix_tables:
	c=c+1
	print c
	print('ttpick.py -P %s*\n' % var)
	f.write('ttpick.py -P %s*\n' % var)

f.close()
