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
allfreq=[]
freq_arr=np.transpose(allfreq)

#===============================================================================
#  Model Evaluation using lalsuite executables
#===============================================================================
def lalsim_inspiral(mass1 = 1.35e+00,                        # mass of primary   (solar mass)
                    mass2 = 1.45e+00,                        # mass of secondary (solar mass)
                    lambda1= 5.0e+02,                        # tildal deformability primary
                    lambda2= 5.0e+02,                        # tildal deformability secondary
                    spin1 = [0.0, 0.0, 0.0],                 # dimensionless spin of primary
                    spin2 = [0.0, 0.0, 0.0],                 # dimensionless spin of secondary
                    Freq_arr=freq_arr,
                    approximant = "SEOBNRv4T",				 # approximant
                    output_domain = "time",      			 # waveform in "time" or "freq" domain
                    f_min=500,                               # starting GW frequency (Hertz)
                    f_ref = 0.0,                             # reference frequency (Hertz)
                    phi_ref=0.0,                              # reference phase (rad)
                    lalsim_inspiral_bin = "lalsim-inspiral",
                    srate = 16384., #16384                          # sample rate (Hertz)
                    verbose = False):

  command = lalsim_inspiral_bin + " --m1 %.2f --m2 %.2f" % (mass1, mass2)
  command += " --spin1x %.2f --spin1y %.2f --spin1z %.2f" % (spin1[0], spin1[1], spin1[2])
  command += " --spin2x %.2f --spin2y %.2f --spin2z %.2f" % (spin2[0], spin2[1], spin2[2])
  command += " --tidal-lambda1 %.2f" % (lambda1)
  command += " --tidal-lambda2 %.2f" % (lambda2)
  command += " --approximant %s" % (approximant)
  command += " --f-min %.2f --fRef %.2f" %(f_min,f_ref)
  command += " --sample-rate %.2f" % (srate)

  if output_domain == "time":
    command += " --condition-waveform" # apply waveform conditioning
  elif output_domain in ["freq", "frequency"]:
    command += " --frequency-domain"
  else:
    printf("Unknown output_domain. Ignoring ...", __file__, type="warning")
    printf("Output_domain is set to be 'time'.", __file__, type="warning")
    command += " --condition-waveform" # apply waveform conditioning

  if verbose:
    printf(command, __file__, type="verbose")

  output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
  lines = output.stdout.readlines()[1:]
  lines = np.array([k.strip('\n') for k in lines])
  
  x  = []
  h_p = [] # in case of amp_phase, it is amplitude (strain)!
  h_c = [] # in case of amp_phase, it is phase (in rad)!
  
  if output_domain == "time":
    for l in lines:
      x.append(float(l.split("\t")[0]))
      h_p.append(float(l.split("\t")[1]))
      h_c.append(float(l.split("\t")[2]))
  elif output_domain in [ "freq", "frequency" ]:
    for l in lines:
      x.append(float(l.split("\t")[0]))                             # frequency
      h_p.append([float(l.split("\t")[1]), float(l.split("\t")[2])]) # [hp_real, hp_imag] (in case of amp_phase, it is [abs hp (strain), arg hp (in rad)])
      h_c.append([float(l.split("\t")[3]), float(l.split("\t")[4])]) # [hc_real, hc_imag] (in case of amp_phase, it is [abs hc (strain), arg hc (in rad)])
  else:
    printf("Only use \"time\" or \"freq\" as the output_domain.", __file__, "error")
    return None, None, None

#===============================================================================
# Plot the h+ result
#===============================================================================
  hc=np.array(h_c)
  hp=np.array(h_p)
  t=np.array(x)
  envelope=(hp**2 + hc**2)**0.5

#===============================================================================
# Locate and Return Frequency at Peak Amplitude
#===============================================================================
  max_amp_tuple=np.where(envelope==max(envelope))
  max_amp=max_amp_tuple[0]-1
  max_amp_time=t[max_amp]
  dt=1./srate
  print("The time at max amplitude for this data point is %s" %(max_amp_time))

  phase = np.unwrap(np.angle(hp+1j*hc))
  dphi = np.gradient(phase)/dt
  frequency = dphi/(2.*np.pi)
  max_amp_freq=frequency[max_amp]
  if max_amp_freq<800:
    max_amp_new=max_amp-1
    max_amp_freq=frequency[max_amp_new]
    print("The old frequency was %s"%(frequency[max_amp]))
  print("The frequency at max amplitude for his data point is %s \n" %(max_amp_freq))
  freq_arr=np.append(Freq_arr,max_amp_freq)

#plt.figure()
# plt.plot(t, hp)
# plt.scatter(max_amp_time,hp[max_amp],c='r',s=10)
# plt.plot(t, envelope)
# plt.savefig("Test")

  return [x, h_p, h_c,freq_arr];

#===============================================================================
# Rinse and Repeat for Every Spin {0,0.6}
#===============================================================================
spin_arr=np.arange(0,0.6,0.05)
for value in spin_arr:
  print("The spin for this data point is %s"%(value))
  spin1=[0,0,-value]
  spin2=[0,0,-value]
  temparr=lalsim_inspiral(1.35,1.45,500,500,spin1,spin2,freq_arr)
  freq_arr=temparr[3]
#np.save("H4.npy",freq_arr)
np.savetxt("SEOBAntiAlignedSpinFreqArr.txt",freq_arr)

#===============================================================================
# Create Histogram of Frequency Data
#===============================================================================
#plt.hist(freq_arr)  # arguments are passed to np.histogram
#plt.title("Frequency at Maximum Amplitude with Maxmimum Mass")
#plt.xlabel("Frequency")
#plt.ylabel("Count")
#plt.show()
#plt.savefig("HistFreqMaxAmp4")
