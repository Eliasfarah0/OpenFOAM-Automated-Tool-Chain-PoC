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


class kboundary:
	def __init__(self, parameters):
		self.parameters = parameters
		if self.parameters['physModel'] == 'wallModeled':
			self.turbBound = 'kqRWallFunction'
		elif self.parameters['physModel'] == 'wallResolved':
			self.turbBound = 'fixedValue'

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
			boundaryType = self.turbBound
		return boundaryType


class gen0kBoundaryFile:
	def __init__(self, parameters, defBC):
		self.defBC = defBC
		self.test = kboundary(parameters)
		self.kboundaryType=[]
		self.kIntensity = parameters['turbk']
		for i in range(0, len(self.defBC)):
			self.kboundaryType.append(self.test.getBoundaryType(self.defBC[i]))

	def writekboundaryFile(self):
		kinitialFile = open("k", "w")
		kinitialFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		kinitialFile.write("\n| ==========                |                                           |")
		kinitialFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		kinitialFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		kinitialFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		kinitialFile.write("\n|    \\\\/     M anipulation  |                                           |")
		kinitialFile.write("\n\\*---------------------------------------------------------------------*/")
		kinitialFile.write("\nFoamFile")
		kinitialFile.write("\n{")
		kinitialFile.write("\n	version		2.0;")
		kinitialFile.write("\n	format		ascii;")
		kinitialFile.write('\n	location	\"0\";')
		kinitialFile.write("\n	class		volScalarField;")
		kinitialFile.write("\n	object		k;")
		kinitialFile.write("\n}")
		kinitialFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		kinitialFile.write("\n\ndimensions	[0 2 -2 0 0 0 0];")
		kinitialFile.write("\ninternalField	uniform " + str(self.kIntensity) +  ";")
		kinitialFile.write("\n\nboundaryField")
		kinitialFile.write("\n{")
		kinitialFile.write('\n	#includeEtc "caseDicts/setConstraintTypes"')
		for n in range(0,len(self.defBC)):
			kinitialFile.write("\n\n	"+ str(self.defBC[n]))
			kinitialFile.write("\n	{")
			kinitialFile.write("\n		type		"+ str(self.kboundaryType[n]) + ";")
			if self.kboundaryType[n]=="inletOutlet" :
				kinitialFile.write("\n		inletValue	$internalField;")
			elif self.kboundaryType[n] != "cyclic":
				if self.kboundaryType[n] != "empty":
					if self.kboundaryType[n] != "symmetry":
						if self.kboundaryType[n]== "fixedValue":
							if self.defBC[n]== 'cylinder':
								kinitialFile.write("\n		value		uniform 1e-11;")
							else:
								kinitialFile.write("\n		value		uniform " + str(self.kIntensity) +  ";")
						else:
							kinitialFile.write("\n		value		$internalField;")
			kinitialFile.write("\n	}")
		kinitialFile.write("\n}")
		kinitialFile.write("\n\n// ******************************************************************* //")
