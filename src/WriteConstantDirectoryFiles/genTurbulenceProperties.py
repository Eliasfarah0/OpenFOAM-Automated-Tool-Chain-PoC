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


class genTurbulencePropertiesFile:
    #parameters: Parameters specified in the main driver
    #turbModel: if the simulation is turbulent then specify the RAS model
	def __init__(self, parameters):
		self.flowType = parameters['flowType']
		self.turbModel = parameters['turbModel']

	def writeTurbulencePropertiesFile(self):        
		turbulencePropertiesFile = open("turbulenceProperties", "w")
		turbulencePropertiesFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		turbulencePropertiesFile.write("\n| ==========                |                                           |")
		turbulencePropertiesFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		turbulencePropertiesFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		turbulencePropertiesFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		turbulencePropertiesFile.write("\n|    \\\\/     M anipulation  |                                           |")
		turbulencePropertiesFile.write("\n\\*---------------------------------------------------------------------*/")
		turbulencePropertiesFile.write("\nFoamFile")
		turbulencePropertiesFile.write("\n{")
		turbulencePropertiesFile.write("\n	version		2.0;")
		turbulencePropertiesFile.write("\n	format		ascii;")
		turbulencePropertiesFile.write("\n	class		dictionary;")
		turbulencePropertiesFile.write("\n	location	\"constant\";")
		turbulencePropertiesFile.write("\n	object		turbulenceProperties;")
		turbulencePropertiesFile.write("\n}")
		turbulencePropertiesFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		if self.flowType == "laminar":
			turbulencePropertiesFile.write("\n\nsimulationType	laminar;")
		if self.flowType == "RAS":
			turbulencePropertiesFile.write("\n\nsimulationType	RAS;")
			turbulencePropertiesFile.write("\nRAS")
			turbulencePropertiesFile.write("\n{")
			turbulencePropertiesFile.write("\n	RASModel	"+str(self.turbModel)+";")
			turbulencePropertiesFile.write("\n	turbulence	on;")
			turbulencePropertiesFile.write("\n	printCoeffs	on;")
			turbulencePropertiesFile.write("\n}")
		turbulencePropertiesFile.write("\n\n// ******************************************************************* //")