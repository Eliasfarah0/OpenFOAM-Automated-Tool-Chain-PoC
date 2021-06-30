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


class genCuttingPlaneFile:
	#fileName: name of the singleGraph file
	#planeName: name given to plane
	#point: the  point given as a string in the form (x0 y0 z0)
	#normal: the normal given as a string in the form (x1 y1 z1)
	#fields: the fields taken for plotting given in the form (U p)
	def __init__(self, fileName, planeName, point, normal, fields):
		self.fileName = fileName
		self.planeName = planeName
		self.point = point
		self.normal = normal
		self.fields = fields

	def writeCuttingPlaneFile(self):
		cuttingPlaneFile = open("cuttingPlane"+str(self.fileName), "w")
		cuttingPlaneFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		cuttingPlaneFile.write("\n| ==========                |                                           |")
		cuttingPlaneFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		cuttingPlaneFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		cuttingPlaneFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		cuttingPlaneFile.write("\n|    \\\\/     M anipulation  |                                           |")
		cuttingPlaneFile.write("\n\\*---------------------------------------------------------------------*/")
		cuttingPlaneFile.write("\n\ncuttingPlane"+str(self.fileName)+"\n{")
		cuttingPlaneFile.write("\n	type			surfaces;")
		cuttingPlaneFile.write("\n	libs			(\"libsampling.so\");")
		cuttingPlaneFile.write("\n	writeControl		writeTime;")
		cuttingPlaneFile.write("\n	surfaceFormat		vtk;")
		cuttingPlaneFile.write("\n	fields			"+str(self.fields)+";")
		cuttingPlaneFile.write("\n	interpolationScheme	cellPoint;")
		cuttingPlaneFile.write("\n	surfaces")
		cuttingPlaneFile.write("\n	(")
		cuttingPlaneFile.write("\n		"+str(self.planeName))
		cuttingPlaneFile.write("\n		{")
		cuttingPlaneFile.write("\n			type		cuttingPlane;")
		cuttingPlaneFile.write("\n			planeType	pointAndNormal;")
		cuttingPlaneFile.write("\n			pointAndNormalDict")
		cuttingPlaneFile.write("\n			{")
		cuttingPlaneFile.write("\n				point	"+str(self.point)+";")
		cuttingPlaneFile.write("\n				normal	"+str(self.normal)+";")
		cuttingPlaneFile.write("\n			}")
		cuttingPlaneFile.write("\n			interpolate	true;")
		cuttingPlaneFile.write("\n		}")
		cuttingPlaneFile.write("\n	);")
		cuttingPlaneFile.write("\n}")
		cuttingPlaneFile.write("\n\n// ******************************************************************* //")