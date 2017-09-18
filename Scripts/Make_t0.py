# programa para inserir o tempo de chegada "a" na variável t0
# Iago Costa

from obspy import read
from os import listdir

files = listdir(".")

for lines in files:
	st = read(lines)
	t0 = st[0].stats.sac.a
	st[0].stats.sac.t0 = t0
	output_sac=lines[:-1]
	st.write(output_sac, format='SAC')
	print ("processando %s " % output_sac)
	
