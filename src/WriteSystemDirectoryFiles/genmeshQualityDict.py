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


class genmeshQualityDictFile:
	def writemeshQualityDictFile(self):        
		meshQualityDict = open("meshQualityDict", "w") #open the file and overwrite in it
		meshQualityDict.write("/*--------------------------------*-C++-*------------------------------*\\")
		meshQualityDict.write("\n| ==========                |                                           |")
		meshQualityDict.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		meshQualityDict.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		meshQualityDict.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		meshQualityDict.write("\n|    \\\\/     M anipulation  |                                           |")
		meshQualityDict.write("\n\\*---------------------------------------------------------------------*/")
		meshQualityDict.write("\nFoamFile")
		meshQualityDict.write("\n{")
		meshQualityDict.write("\n	version		2.0;")
		meshQualityDict.write("\n	format		ascii;")
		meshQualityDict.write("\n	class		dictionary;")
		meshQualityDict.write("\n	location	\"system\";")
		meshQualityDict.write("\n	object		meshQualityDict;")
		meshQualityDict.write("\n}")
		meshQualityDict.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		meshQualityDict.write("\n\n// Include defaults parameters from master dictionary")
		meshQualityDict.write("\n#includeEtc	\"caseDicts/meshQualityDict\"")
		#meshQualityDict.write("\n//- minFaceWeight (0 -> 0.5)")
		#meshQualityDict.write("\nminFaceWeight 0.02;")
		meshQualityDict.write("\n\n// ******************************************************************* //")