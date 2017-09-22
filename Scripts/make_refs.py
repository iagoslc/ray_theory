# programa para criar os dados refs
# Iago Costa - 09/2017
import datetime
import sys
from os import listdir
import linecache
import math

phase = 'P'

f_tcale = open('ref.tcale', 'w')

f_tcals = open('ref.tcals', 'w')

f_teqs = open('ref.teqs', 'w')

f_trays = open('ref.trays', 'w')

f_tsta = open('ref.tsta', 'w')



ref_tsta = 'ref.tsta'

if phase in 'P':
	phase_sufix='x'

if phase in ('PKIKP','PKiKP'):
	phase_sufix='kp'

try:
	database_file=open('database_file','r')
	database=database_file.readlines()
	database_file.close()
except:
	sys.exit('database_file not found')

all_files = listdir(".")

for files in all_files:
	if files.endswith(".mcp"):
		mcp_file = open(files,'r')
		r = mcp_file.readlines()
		mcp_file.close()
		
		#pegando as informacoes do evento a partir do arquivo .mcp
		last_line_all = linecache.getline(files,len(r))
		last_line = last_line_all.split()
		catalog_mcp = last_line[0]
		year_mcp = int(last_line[1])
		month_mcp = int(last_line[2])
		day_mcp = int(last_line[3])
		hour_mcp = int(last_line[4])
		min_mcp = int(last_line[5])
		sec_mcp = last_line[6].split(".")[0]
		# making jday
		date_mcp = datetime.datetime(year_mcp,month_mcp,day_mcp)
		tt = date_mcp.timetuple()
		julday_mcp = tt.tm_yday
		#definindo o nome do evento baseado no .mcp
		#definindo strings
		nzyear_str = last_line[1]
		nzjday_str = str(julday_mcp)
		nzhour_str = last_line[4]
		nzmin_str = last_line[5]
		
		date_format=nzyear_str[-2:]+nzjday_str.zfill(3)+nzhour_str.zfill(2)+nzmin_str.zfill(2)+phase_sufix
		
		
		
		max_lines = len(r)-7
		min_lines = 2
		list_stations = []
		for i in range(2,max_lines):
			list_stations.append(r[i])
		number_stations = len(list_stations)
		
		print 'o evento %s possui %i estacoes' % (files,number_stations)
		#Pegando os dados dos residuos a partir dos arquivos mcp
		for station in list_stations:
			x = station.split()
			x_station_full = x[0]
			network = x_station_full.split(".")[0]
			station = x_station_full.split(".")[1]
			mccc_delay = x[1]
			std = x[2]
			cc_coeff = x[3]
			cc_std = x[4]
			pol = x[5]
			name_sacfile = x[6]
			t0_time = x[7]
			delay_time = x[8]
			#calculando o tobs
			t3_time = float(t0_time) + float(delay_time)
			print station
			
			
			# comparar os dados com a database			
			for database_line in database:
				if date_format in database_line and station in database_line:
					y = database_line.split('\t')
					#dados da database
					counter = y[0]
					date_database = y[1]
					kstnm = y[2]
					stla = y[3]
					stlo = y[4]
					stel = y[5]
					evla = y[6]
					evlo = y[7]
					evdp = y[8]
					gcarc = y[9]
					kevnm = y[10]
					az = y[11]
					baz = y[12]
					toa = y[13]
					taup_time = y[14]
					date_pdelin = nzyear_str+str(month_mcp).zfill(2)+str(day_mcp).zfill(2)+str(hour_mcp).zfill(2)+str(min_mcp).zfill(2)+str(sec_mcp).zfill(2)+'0'
					
					#formatando latitude e longitude para o ref.teqs
					evla_g1 = str(abs(float(evla))).split(".")[0]
					evla_g2 = evla_g2 = evla.split(".")[1][:3]
					
					evlo_g1 = str(abs(float(evlo))).split(".")[0]
					evlo_g2 = evla_g2 = evlo.split(".")[1][:3]
					
					if evla < 0:
						evla_n = 'S'
					if evla >= 0:
						evla_n = 'N'
						
					if evlo < 0:
						evlo_n = 'W'
					if evlo >= 0:
						evlo_n = 'E'
					
					#calculando a covariancia para o ref.trays
					
					covar = float(cc_std)*float(cc_std)
					if math.isnan(covar) is True:
						covar = 0.0
											
					#transformando take-off angle e backazimute de graus para radianos
					toa_rad = math.radians(float(toa))
					baz_rad = math.radians(float(baz))
					#criando o 'ref.tcale'
					f_tcale.write('%s.000000\n' % '{:18}'.format(date_database))
					#criando o 'ref.tcals'
					f_tcals.write('%s.00000\n' % '{:7}'.format(kstnm))
					#criando o 'ref.teqs'
					f_teqs.write('%s HDS %s%s%s%s%s%s%s     1000 MB\n'% ('{:11}'.format(date_database),'{:15}'.format(date_pdelin),'{:>2}'.format(evla_g1),'{:>3}'.format(evla_g2),evla_n,'{:>3}'.format(evlo_g1),'{:>3}'.format(evlo_g2),evlo_n))
					#criando o 'ref.trays'
					f_trays.write('%s %s %s ***.****  .%s .%s  .%s%s.%s%s  .00000 %s\n' % ('{:>5}'.format(counter),'{:11}'.format(date_database),'{:4}'.format(kstnm),str(format(float(covar), '.5f')).split(".")[1],str(format(float(cc_coeff), '.5f')).split(".")[1],str(format(float(toa_rad), '.6f')).split(".")[1],str(format(float(baz_rad), '.1f')).split(".")[0],str(format(float(baz_rad), '.6f')).split(".")[1],'{:>9}'.format(t3_time),phase))
					#criando o 'ref.tsta'
					f_tsta.write('%s%s %s%s%s%s%s' % (kstnm,'{:>4}'.format(stla.split(".")[0]),str(format(float(stla), '.5f')).split(".")[1],'{:>4}'.format(stlo.split(".")[0]),str(format(float(stlo), '.5f')).split(".")[1],'{:>2}'.format(str(float(stel)/1000).split(".")[0]),'{:>2}'.format(str(float(stel)/1000).split(".")[1])))
					
					
					break
f_tcale.close()
f_tcals.close()
f_teqs.close()
f_trays.close()
f_tsta.close()					

					
					
					
					
					
					
					
					
					
					
					
					
				
			

