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
from distutils.dir_util	import copy_tree, remove_tree
from src.Write0DirectoryFiles.gen0U								import gen0UBoundaryFile
from src.Write0DirectoryFiles.gen0p								import gen0pBoundaryFile
from src.Write0DirectoryFiles.gen0k 							import gen0kBoundaryFile
from src.Write0DirectoryFiles.gen0Omega  						import gen0OmegaBoundaryFile
from src.Write0DirectoryFiles.gen0Nut 							import gen0NutBoundaryFile
from src.Write0DirectoryFiles.gen0Epsilon						import gen0epsilonBoundaryFile
from src.Write0DirectoryFiles.gen0nuTilda						import gen0NuTildaBoundaryFile
from src.WriteConstantDirectoryFiles.genTurbulenceProperties  	import genTurbulencePropertiesFile
from src.WriteConstantDirectoryFiles.genTransportProperties 	import genTransportPropertiesFile
from src.WriteSystemDirectoryFiles.genBlockMeshDict				import genBlockMeshDictFile
from src.WriteSystemDirectoryFiles.genSnappyHexMeshDict			import genSnappyHexMeshDictFile
from src.WriteSystemDirectoryFiles.genControlDict 				import genControlDictFile
from src.WriteSystemDirectoryFiles.gendecomposeParDict			import gendecomposeParDictFile
from src.WriteSystemDirectoryFiles.genfvSchemes					import genfvSchemesFile
from src.WriteSystemDirectoryFiles.genfvSolution				import genfvSolutionFile
from src.WriteSystemDirectoryFiles.genmeshQualityDict			import genmeshQualityDictFile
from src.DriverFiles.postProcessingDriver						import callPostProcessing


class createDirectories(object):
	def __init__(self, parameters, defBCname, defBCtype, defBCside, singleGraphs, cuttingPlanes):
		self.parameters = parameters
		self.defBCname = defBCname
		self.defBCtype = defBCtype
		self.defBCside = defBCside
		self.singleGraphs = singleGraphs
		self.cuttingPlanes = cuttingPlanes
		os.environ["HOME"] = os.getcwd()
		if not os.path.isdir(os.path.join(os.path.expandvars("$HOME"), str(self.parameters["folderName"]))):
			os.makedirs(os.path.join(os.path.expandvars("$HOME"), str(self.parameters["folderName"])))
		self.baseDir = os.path.join(os.path.expandvars("$HOME"), str(self.parameters["folderName"]))	
		# or directly:
		# self.baseDir = os.getcwd()
		# self.home = os.path.expandvars("$HOME")
		# if not os.path.isdir(os.path.join(self.home, str(self.parameters["folderName"]))):
		# 	os.makedirs(os.path.join(self.home, str(self.parameters["folderName"])))
		# self.baseDir = os.path.join(self.home, str(self.parameters["folderName"]))

	def writeSystemFiles(self, wallSpacing, sgFiles=0, cpFiles=0): #system/ --> blockMeshDict, snappyHexMeshDict, controlDict, fvSchemes, fvSolution, meshQualityDict, postProcessing & decomposeParDict Files 
		if not os.path.isdir(os.path.join(self.baseDir, "system")):
			os.makedirs(os.path.join(self.baseDir, "system"))
		print("Populating system/ Directory...")
		os.chdir(os.path.join(self.baseDir, "system/"))
		genBlockMeshDictFile(self.parameters, self.defBCname, self.defBCtype, self.defBCside).writeBlockFile()
		if self.parameters["topology"] == "2D":
			genBlockMeshDictFile(self.parameters, self.defBCname, self.defBCtype, self.defBCside).writeExtrudeMeshDict()
		genSnappyHexMeshDictFile(self.parameters, wallSpacing).writeSnappyFile()
		genControlDictFile(self.parameters["solver"], self.parameters["startTime"] ,self.parameters["deltaT"], self.parameters["endTime"], self.parameters["writeInterval"],sgFileCount=sgFiles, cpFileCount=cpFiles).writeControlDictFile()
		genfvSchemesFile(self.parameters).writefvSchemesFile()
		genfvSolutionFile(self.parameters).writefvSolutionFile()
		genmeshQualityDictFile().writemeshQualityDictFile()
		callPostProcessing(self.parameters, self.singleGraphs, self.cuttingPlanes).startPostProcessingProcess()
		if self.parameters["procs"] > 1:
			gendecomposeParDictFile(self.parameters).writedecomposeParDictFile()
		os.chdir(self.baseDir)

	def writeConstantFiles(self): #constant/ --> transportProperties & turbulentProperties Files 
		if not os.path.isdir(os.path.join(self.baseDir, "constant")):
			os.makedirs(os.path.join(self.baseDir, "constant"))
		print("Populating constant/ Directory...")
		os.chdir(os.path.join(self.baseDir, "constant/"))
		genTurbulencePropertiesFile(self.parameters).writeTurbulencePropertiesFile()
		genTransportPropertiesFile(self.parameters).writeTransportPropertiesFile()
		os.chdir(self.baseDir)

	def writeZeroFiles(self): #0/ --> U, p, k, epsilon, omega, nut & nuTilda Files
		if not os.path.isdir(os.path.join(self.baseDir, "0")):
			os.makedirs(os.path.join(self.baseDir, "0"))		
		print("\nPopulating 0/ Directory...")
		os.chdir(os.path.join(self.baseDir, "0/"))
		gen0UBoundaryFile(self.parameters, self.defBCname).writeUboundaryFile()
		gen0pBoundaryFile(self.parameters, self.defBCname).writepboundaryFile()
		if self.parameters["flowType"] == "RAS":
			gen0NutBoundaryFile(self.parameters, self.defBCname).writeNutboundaryFile()
			if self.parameters["turbModel"] == "SpalartAllmaras":
				gen0NuTildaBoundaryFile(self.parameters, self.defBCname).writeNuTildaboundaryFile()
			elif self.parameters["turbModel"] == "kEpsilon":
				gen0kBoundaryFile(self.parameters, self.defBCname).writekboundaryFile()
				gen0epsilonBoundaryFile(self.parameters, self.defBCname).writeEpsilonboundaryFile()
			elif self.parameters["turbModel"] == "kOmega" or self.parameters["turbModel"] == "kOmegaSST":
				gen0kBoundaryFile(self.parameters, self.defBCname).writekboundaryFile()
				gen0OmegaBoundaryFile(self.parameters, self.defBCname).writeOmegaboundaryFile()
		os.chdir(self.baseDir) #go back to self.baseDir

	def polyMeshFiles(self):
		if self.parameters["timeDerivative"] == "unsteady":
			copy_tree(os.path.join(self.baseDir, str(self.parameters["deltaT"]*3), "polyMesh"), os.path.join(self.baseDir, "constant", "polymesh"))
			for i in range(1, 4):
				deletefile = str(self.parameters["deltaT"]*i)
				remove_tree(os.path.join(self.baseDir, deletefile), verbose=True)
		else:
			copy_tree(os.path.join(self.baseDir, str(3), "polyMesh"), os.path.join(self.baseDir, "constant", "polymesh"))
			for i in range(1, 4):
				deletefile = str(i)
				remove_tree(os.path.join(self.baseDir, deletefile), verbose=True)

	def startCreatingDirectories(self, wallSpacing, sgParams=0, cpParams=0):
		self.wallSpacing = wallSpacing
		self.writeZeroFiles()
		self.writeConstantFiles()
		self.writeSystemFiles(self.wallSpacing, sgParams, cpParams)