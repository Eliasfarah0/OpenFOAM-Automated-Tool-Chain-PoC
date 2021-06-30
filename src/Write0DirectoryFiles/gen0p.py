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


class pboundary:
	def __init__(self, pressure, parameters):
		self.pressure = pressure
		self.parameters = parameters
	

	def getBoundaryType(self, boundaryName):
		boundaryType = 'init'
		if boundaryName == "outlet":
			boundaryType = "fixedValue"
		elif boundaryName == "inlet":
			boundaryType = "zeroGradient"
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
			boundaryType = "zeroGradient"
		return boundaryType


class gen0pBoundaryFile:
	def __init__(self, parameters, defBC):
		self.defBC = defBC
		self.pressure = 0
		self.test = pboundary(self.pressure, parameters)
		self.pboundaryType=[]
		for i in range(0, len(self.defBC)):
			self.pboundaryType.append(self.test.getBoundaryType(self.defBC[i]))

	def writepboundaryFile(self):
		pinitialFile = open("p", "w")
		pinitialFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		pinitialFile.write("\n| ==========                |                                           |")
		pinitialFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		pinitialFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		pinitialFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		pinitialFile.write("\n|    \\\\/     M anipulation  |                                           |")
		pinitialFile.write("\n\\*---------------------------------------------------------------------*/")
		pinitialFile.write("\nFoamFile")
		pinitialFile.write("\n{")
		pinitialFile.write("\n	version		2.0;")
		pinitialFile.write("\n	format		ascii;")
		pinitialFile.write("\n	class		volScalarField;")
		pinitialFile.write("\n	location	\"0\";")
		pinitialFile.write("\n	object		p;")
		pinitialFile.write("\n}")
		pinitialFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		pinitialFile.write("\n\ndimensions	[0 2 -2 0 0 0 0];")
		pinitialFile.write("\ninternalField	uniform " + str(self.pressure) +  ";")
		pinitialFile.write("\n\nboundaryField")
		pinitialFile.write("\n{")
		for n in range(0,len(self.defBC)):
			pinitialFile.write("\n\n	"+ str(self.defBC[n]))
			pinitialFile.write("\n	{")
			pinitialFile.write("\n		type	"+ str(self.pboundaryType[n]) + ";")
			if self.pboundaryType[n]=="fixedValue":
				pinitialFile.write("\n		value	uniform " + str(self.pressure) + ";")
			pinitialFile.write("\n	}")
		pinitialFile.write("\n}")
		pinitialFile.write("\n\n// ******************************************************************* //")