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


class genSingleGraphFile:
	#fileName: name of the singleGraph file
	#start: the start point given as a string in the form (x0 y0 z0)
	#end: the end point given as a string in the form (x1 y1 z1)
	#fields: the fields taken for plotting given in the form (U p)
	def __init__(self, fileName, start, end, fields):
		self.fileName = fileName
		self.start = start
		self.end = end
		self.fields = fields

	def writeSingleGraphFile(self):
		singleGraphFile = open("singleGraph"+str(self.fileName), "w")
		singleGraphFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		singleGraphFile.write("\n| ==========                |                                           |")
		singleGraphFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		singleGraphFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		singleGraphFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		singleGraphFile.write("\n|    \\\\/     M anipulation  |                                           |")
		singleGraphFile.write("\n\\*---------------------------------------------------------------------*/")
		singleGraphFile.write("\n\nsingleGraph"+str(self.fileName))
		singleGraphFile.write("\n{")
		singleGraphFile.write("\n	start	"+str(self.start)+";")
		singleGraphFile.write("\n	end	"+str(self.end)+";")
		singleGraphFile.write("\n	fields	"+str(self.fields)+";")
		singleGraphFile.write("\n\n	// Sampling and I/O settings")
		singleGraphFile.write("\n	#includeEtc	\"caseDicts/postProcessing/graphs/sampleDict.cfg\"")
		singleGraphFile.write("\n\n	// Must be last entry")
		singleGraphFile.write("\n	#includeEtc	\"caseDicts/postProcessing/graphs/graph.cfg\"")
		singleGraphFile.write("\n}")
		singleGraphFile.write("\n\n// ******************************************************************* //")