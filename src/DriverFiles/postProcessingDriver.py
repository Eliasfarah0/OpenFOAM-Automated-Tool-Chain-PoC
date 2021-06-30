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


import sys, string, os, subprocess
import numpy as np
from src.WriteSystemDirectoryFiles.genForceCoeffs  import genForceCoeffsFile
from src.WriteSystemDirectoryFiles.genSingleGraph  import genSingleGraphFile
from src.WriteSystemDirectoryFiles.genCuttingPlane import genCuttingPlaneFile
from src.WriteSystemDirectoryFiles.genStrouhal     import FourierAnalysis


class callPostProcessing(object):
	#sgDictArray: array of dictionaries with fields for singleGraphFiles. dictionary takes the form {"start":"(1.0 1e-6 0)", "end":"(1.0 0 0)", "fields": "(U p)"}
	#cpDictArray: array of dictionaries with fields for cuttingPlaneFiles. dictionary takes the form {"planeName":"yPlane","point":"(1.0 1e-6 0)", "normal":"(1.0 0 0)", "fields": "(U p)"}
	def __init__(self, parameters, sgDictArray=None, cpDictArray=None):
		self.parameters = parameters
		self.sgDictArray = sgDictArray
		self.cpDictArray = cpDictArray
		self.graphCount = 0

	def writeSingleGraphFiles(self):
		noOfFiles = len(self.sgDictArray)
		if noOfFiles==1:
			start = str(self.sgDictArray[0]["start"])
			end = str(self.sgDictArray[0]["end"])
			fields = str(self.sgDictArray[0]["fields"])
			genSingleGraphFile("", start, end, fields).writeSingleGraphFile()
		elif noOfFiles>1:
			i=1
			for paramDict in self.sgDictArray:
				start = str(paramDict["start"])
				end = str(paramDict["end"])
				fields = str(paramDict["fields"])
				genSingleGraphFile(str(i), start, end, fields).writeSingleGraphFile()
				i=i+1

	def writeCuttingPlaneFiles(self):
		noOfFiles = len(self.cpDictArray)
		if noOfFiles==1:
			planeName = str(self.cpDictArray[0]["planeName"])
			point = str(self.cpDictArray[0]["point"])
			normal = str(self.cpDictArray[0]["normal"])
			fields = str(self.cpDictArray[0]["fields"])
			genCuttingPlaneFile("", planeName, point, normal, fields).writeCuttingPlaneFile()
		elif noOfFiles>1:
			i=1
			for paramDict in self.cpDictArray:
				planeName = str(paramDict["planeName"])
				point = str(paramDict["point"])
				normal = str(paramDict["normal"])
				fields = str(paramDict["fields"])
				genCuttingPlaneFile(str(i), planeName, point, normal, fields).writeCuttingPlaneFile()
				i=i+1

	def processStrouhalAndFFT(self, data, fmax, inletVelocity, refLength, fft_name=None):
		fourierObject = FourierAnalysis(data, fmax)
		if fft_name is not None:
			fft = fourierObject.writeFFT(fft_name)
		return (fourierObject.doStrouhal(inletVelocity, refLength))

	def startPostProcessingProcess(self):
		genForceCoeffsFile(self.parameters).writeForceCoeffsFile()
		self.writeCuttingPlaneFiles()
		self.writeSingleGraphFiles()

	def strouhalNumberCalculation(self, time_point=1):
		post_proc_file = open("postProcessing/forceCoeffs1/0/coefficient.dat", "r")
		fftGPFile = open("strouhal.gp", "w")
		lines = post_proc_file.readlines()
		time = []
		#lift = []
		drag = []
		for line in lines:
			this_line = line.split('\t')
			if this_line[0][0] == '#':
				continue
			else:
				time.append(float(this_line[0]))
				#lift.append(float(this_line[3]))
				drag.append(float(this_line[2]))
		if time<len(lines):
			print("\nTime provided is not within the range")
			return
		ts = abs(np.mean(time[(int(time_point)-1):len(time)-1])-np.mean(time[int(time_point):len(time)]))
		fmax = 1/(2*ts)
		#lift_strouhal = self.processStrouhalAndFFT(lift[int(time_point)-1:], fmax, self.parameters['U'] , 1, "lift_fft")
		drag_strouhal = self.processStrouhalAndFFT(drag[int(time_point)-1:], fmax, self.parameters['U'] , 1, "drag_fft")
		#print("\nThe Strouhal Number for the Lift:")
		#print('%.4f' % lift_strouhal)
		fftGPFile.write("set terminal x11 "+str(self.graphCount))
		fftGPFile.write("\nset title \"FFT for Drag\"")
		fftGPFile.write("\nset xlabel \"Frquency\"")
		fftGPFile.write("\nset ylabel \"Amplitude\"")
		self.graphCount = self.graphCount + 1
		fftGPFile.write("\nset style data lines")
		fftGPFile.write("\nplot \"drag_fft\" every ::1 u 1:2")
		print("\nThe Strouhal Number for the Drag:")
		print('%.4f' % drag_strouhal)

	def outputSingleGraph(self, time=1, whichGraph=None, component='U', u_component=["x", "y", "z"]):
		file_name = "singleGraph_"+str(component)+".gp"
		sgGPFile = open(file_name, "w")
		axes = ["x", "y", "z"]
		for i in u_component:
			sgGPFile.write("\nset terminal x11 "+str(self.graphCount))
			sgGPFile.write("\nset title \"Single Graph for "+str(component)+" at time "+str(time)+"\"")
			sgGPFile.write("\nset xlabel \"Point along line\"")
			sgGPFile.write("\nset ylabel \"Magnitude\"")
			self.graphCount = self.graphCount + 1
			sgGPFile.write("\nset style data lines")
			if whichGraph is None:
				sgGPFile.write("\nplot \"postProcessing/singleGraph/"+str(time)+"/line_"+str(component)+".xy\" u 1:"+str(axes.index(i)+2))
			else:
				sgGPFile.write("\nplot \"postProcessing/singleGraph"+str(whichGraph)+"/"+str(time)+"/line_"+str(component)+".xy\" u 1:"+str(axes.index(i)+2))

	def outputForceCoeffs(self):
		dragFile = open("drag.gp", "w")
		dragFile.write("\nset terminal x11 " + str(self.graphCount))
		self.graphCount = self.graphCount + 1
		dragFile.write("\nset title \"Drag Coefficient\"")
		dragFile.write("\nset xlabel \"Time\"")
		dragFile.write("\nset style data lines")
		dragFile.write("\nplot \"postProcessing/forceCoeffs1/0/coefficient.dat\" every ::13 u 1:2")
		liftFile = open("lift.gp", "w")
		liftFile.write("\nset terminal x11 "+ str(self.graphCount))
		self.graphCount = self.graphCount + 1
		liftFile.write("\nset title \"Lift Coefficient\"")
		liftFile.write("\nset xlabel \"Time\"")
		liftFile.write("\nset style data lines")
		liftFile.write("\nplot \"postProcessing/forceCoeffs1/0/coefficient.dat\" every ::13 u 1:4")