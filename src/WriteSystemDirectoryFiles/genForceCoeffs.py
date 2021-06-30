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


from __future__             import division


class genForceCoeffsFile:
    #parameters: Parameters specified in the main driver
    #rasModel: if the simulation is turbulent then specify the RAS model
	def __init__(self, parameters):
		self.parameters = parameters
		self.Diam = parameters['Diam']
		self.U = parameters['U']
		self.geometry = 'cylinder'
		self.thick = parameters['thickness']
		self.CofR = [10*self.Diam, 10*self.Diam, self.thick/2]
		self.lRef = self.Diam
		if parameters["topology"] == "2D":
			self.Aref = self.Diam * 0.5
		elif parameters["topology"] == "3D":
			self.Aref = self.Diam * self.thick
		self.liftDir = [0, 1, 0]
		self.dragDir = [1, 0, 0]
		self.pitchAxis = [0, 0, 1]

	def writeForceCoeffsFile(self):        
		forceCoeffsFile = open("forceCoeffs", "w")
		forceCoeffsFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		forceCoeffsFile.write("\n| ==========                |                                           |")
		forceCoeffsFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		forceCoeffsFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		forceCoeffsFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		forceCoeffsFile.write("\n|    \\\\/     M anipulation  |                                           |")
		forceCoeffsFile.write("\n\\*---------------------------------------------------------------------*/")
		forceCoeffsFile.write("\n\nforceCoeffs1")
		forceCoeffsFile.write("\n{")
		forceCoeffsFile.write("\n	type		forceCoeffs;")
		forceCoeffsFile.write('\n	libs		("libforces.so");')
		forceCoeffsFile.write("\n	writeControl	timeStep;")
		forceCoeffsFile.write("\n	timeInterval	1;")
		forceCoeffsFile.write("\n	log		yes;")
		forceCoeffsFile.write("\n	pRef		0;")
		forceCoeffsFile.write("\n	patches		(" + self.geometry + ");")
		forceCoeffsFile.write("\n	rho		rhoInf;")
		forceCoeffsFile.write("\n	rhoInf		"+ str(self.parameters['rho']) +";")
		forceCoeffsFile.write("\n	liftDir		(" + str(self.liftDir[0]) + " " + str(self.liftDir[1]) + " " + str(self.liftDir[2]) + ");")
		forceCoeffsFile.write("\n	dragDir		(" + str(self.dragDir[0]) + " " + str(self.dragDir[1]) + " " + str(self.dragDir[2]) + ");")
		forceCoeffsFile.write("\n	CofR		(" + str(self.CofR[0]) + " " + str(self.CofR[1]) + " " + str(self.CofR[2]) + ");")
		forceCoeffsFile.write("\n	pitchAxis	(" + str(self.pitchAxis[0]) + " " + str(self.pitchAxis[1]) + " " + str(self.pitchAxis[2]) + ");")
		forceCoeffsFile.write("\n	magUInf		"+ str(self.U) + ";")
		forceCoeffsFile.write("\n	lRef		" + str(self.Diam) + ";")
		forceCoeffsFile.write("\n	Aref		" + str(self.Aref) + ";")
		forceCoeffsFile.write("\n	/*binData")
		forceCoeffsFile.write("\n	{")
		forceCoeffsFile.write("\n		nBin  20;")
		forceCoeffsFile.write("\n		direction (1 0 0);")
		forceCoeffsFile.write("\n		cumulative  yes;")
		forceCoeffsFile.write("\n	}*/")
		forceCoeffsFile.write("\n}")
		forceCoeffsFile.write("\n\npressureCoeff1")
		forceCoeffsFile.write("\n{")
		forceCoeffsFile.write("\n	type		pressure;")
		forceCoeffsFile.write('\n	libs		("libfieldFunctionObjects.so");')
		forceCoeffsFile.write("\n	writeControl	writeTime;")
		forceCoeffsFile.write("\n	timeInterval	" + str(self.parameters['writeInterval'] )+ ";")
		forceCoeffsFile.write("\n	log		yes;")
		forceCoeffsFile.write("\n	patch		(" + str(self.geometry) + ");")
		forceCoeffsFile.write("\n	rhoInf		" + str(self.parameters['rho']) +";")
		forceCoeffsFile.write("\n	mode		totalCoeff;")
		forceCoeffsFile.write("\n	pRef		0;")
		forceCoeffsFile.write("\n	pInf		0;")
		forceCoeffsFile.write("\n	UInf		("+ str(self.U) + " 0 0);")
		forceCoeffsFile.write("\n}")
		forceCoeffsFile.write("\n\n// ******************************************************************* //")