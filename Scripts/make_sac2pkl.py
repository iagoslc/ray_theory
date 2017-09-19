# programa para criar os arquivos .pkl 
# Iago Costa

import sys, os
from os import listdir
from obspy import read

files = listdir(".")
outfile='processing_files.sh'



#normalizacao dos dados para auxilio na análise do MCPCC considerando que nao serao feitas
#correcoes de amplitude

for lines in listdir("."):
		st=read(lines)
		tr = st[0]
		tr_norm=tr.normalize()
		tr_norm.write(filename=lines+'n',format="SAC")

prefix_tables=[]



for lines in files:
	line_prefix=lines[:14]
	if line_prefix not in prefix_tables:
		prefix_tables.append(line_prefix)

teste = len(prefix_tables) 

f = open(outfile, 'w')

c = 0

for var in prefix_tables:
	c=c+1
	print c
	print('processando %s* \n' % (var))
	f.write('sac2pkl.py -s %s* -o %s.pkl -d 0.025\n' % (var,var))


f.close()

os.system(outfile)

os.remove(outfile)

