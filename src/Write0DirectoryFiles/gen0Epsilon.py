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


class epsilonboundary:
	def __init__(self, parameters):
		self.parameters = parameters
		if self.parameters['physModel'] == 'wallModeled':
			self.turbBound = 'epsilonWallFunction'
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


class gen0epsilonBoundaryFile:
	def __init__(self, parameters, defBC):
		self.defBC = defBC
		self.test = epsilonboundary(parameters)
		self.epsilonIntensity = parameters["epsilon"]
		self.epsilonboundaryType=[]
		for i in range(0, len(self.defBC)):
			self.epsilonboundaryType.append(self.test.getBoundaryType(self.defBC[i]))

	def writeEpsilonboundaryFile(self):
		epsiloninitialFile = open("epsilon", "w")
		epsiloninitialFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		epsiloninitialFile.write("\n| ==========                |                                           |")
		epsiloninitialFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		epsiloninitialFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		epsiloninitialFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		epsiloninitialFile.write("\n|    \\\\/     M anipulation  |                                           |")
		epsiloninitialFile.write("\n\\*---------------------------------------------------------------------*/")
		epsiloninitialFile.write("\nFoamFile")
		epsiloninitialFile.write("\n{")
		epsiloninitialFile.write("\n	version		2.0;")
		epsiloninitialFile.write("\n	format		ascii;")
		epsiloninitialFile.write("\n	class		volScalarField;")
		epsiloninitialFile.write('\n	location	\"0\";')
		epsiloninitialFile.write("\n	object		epsilon;")
		epsiloninitialFile.write("\n}")
		epsiloninitialFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		epsiloninitialFile.write("\n\ndimensions	[0 2 -3 0 0 0 0];")
		epsiloninitialFile.write("\ninternalField	uniform " + str(self.epsilonIntensity) +  ";")
		epsiloninitialFile.write("\n\nboundaryField")
		epsiloninitialFile.write("\n{")
		epsiloninitialFile.write('\n	#includeEtc "caseDicts/setConstraintTypes"')
		for n in range(0,len(self.defBC)):
			epsiloninitialFile.write("\n\n	"+ str(self.defBC[n]))
			epsiloninitialFile.write("\n	{")
			epsiloninitialFile.write("\n		type		"+ str(self.epsilonboundaryType[n]) + ";")
			if self.epsilonboundaryType[n]=="inletOutlet" :
				epsiloninitialFile.write("\n		inletValue	$internalField;")
			if	self.epsilonboundaryType[n] is not "cyclic":
				if self.epsilonboundaryType[n] is not "empty":
					if self.epsilonboundaryType[n] is not "symmetry": 
						if self.epsilonboundaryType[n]=="fixedValue":
							if self.defBC[n] == 'cylinder':
								epsiloninitialFile.write("\n		value		uniform 1e-11;")
							else:
								epsiloninitialFile.write("\n		value		uniform " + str(self.epsilonIntensity) +  ";")
						else:
							epsiloninitialFile.write("\n		value		$internalField;")
			epsiloninitialFile.write("\n	}")
		epsiloninitialFile.write("\n}")
		epsiloninitialFile.write("\n\n// ******************************************************************* //")