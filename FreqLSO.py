#===============================================================================
#  Imports & Set-Up
#===============================================================================

import lalsimulation as lalsim
import lal
from lal import MTSUN_SI, PC_SI, C_SI
from operator import add
import numpy as np
import subprocess
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import h5py

# defining constants
PI =  np.pi
c = 3*10**8
G = 6.674*10**(-11)
MSun=1.998*10**30

#===============================================================================
# Read data from previous work & generate total mass array
#===============================================================================
Lambda1=[];Lambda2=[];Mass1=[];Mass2=[];Mass=[]

data= open('ParamMaxMass.txt','r')
for line in data.readlines():
    Lambda1.append(float(line.split(' ')[2]))
    Lambda2.append(float(line.split(' ')[3]))
    Mass1.append(float(line.split(' ')[0]))
    Mass2.append(float(line.split(' ')[1]))

data2= open('ParamNoMaxMass.txt','r')
for line in data2.readlines():
    Lambda1.append(float(line.split(' ')[2]))
    Lambda2.append(float(line.split(' ')[3]))
    Mass1.append(float(line.split(' ')[0]))
    Mass2.append(float(line.split(' ')[1]))

data3=open('EoS.txt','r')
for line in data3.readlines():
    Lambda1.append(float(line.split(' ')[2]))
    Lambda2.append(float(line.split(' ')[3]))
    Mass1.append(float(line.split(' ')[0]))
    Mass2.append(float(line.split(' ')[1]))

mass1=np.array(Mass1)
mass2=np.array(Mass2)
for n in range(0,len(Mass1)):
  mass_total=Mass1[n]+Mass2[n]
  Mass.append(mass_total)

#===============================================================================
# Calculate Frequency at Last Stable Orbit for every point
#===============================================================================
freq_arr=[]
for n in range(0,len(Mass1)):
  frequency = ((c**3)/(PI*Mass[n]*MSun*(6**1.5)*G))
  freq_arr.append(frequency)

np.savetxt("fLSOTotal.txt",freq_arr)

#===============================================================================
# Create Histogram of Frequency Data
#===============================================================================
plt.hist(freq_arr)  # arguments are passed to np.histogram
plt.title("Frequency at Last Stable Orbit with All Data")
plt.xlabel("Frequency(Hz)")
plt.ylabel("Count")
plt.show()
plt.savefig("HistfLSOTotal")
