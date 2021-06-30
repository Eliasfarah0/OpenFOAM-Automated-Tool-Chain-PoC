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

class Uboundary:
	def __init__(self, parameters):
		self.parameters = parameters

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
			boundaryType = "noSlip"
		return boundaryType


class gen0UBoundaryFile:
	def __init__(self, parameters, defBC):
		self.defBC = defBC
		defBC.append("cylinder")
		self.velocity = parameters['U']
		self.test = Uboundary(parameters)
		self.UboundaryType=[]
		for i in range(0, len(self.defBC)):
			self.UboundaryType.append(self.test.getBoundaryType(self.defBC[i]))

	def writeUboundaryFile(self):
		UinitialFile = open("U", "w")
		UinitialFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		UinitialFile.write("\n| ==========                |                                           |")
		UinitialFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		UinitialFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		UinitialFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		UinitialFile.write("\n|    \\\\/     M anipulation  |                                           |")
		UinitialFile.write("\n\\*---------------------------------------------------------------------*/")
		UinitialFile.write("\nFoamFile")
		UinitialFile.write("\n{")
		UinitialFile.write("\n	version		2.0;")
		UinitialFile.write("\n	format		ascii;")
		UinitialFile.write("\n	class		volVectorField;")
		UinitialFile.write("\n	location	\"0\";")
		UinitialFile.write("\n	object		U;")
		UinitialFile.write("\n}")
		UinitialFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		UinitialFile.write("\n\ndimensions	[0 1 -1 0 0 0 0];")
		UinitialFile.write("\ninternalField	uniform (" + str(self.velocity) +  " 0 0);")
		UinitialFile.write("\n\nboundaryField")
		UinitialFile.write("\n{")
		for n in range(0,len(self.defBC)):
			UinitialFile.write("\n\n	"+ str(self.defBC[n]))
			UinitialFile.write("\n	{")
			UinitialFile.write("\n		type		"+ str(self.UboundaryType[n]) + ";")
			if self.UboundaryType[n]=="fixedValue":
				UinitialFile.write("\n		value		uniform (" + str(self.velocity) + " 0 0);")
			if self.UboundaryType[n]=="inletOutlet":
				UinitialFile.write("\n		inletValue	uniform (0 0 0);")
				UinitialFile.write("\n		value		uniform (" + str(self.velocity) + " 0 0);")
			UinitialFile.write("\n}")
		UinitialFile.write("\n}")
		UinitialFile.write("\n\n// ******************************************************************* //")