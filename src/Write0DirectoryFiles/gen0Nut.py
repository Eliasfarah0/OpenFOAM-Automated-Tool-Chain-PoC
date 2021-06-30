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


import math


class nutboundary:
	def __init__(self, parameters):
		self.parameters = parameters
		if self.parameters['physModel'] == 'wallModeled':
			self.turbBound = 'nutUSpaldingWallFunction'
		elif self.parameters['physModel'] == 'wallResolved':
			self.turbBound = 'calculated'

	def getBoundaryType(self, boundaryName):
		boundaryType = 'init'
		if boundaryName == "outlet":
			boundaryType = "calculated"
		elif boundaryName == "inlet":
			boundaryType = "calculated"
		elif boundaryName == "topWall":
			if self.parameters['topology'] == '2D':
				boundaryType = "empty"
			elif self.parameters['topology'] == '3D':
				boundaryType = "cyclic"
		elif boundaryName == "bottomWall":
			if self.parameters['topology'] == '2D':
				boundaryType = "empty"
			elif self.parameters['topology'] == '3D':
				boundaryType = "cyclic"
		elif boundaryName == "frontWall":
			boundaryType = "symmetry"
		elif boundaryName == "backWall":
			boundaryType = "symmetry"
		elif boundaryName == "cylinder":
			boundaryType = self.turbBound
		return boundaryType


class gen0NutBoundaryFile:
	def __init__(self, parameters, defBC):
		self.defBC = defBC
		self.nutIntensity = (parameters['Cmu'] * math.pow(parameters['turbk'], 2)) / parameters['epsilon']
		# if parameters["turbModel"] == "SpalartAllmaras":
		# 	self.nutIntensity = ...
		# elif parameters["turbModel"] == "kEpsilon":
		# 	self.nutIntensity = (parameters['Cmu'] * math.pow(parameters['turbk'], 2)) / parameters['epsilon']
		# elif parameters["turbModel"] == "kOmega":
		# 	self.nutIntensity = parameters['turbk'] / parameters['omega']
		# elif parameters["turbModel"] == "kOmegaSST":
		# 	self.nutIntensity = ...
		self.test = nutboundary(parameters)
		self.nutboundaryType=[]
		for i in range(0, len(self.defBC)):
			self.nutboundaryType.append(self.test.getBoundaryType(self.defBC[i]))

	def writeNutboundaryFile(self):
		nutinitialFile = open("nut", "w")
		nutinitialFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		nutinitialFile.write("\n| ==========                |                                           |")
		nutinitialFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		nutinitialFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		nutinitialFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		nutinitialFile.write("\n|    \\\\/     M anipulation  |                                           |")
		nutinitialFile.write("\n\\*---------------------------------------------------------------------*/")
		nutinitialFile.write("\nFoamFile")
		nutinitialFile.write("\n{")
		nutinitialFile.write("\n	version		2.0;")
		nutinitialFile.write("\n	format		ascii;")
		nutinitialFile.write("\n	class		volScalarField;")
		nutinitialFile.write('\n	location	\"0\";')
		nutinitialFile.write("\n	object		nut;")
		nutinitialFile.write("\n}")
		nutinitialFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		nutinitialFile.write("\n\ndimensions	[0 2 -1 0 0 0 0];")
		nutinitialFile.write("\ninternalField	uniform " + str(self.nutIntensity) + ";")
		nutinitialFile.write("\n\nboundaryField")
		nutinitialFile.write("\n{")
		nutinitialFile.write('\n	#includeEtc "caseDicts/setConstraintTypes"')
		for n in range(0,len(self.defBC)):
			nutinitialFile.write("\n\n	"+ str(self.defBC[n]))
			nutinitialFile.write("\n	{")
			nutinitialFile.write("\n		type	"+ str(self.nutboundaryType[n]) + ";")
			if self.nutboundaryType[n] is not "cyclic":
				if self.nutboundaryType[n] is not "empty":
					if self.nutboundaryType[n] is not "symmetry":
						nutinitialFile.write("\n		value	$internalField;")
			nutinitialFile.write("\n	}")
		nutinitialFile.write("\n}")
		nutinitialFile.write("\n\n// ******************************************************************* //")