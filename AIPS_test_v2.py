import numpy as np
import pyfits
import matplotlib.pyplot as plt
from datetime import datetime as dt
from itertools import combinations

def AIPS2HOPS_ANT(AIPS_ANT):
	HOPS_ANT = []
	for ant in AIPS_ANT:
		# ['AA', 'AP', 'AZ', 'LM', 'PV', 'JC', 'SM', 'SR']
		if(ant == 'AA'):
			HOPS_ANT.append('A')
		elif(ant == 'AP'):
			HOPS_ANT.append('X')
		elif(ant == 'AZ'):
			HOPS_ANT.append('Z')
		elif(ant == 'LM'):
			HOPS_ANT.append('L')
		elif(ant == 'PV'):
			HOPS_ANT.append('P')
		elif(ant == 'JC'):
			HOPS_ANT.append('J')
		elif(ant == 'SM'):
			HOPS_ANT.append('S')
		elif(ant == 'SR'):
			HOPS_ANT.append('R')
	return HOPS_ANT	

#------------------------------------------#
#	inputs
#------------------------------------------#
FITSname="e17a10-1l.59.tasav2.fittp"
CLver = 10
#ANT=['A', 'X', 'Z', 'L', 'P', 'J', 'S', 'R']
#------------------------------------------#
hdulist = pyfits.open(FITSname)
hdulist.info()

year=int(hdulist[0].header['DATE-OBS'][0:4])
month=int(hdulist[0].header['DATE-OBS'][5:7])
date=int(hdulist[0].header['DATE-OBS'][8:10])

# Day of the year
DOY=dt(year,month,date).timetuple().tm_yday

# Get CL tables
cltab = hdulist[CLver]
#cltab.columns
#

# List of antenna names
AIPS_ANT = hdulist['AIPS AN'].data['ANNAME']
HOPS_ANT = AIPS2HOPS_ANT(AIPS_ANT)

# Generate baselines using antennas
AIPS_BS=[''.join(x) for x in list(combinations(HOPS_ANT, 2))]

ANT=np.unique(cltab.data["ANTENNA NO."])
BLNoList=list(combinations(ANT,r=2))


# Now loop over all the baselines.

#AIPS antenna numbers: 1,2,3,4,...n
ANT1, ANT2 = BLNoList[0]
BS = ''.join([HOPS_ANT[ANT1-1],HOPS_ANT[ANT2-1]])


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

outname = FITSname[:-5]+key.replace(" ","")+"."+BS
f = open(outname,'w')
f.write("#day\t\tdelay_an1\tdelay_an1\tdelay_bs\tbaseline\n")
f.write("#(day)\t\t(nsec)\t(nsec)\t(nsec)\tbaseline\n")
for i in range(len(ttime)):
	if(isnan(delay_an1[i])==False and isnan(delay_an2[i])==False):
		f.write("%0.6f\t%0.6f\t%0.6f\t%0.6f\t%s\n" 
			%(ttime[i]+DOY, delay_an1[i], delay_an2[i], delay_an1[i]-delay_an2[i], BS))
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
