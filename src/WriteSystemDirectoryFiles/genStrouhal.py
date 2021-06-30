#########################################################################
#                                                                       #
#                C R A N F I E L D   U N I V E R S I T Y                #
#                          2 0 1 9  /  2 0 2 0                          #
#                                                                       #
#               MSc in Aerospace Computational Engineering              #
#                                                                       #
#                          Group Design Project                         #
#                                                                       #
#           Driver File for the OpenFoam Automated Tool Chain           #
#                      Flow Past Cylinder Test Case                     #
#                                                                       #
#-----------------------------------------------------------------------#
#                                                                       #
#   Main Contributors:                                                  #
#       Vadim Maltsev          (Email: V.Maltsev@cranfield.ac.uk)       #
#       Samali Liyanage        (Email: Samali.Liyanage@cranfield.ac.uk) #
#       Elias Farah            (Email: E.Farah@cranfield.ac.uk)         #
#   Supervisor:                                                         #
#       Dr. Tom-Robin Teschner (Email: Tom.Teschner@cranfield.ac.uk )   #
#                                                                       #
#########################################################################


import numpy as np
from math import ceil


class FourierAnalysis(object):
	def __init__(self, data, fmax, n=None, axis=-1, norm=None):
		self.data = data
		self.fmax = fmax
		self.n = n
		self.axis = axis
		self.norm = norm

	def doFFT(self):
		return	np.fft.fft(self.data, self.n, self.axis, self.norm)

	def doStrouhal(self, U, L):
		strouhal_array = []
		f_fft = self.doFFT()
		f_fft = f_fft[0:int(ceil((len(f_fft)+1)/2))] #Since FFt is symmetrical get half of the array
		#i = (f_fft.index(max(f_fft))+1)*self.fmax/float(len(f_fft))
		i = (np.where(f_fft==max(f_fft))[0][0]+1)*self.fmax/float(len(f_fft))
		return (abs(i)*L/U)

	def writeFFT(self, fname):
		fft_file = open(fname, "w")
		fft_file.write("Fq\tAmp")
		fft = self.doFFT()
		fft = fft[0:int(ceil((len(fft)+1)/2))]
		freq = 1
		for i in fft:
			fft_file.write("\n"+str(freq*self.fmax/float(len(fft)))+"\t"+str(abs(i)))
			freq = freq + 1