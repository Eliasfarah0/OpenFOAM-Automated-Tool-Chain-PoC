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


class nuTildaboundary:
	def __init__(self, parameters):
		self.parameters = parameters
		# if self.parameters['physModel'] == 'wallModeled':
		# 	self.turbBound = ...
		# elif self.parameters['physModel'] == 'wallResolved':
		# 	self.turbBound = ...

	def getBoundaryType(self, boundaryName):
		boundaryType = 'init'
		if boundaryName == "outlet":
			boundaryType = "inletOutlet"
		elif boundaryName == "inlet":
			boundaryType = "fixedValue"
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
			boundaryType = "fixedValue"
		return boundaryType


class gen0NuTildaBoundaryFile:
	def __init__(self, parameters, defBC):
		self.defBC = defBC
		self.test = nuTildaboundary(parameters)
		self.nuTildaboundaryType=[]
		self.nuTildaIntensity = parameters["nuTilda"]
		for i in range(0, len(self.defBC)):
			self.nuTildaboundaryType.append(self.test.getBoundaryType(self.defBC[i]))

	def writeNuTildaboundaryFile(self):
		nuTildainitialFile = open("nuTilda", "w")
		nuTildainitialFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		nuTildainitialFile.write("\n| ==========                |                                           |")
		nuTildainitialFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		nuTildainitialFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		nuTildainitialFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		nuTildainitialFile.write("\n|    \\\\/     M anipulation  |                                           |")
		nuTildainitialFile.write("\n\\*---------------------------------------------------------------------*/")
		nuTildainitialFile.write("\nFoamFile")
		nuTildainitialFile.write("\n{")
		nuTildainitialFile.write("\n	version		2.0;")
		nuTildainitialFile.write("\n	format		ascii;")
		nuTildainitialFile.write("\n	class		volScalarField;")
		nuTildainitialFile.write("\n	location	\"0\";")
		nuTildainitialFile.write("\n	object		nuTilda;")
		nuTildainitialFile.write("\n}")
		nuTildainitialFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		nuTildainitialFile.write("\n\ndimensions	[0 2 -1 0 0 0 0];")
		nuTildainitialFile.write("\ninternalField	uniform " + str(self.nuTildaIntensity) +  ";")
		nuTildainitialFile.write("\n\nboundaryField")
		nuTildainitialFile.write("\n{")
		nuTildainitialFile.write('\n	#includeEtc "caseDicts/setConstraintTypes"')
		for n in range(0,len(self.defBC)):
			nuTildainitialFile.write("\n\n	"+ str(self.defBC[n]))
			nuTildainitialFile.write("\n	{")
			nuTildainitialFile.write("\n		type		"+ str(self.nuTildaboundaryType[n]) + ";")
			if self.nuTildaboundaryType[n]=="inletOutlet" :
				nuTildainitialFile.write("\n		inletValue	$internalField;")
			if self.nuTildaboundaryType[n] != "slip":
				if self.nuTildaboundaryType[n] != "empty":
					if self.nuTildaboundaryType[n] != "symmetry":
						if self.nuTildaboundaryType[n]== "fixedValue":
							if self.defBC[n] == 'cylinder':
								nuTildainitialFile.write("\n		value		uniform 1e-11;")
							else:
								nuTildainitialFile.write("\n		value		uniform " + str(self.nuTildaIntensity) +  ";")
						else:
							nuTildainitialFile.write("\n		value		$internalField;")
			nuTildainitialFile.write("\n	}")
		nuTildainitialFile.write("\n}")
		nuTildainitialFile.write("\n\n// ******************************************************************* //")
