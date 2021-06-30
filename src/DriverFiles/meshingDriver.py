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


import os, os.path, sys, string, shutil, glob, subprocess, math


class callMeshing(object):
	def __init__(self, parameters):
		self.parameters = parameters

	def getFirstCellSpacing(self):
		Cf=0.058/(pow(self.parameters["Re"] , 0.2))
		tauWall=(Cf*self.parameters["rho"]*pow(self.parameters["U"],2))/2
		Ufric=math.sqrt(tauWall/self.parameters["rho"])
		firstCellSpacing=self.parameters["yplus"]*self.parameters["nu"]/Ufric
		return firstCellSpacing

	def inflationLayersParameters(self):
		initialLayerThickness = 0.1
		targetLayerThickness = self.getFirstCellSpacing()*2
		iterLayer = initialLayerThickness
		expansionRatio = 1.04
		ratio = [0.85]
		iterCounter = 0
		while iterLayer >= targetLayerThickness:
			iterLayer = iterLayer * ratio[iterCounter]
			newRatio =(ratio[iterCounter]/expansionRatio)
			ratio.append(newRatio)
			iterCounter = iterCounter + 1
		return ratio, iterCounter

	def addLayers(self):
		layerParameters = self.inflationLayersParameters()
		ratio = layerParameters[0]
		counter = layerParameters[1]
		for i in range(0,counter):
			argr=["refineWallLayer -overwrite '(cylinder)' "  + str(ratio[i])]
			subprocess.call(argr, shell = True)

	def startMeshingProcess(self):
		#layerParameters = self.inflationLayersParameters()
		#ratio = layerParameters[0]
		print("\nRunning Backgroung Mesh...")
		argv = ["blockMesh"]
		subprocess.call(argv)
		print("\nCreating the Mesh...")
		argv = ["snappyHexMesh"]
		subprocess.call(argv)
		#if ratio != 0:
		#	self.addLayers()

	def generate2Dmesh(self):
		#set first the right boundary conditions in the polymesh folder for the 2D case
		os.environ["HOME"] = os.getcwd()
		os.chdir(os.path.join(os.path.expandvars("$HOME"), "constant/", "polymesh/"))
		with open('boundary', 'r') as file :
			filedata = file.read()
		# Replace the target string
		filedata = filedata.replace('cyclic', 'empty')
		# Write the file out again
		with open('boundary', 'w') as file:
			file.write(filedata)
		os.chdir(os.path.expandvars("$HOME"))
		#Call the openfoam utility to extract the 2D mesh
		print("\nExtruding mesh to 2D")
		argv = ["extrudeMesh"]
		subprocess.call(argv)