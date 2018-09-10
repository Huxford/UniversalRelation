#===============================================================================
#  Imports & Set-Up
#===============================================================================
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

#===============================================================================
#  Read in Mass and Lambda Files
#===============================================================================
Lambda1=[];Lambda2=[];Mass1=[];Mass2=[];Freq_arr=[]

data=open('AllFiles.txt','r')
for line in data.readlines():
    Lambda1.append(float(line.split(' ')[2]))
    Lambda2.append(float(line.split(' ')[3]))
    Mass1.append(float(line.split(' ')[0]))
    Mass2.append(float(line.split(' ')[1]))



data4=open('AllFreqArrLowInd.txt','r')
for line in data4.readlines():
    Freq_arr.append(float(line.split()[0]))

#===============================================================================
#  Create arrays of integers for x,y,z
#===============================================================================
lambda1_arr=np.array(Lambda1)
lambda2_arr=np.array(Lambda2)
mass1_arr=np.array(Mass1)
mass2_arr=np.array(Mass2)
freq_arr=np.array(Freq_arr)

# We have three dimensions of data. x and y will be plotted on the x and y axis, while z will
# be represented with color. If z is a numpy array, matplotlib refuses to plot this.
x = lambda1_arr
y = lambda2_arr
z = freq_arr

# cmap will generate a tuple of RGBA values for a given number in the range 0.0 to 1.0
# To map our z values cleanly to this range, we create a Normalize object.
cmap = matplotlib.cm.get_cmap('viridis')
normalize = matplotlib.colors.Normalize(vmin=min(z), vmax=max(z))
colors = [cmap(normalize(value)) for value in z]

fig, ax = plt.subplots(figsize=(10,10))
ax.scatter(x, y, color=colors)
plt.xlabel("$\Lambda_1$")
plt.ylabel("$\Lambda_2$")
plt.title("Lambda-Frequency Relationship")

# Optionally add a colorbar
cax, _ = matplotlib.colorbar.make_axes(ax)
cbar = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap, norm=normalize)
plt.ylabel("Frequency (Hz)")
plt.savefig("LambdavFreqScatterTotalLowInd")
