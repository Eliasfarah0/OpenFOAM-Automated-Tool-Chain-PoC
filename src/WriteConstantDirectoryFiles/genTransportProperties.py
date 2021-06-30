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


class genTransportPropertiesFile:
	def __init__(self, parameters):
		self.nu = parameters['nu']
        
	def writeTransportPropertiesFile(self):
		transportPropertiesFile = open("transportProperties", "w")
		transportPropertiesFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		transportPropertiesFile.write("\n| ==========                |                                           |")
		transportPropertiesFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		transportPropertiesFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		transportPropertiesFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		transportPropertiesFile.write("\n|    \\\\/     M anipulation  |                                           |")
		transportPropertiesFile.write("\n\\*---------------------------------------------------------------------*/")
		transportPropertiesFile.write("\nFoamFile")
		transportPropertiesFile.write("\n{")
		transportPropertiesFile.write("\n	version		2.0;")
		transportPropertiesFile.write("\n	format		ascii;")
		transportPropertiesFile.write("\n	class		dictionary;")
		transportPropertiesFile.write("\n	location	\"constant\";")
		transportPropertiesFile.write("\n	object		transportProperties;")
		transportPropertiesFile.write("\n}")
		transportPropertiesFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		transportPropertiesFile.write("\n\ntransportModel	Newtonian;")
		transportPropertiesFile.write("\nnu		[0 2 -1 0 0 0 0] "+str(self.nu)+";")
		transportPropertiesFile.write("\n\n// ******************************************************************* //")