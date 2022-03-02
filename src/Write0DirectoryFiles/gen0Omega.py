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


class omegaboundary:
	def __init__(self, parameters):
		self.parameters = parameters
		if self.parameters['physModel'] == 'wallModeled':
			self.turbBound = 'omegaWallFunction'
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


class gen0OmegaBoundaryFile:
	def __init__(self, parameters, defBC):
		self.defBC = defBC
		self.test = omegaboundary(parameters)
		self.omegaIntensity = parameters["omega"]
		self.omegaboundaryType=[]
		for i in range(0, len(self.defBC)):
			self.omegaboundaryType.append(self.test.getBoundaryType(self.defBC[i]))

	def writeOmegaboundaryFile(self):
		omegainitialFile = open("omega", "w")
		omegainitialFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		omegainitialFile.write("\n| ==========                |                                           |")
		omegainitialFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		omegainitialFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		omegainitialFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		omegainitialFile.write("\n|    \\\\/     M anipulation  |                                           |")
		omegainitialFile.write("\n\\*---------------------------------------------------------------------*/")
		omegainitialFile.write("\nFoamFile")
		omegainitialFile.write("\n{")
		omegainitialFile.write("\n	version		2.0;")
		omegainitialFile.write("\n	format		ascii;")
		omegainitialFile.write("\n	class		volScalarField;")
		omegainitialFile.write("\n	location	\"0\";")
		omegainitialFile.write("\n	object		omega;")
		omegainitialFile.write("\n}")
		omegainitialFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		omegainitialFile.write("\n\ndimensions	[0 0 -1 0 0 0 0];")
		omegainitialFile.write("\ninternalField	uniform " + str(self.omegaIntensity) +  ";")
		omegainitialFile.write("\n\nboundaryField")
		omegainitialFile.write("\n{")
		omegainitialFile.write('\n	#includeEtc "caseDicts/setConstraintTypes"')
		for n in range(0,len(self.defBC)):
			omegainitialFile.write("\n\n	"+ str(self.defBC[n]))
			omegainitialFile.write("\n	{")
			omegainitialFile.write("\n		type		"+ str(self.omegaboundaryType[n]) + ";")
			if self.omegaboundaryType[n]=="inletOutlet":
				omegainitialFile.write("\n		inletValue	$internalField;")
			if	self.omegaboundaryType[n] != "cyclic":
				if self.omegaboundaryType[n] != "empty":
					if self.omegaboundaryType[n] != "symmetry":
						if self.omegaboundaryType[n]=="fixedValue":
							if self.defBC[n] == 'cylinder':
								omegainitialFile.write("\n		value		uniform 1e-11;")
							else:
								omegainitialFile.write("\n		value		uniform " + str(self.omegaIntensity) +  ";")
						else:
							omegainitialFile.write("\n		value		$internalField;")
			omegainitialFile.write("\n	}")
		omegainitialFile.write("\n}")
		omegainitialFile.write("\n\n// ******************************************************************* //")
