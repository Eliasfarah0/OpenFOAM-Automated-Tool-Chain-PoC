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


class gendecomposeParDictFile:
	def __init__(self, parameters):
		self.procs = parameters['procs']
        
	def writedecomposeParDictFile(self):
		decomposeParDictFile = open("decomposeParDict", "w")
		decomposeParDictFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		decomposeParDictFile.write("\n| ==========                |                                           |")
		decomposeParDictFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		decomposeParDictFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		decomposeParDictFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		decomposeParDictFile.write("\n|    \\\\/     M anipulation  |                                           |")
		decomposeParDictFile.write("\n\\*---------------------------------------------------------------------*/")
		decomposeParDictFile.write("\nFoamFile")
		decomposeParDictFile.write("\n{")
		decomposeParDictFile.write("\n	version		2.0;")
		decomposeParDictFile.write("\n	format		ascii;")
		decomposeParDictFile.write("\n	class		dictionary;")
		decomposeParDictFile.write("\n	location	\"system\";")
		decomposeParDictFile.write("\n	object		decomposeParDict;")
		decomposeParDictFile.write("\n}")
		decomposeParDictFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		# decomposeParDictFile.write('\n\nlibs	("libmetis.so");')
		decomposeParDictFile.write("\n\nnumberOfSubdomains "+str(self.procs)+";")
		decomposeParDictFile.write("\n\nmethod			scotch;")
		decomposeParDictFile.write("\n\nscotchCoeffs")
		decomposeParDictFile.write("\n{")
		decomposeParDictFile.write("\n	processorWeights")
		decomposeParDictFile.write("\n	(")
		for i in range(1, self.procs + 1):
			decomposeParDictFile.write("\n		1")
		decomposeParDictFile.write("\n	);")
		decomposeParDictFile.write("\n}")
		# decomposeParDictFile.write("\n\nmethod			simple;")
		# decomposeParDictFile.write("\n\nsimpleCoeffs")
		# decomposeParDictFile.write("\n{")
		# decomposeParDictFile.write("\nn (2 2 1);")
		# decomposeParDictFile.write("\ndelta 0.001;")
		# decomposeParDictFile.write("\n}")
		decomposeParDictFile.write("\n\n// ************************************************************************* //")