# programa para/criar a base de dados e arquivos .pkl 
# Iago Costa - 09/2017

from obspy.geodetics.base import kilometer2degrees
from obspy.geodetics.base import gps2dist_azimuth
from obspy.taup.taup import getTravelTimes
import sys, os
from os import listdir
from obspy import read

model = 'IASP91'
phase = 'P'
sufix = 'SAC'
database_file = 'database_file'

outfile='processing_files.sh'
if phase in 'P':
	phase_sufix='x'

if phase in ('PKIKP','PKiKP'):
	phase_sufix='kp'



files = listdir(".")

#criando a base de dados principal

f = open(database_file, 'w')
f.write('Counter	Date	Station_name	Stla	Stlo	Stel	Evla	Evlo	Evdp	Gcarc	Event_name	Azimute	BackAzimute	Take-off-Angle	Travel_Time\n')	

c=0

for line in files:
	if line.endswith(".SAC"):
		sac_temp = read(line)
		sac = sac_temp[0]
		#Parametros da estacao
		stla = sac.stats.sac.stla
		stlo = sac.stats.sac.stlo
	
		#verificacao de problemas no cabecalho da elevacao da estacao
		try:
			stel=sac.stats.sac.stel
		except:
			stel=sac.stats.sac.stdp
		az = sac.stats.sac.az
		baz = sac.stats.sac.baz
			#nome da estacao
		kstnm = sac.stats.sac.kstnm
		#Parametros do evento
		evla = sac.stats.sac.evla
		evlo = sac.stats.sac.evlo
		evdp = sac.stats.sac.evdp
		nzyear = sac.stats.sac.nzyear
		nzjday = sac.stats.sac.nzjday
		nzhour = sac.stats.sac.nzhour
		nzmin = sac.stats.sac.nzmin
		#making strings
		nzyear_str = str(nzyear)
		nzjday_str = str(nzjday)
		nzhour_str = str(nzhour)
		nzmin_str = str(nzmin)
		
		
		
		#devido a problemas na distancia dos dados, calculamos se este parece errado
		gcarc = sac.stats.sac.gcarc
		if gcarc >= 180 or gcarc <= 10:
			distance_m = gps2dist_azimuth(stla,stlo,evla,evlo)
			distance_km = (distance_m[0])/1000
			gcarc = kilometer2degrees(distance_km)
		else:
			pass
		
		
	
		kevnm = sac.stats.sac.kevnm
		
		#formato de data recebido pelo programa de inversao
		date_format=nzyear_str[-2:]+nzjday_str.zfill(3)+nzhour_str.zfill(2)+nzmin_str.zfill(2)+phase_sufix
				
		
		#calculando o t0 e o take-off angle (toa)
		try:
			tt = getTravelTimes(delta=gcarc, depth=evdp, model=model)
			taup_time = tt[0].get("time")
			toa = tt[0].get("take-off angle")
		except:
			pass
		#if phase == 'PKIKP' or 'PKP':
		#	taup_time = tt[5].get("time")
		#	toa = tt[5].get("take-off angle")
	
		c=c+1
		print ('%i processando o evento %s') % (c,line)
		try:
			f.write('%i	%s	%s	%3.4f	%3.4f	%3.4f	%3.4f	%3.4f	%3.4f	%3.4f	%s	%3.4f	%3.4f	%3.4f	%4.4f\n' % (c,date_format,kstnm,stla,stlo,stel,evla,evlo,evdp,gcarc,kevnm,az,baz,toa,taup_time))
		except:
			pass
f.close()
	
	
#------------------------------------	
	
# transformando os arquivos sac em pkl e formatando a taxa de amostragem para 0.025
	
	

#normalizacao dos dados para auxilio na analise do MCCC considerando que nao serao feitas
#correcoes de amplitude




for lines in files:
	if lines.endswith(".SAC"):
		st=read(lines)
		tr = st[0]
		tr_norm=tr.normalize()
		tr_norm.write(filename='n'+lines,format="SAC")

prefix_tables=[]

files_n = listdir(".")

for lines in files_n:
	if lines.startswith("n"):
		line_prefix=lines[:15]
		if line_prefix not in prefix_tables:
			prefix_tables.append(line_prefix)


f = open(outfile, 'w')

c = 0

for var in prefix_tables:
	c=c+1
	print c
	print('%i processando %s* \n' % (c,var))
	f.write('sac2pkl.py -s %s* -o %s.pkl -d 0.025\n' % (var,var))


f.close()

os.system(outfile)

#removendo arquivos temporarios
#os.remove(outfile)


for lines in files_n:
	if lines.startswith("n"):
		os.remove(lines)


