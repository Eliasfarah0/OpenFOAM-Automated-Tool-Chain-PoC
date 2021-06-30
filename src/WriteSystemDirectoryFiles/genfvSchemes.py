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


class genfvSchemesFile:
	def __init__(self, parameters):
		self.timeDerivative = parameters["timeDerivative"]
		self.flowType = parameters["flowType"]
		self.turbModel = parameters["turbModel"]    # SpalartAllmaras or kEpsilon or kOmega or kOmegaSST
		self.physModel = parameters["physModel"]

	def writefvSchemesFile(self):
		fvSchemesFile = open("fvSchemes", "w")
		fvSchemesFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		fvSchemesFile.write("\n| ==========                |                                           |")
		fvSchemesFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		fvSchemesFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		fvSchemesFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		fvSchemesFile.write("\n|    \\\\/     M anipulation  |                                           |")
		fvSchemesFile.write("\n\\*---------------------------------------------------------------------*/")
		fvSchemesFile.write("\nFoamFile")
		fvSchemesFile.write("\n{")
		fvSchemesFile.write("\n	version		2.0;")
		fvSchemesFile.write("\n	format		ascii;")
		fvSchemesFile.write("\n	class		dictionary;")
		fvSchemesFile.write("\n	location	\"system\";")
		fvSchemesFile.write("\n	object		fvSchemes;")
		fvSchemesFile.write("\n}")
		fvSchemesFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		fvSchemesFile.write("\n\nddtSchemes")
		fvSchemesFile.write("\n{")
		if self.timeDerivative == "unsteady":
			fvSchemesFile.write("\n    default    Euler;")
			# fvSchemesFile.write("\n    default    backward;")
			# fvSchemesFile.write("\n    default    CrankNicolson 0.9;")
		if self.timeDerivative == "steady":
			fvSchemesFile.write("\n    default    steadyState;")
		fvSchemesFile.write("\n}")
		fvSchemesFile.write("\n\ngradSchemes")
		fvSchemesFile.write("\n{")
		fvSchemesFile.write("\n    default    Gauss linear;")
		fvSchemesFile.write("\n}")
		fvSchemesFile.write("\n\ndivSchemes")
		fvSchemesFile.write("\n{")
		fvSchemesFile.write("\n    default                          none;")
		# fvSchemesFile.write("\n    div(phi,U)                       Gauss upwind;")
		fvSchemesFile.write("\n    div(phi,U)                       Gauss linearUpwind grad(U);")
		fvSchemesFile.write("\n    div((nuEff*dev2(T(grad(U)))))    Gauss linear;")
		if self.flowType == "RAS":
			if self.turbModel == "kEpsilon":
				fvSchemesFile.write("\n    div(phi,k)                       Gauss upwind;")
				fvSchemesFile.write("\n    div(phi,epsilon)                 Gauss upwind;")
			elif self.turbModel == "kOmega" or self.turbModel == "kOmegaSST":
				fvSchemesFile.write("\n    div(phi,k)                       Gauss upwind;")
				fvSchemesFile.write("\n    div(phi,omega)                   Gauss upwind;")
			elif self.turbModel == "SpalartAllmaras":
				fvSchemesFile.write("\n    div(phi,nuTilda)                 Gauss upwind;")
		fvSchemesFile.write("\n}")
		fvSchemesFile.write("\n\nlaplacianSchemes")
		fvSchemesFile.write("\n{")
		fvSchemesFile.write("\n    default    Gauss linear corrected;")
		fvSchemesFile.write("\n}")
		fvSchemesFile.write("\n\ninterpolationSchemes")
		fvSchemesFile.write("\n{")
		fvSchemesFile.write("\n    default    linear;")
		fvSchemesFile.write("\n}")
		fvSchemesFile.write("\n\nsnGradSchemes")
		fvSchemesFile.write("\n{")
		fvSchemesFile.write("\n    default    corrected;")
		fvSchemesFile.write("\n}")
		if self.flowType == "RAS":
			if self.turbModel == "SpalartAllmaras" or self.turbModel == "kOmegaSST":
				fvSchemesFile.write("\n\nwallDist")
				fvSchemesFile.write("\n{")
				fvSchemesFile.write("\n    method          meshWave;")
				fvSchemesFile.write("\n    correctWalls    true;")
				fvSchemesFile.write("\n}")
		fvSchemesFile.write("\n\n// ******************************************************************* //")