import numpy as np
import pyfits
import matplotlib.pyplot as plt
from datetime import datetime as dt
from itertools import combinations

FITSname="e17a10-1l.59.tasav2.fittp"
CLver = 10
hdulist = pyfits.open(FITSname)
hdulist.info()

year=int(hdulist[0].header['DATE-OBS'][0:4])
month=int(hdulist[0].header['DATE-OBS'][5:7])
date=int(hdulist[0].header['DATE-OBS'][8:10])

# Day of the year
DOY=dt(year,month,date).timetuple().tm_yday
#print DOY, year, month, date

# Get CL tables
cltab = hdulist[CLver]
cltab.columns
#

ANT=['A', 'X', 'Z', 'L', 'P', 'J', 'S', 'R']

# Generate baselines using antennas
AIPS_BS=[''.join(x) for x in list(combinations(ANT, 2))]

#print AIPS_BS

#
ANT1=1
ANT2=6
BS = ''.join([ANT[ANT1-1],ANT[ANT2-1]])

t1=cltab.data["TIME"][np.where(cltab.data["ANTENNA NO."]==ANT1)]
t2=cltab.data["TIME"][np.where(cltab.data["ANTENNA NO."]==ANT2)]
tt=np.intersect1d(t1,t2)

IF=0
ttime = []
delay_an1 = []
delay_an2 = []
key = "DELAY 1"
nsec = 1.e9
for time in tt:
	indices=np.where(cltab.data["TIME"]==time)[0]
	index1 = np.where(cltab.data["ANTENNA NO."][indices]==ANT1)[0]
	index2 = np.where(cltab.data["ANTENNA NO."][indices]==ANT2)[0]
	
	ttime.append(time)
	delay_an1.append(cltab.data[key][indices[index1][0],IF]*nsec)
	delay_an2.append(cltab.data[key][indices[index2][0],IF]*nsec)

f = open(FITSname[:-5]+BS+"."+key.replace(" ","")+".txt",'w')
f.write("#day\t\tdelay_an1\tdelay_an1\tdelay_bs\tbaseline\n")
f.write("#(day)\t\t(nsec)\t(nsec)\t(nsec)\tbaseline\n")
for i in range(len(ttime)):
	if(isnan(delay_an1[i])==False and isnan(delay_an2[i])==False):
		f.write("%0.6f\t%0.6f\t%0.6f\t%0.6f\t%s\n" 
			%(ttime[i]+DOY, delay_an1[i], delay_an2[i], delay_an1[i]-delay_an2[i], ''.join([ANT[ANT1-1],ANT[ANT2-1]])))
f.close()
#plt.plot(np.array(ttime),np.array(delay_an1), 'ro', ls='none', label="%s"%(BS))
#plt.plot(np.array(ttime),np.array(delay_an2), 'bo', ls='none', label="%s"%(BS))

#plotif = 0
#stations = list(set(cltab.data["ANTENNA NO."]))
#for station in stations:
#    t = np.where(cltab.data["ANTENNA NO."]==station)
#    plt.plot(cltab.data["TIME"][t], cltab.data["DELAY 1"][:,plotif][t]*1e9, ls="none", marker=".", label="ant%d"%(station))
#plt.xlabel("Relative Time (Day)")
#plt.ylabel("Delay (nsec)")
#plt.legend(frameon=True, ncol=4)
#plt.ylim(-10,10)
