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


class genControlDictFile:
    #solver: simpleFoam, pimpleFoam
    #deltaT: time step
    #startTime: start time of simulation; default 0
    #endTime: end time of simulation; default 10
    #writeInterval: time interval to use to write output of simulation; default 5
    #sgFiles: singleGraph files
    #cpFiles: cuttingPlane files
	def __init__(self, solver, startTime, deltaT, endTime, writeInterval, sgFileCount=0, cpFileCount=0):
		self.solver = solver
		self.startTime = startTime
		self.deltaT = deltaT
		self.endTime = endTime
		self.writeInterval = writeInterval
		self.sgFileCount = sgFileCount
		self.cpFileCount = cpFileCount

	def writeControlDictFile(self):        
		controlDictFile = open("controlDict", "w")
		controlDictFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		controlDictFile.write("\n| ==========                |                                           |")
		controlDictFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		controlDictFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		controlDictFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		controlDictFile.write("\n|    \\\\/     M anipulation  |                                           |")
		controlDictFile.write("\n\\*---------------------------------------------------------------------*/")
		controlDictFile.write("\nFoamFile")
		controlDictFile.write("\n{")
		controlDictFile.write("\n	version		2.0;")
		controlDictFile.write("\n	format		ascii;")
		controlDictFile.write("\n	class		dictionary;")
		controlDictFile.write("\n	location	\"system\";")
		controlDictFile.write("\n	object		controlDict;")
		controlDictFile.write("\n}")
		controlDictFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		controlDictFile.write("\n\napplication          "+str(self.solver)+";")
		controlDictFile.write("\n\nstartFrom            latestTime;")
		controlDictFile.write("\n\nstartTime            "+str(self.startTime)+";")
		controlDictFile.write("\n\nstopAt               endTime;")
		controlDictFile.write("\n\nendTime              "+str(self.endTime)+";")
		if self.solver == "simpleFoam":
			controlDictFile.write("\n\ndeltaT               1;")
		elif self.solver == "pimpleFoam":
			controlDictFile.write("\n\ndeltaT               "+str(self.deltaT)+";")
			# controlDictFile.write("\n\nadjustTimeStep       yes;")
			# controlDictFile.write("\n\nmaxCo                4;")
			# controlDictFile.write("\n\nmaxDeltaT            0.15;")
		controlDictFile.write("\n\nwriteControl         timeStep;")
		controlDictFile.write("\n\nwriteInterval        "+str(self.writeInterval)+";")
		controlDictFile.write("\n\npurgeWrite           0;")
		controlDictFile.write("\n\nwriteFormat          ascii;")
		controlDictFile.write("\n\nwritePrecision       6;")
		controlDictFile.write("\n\nwriteCompression     off;")
		controlDictFile.write("\n\ntimeFormat           general;")
		controlDictFile.write("\n\ntimePrecision        10;")
		controlDictFile.write("\n\nrunTimeModifiable    true;")
		controlDictFile.write("\n\nfunctions")
		controlDictFile.write("\n{")
		#controlDictFile.write("\n    #includeFunc  residuals")
		controlDictFile.write("\n    #include \"forceCoeffs\"")
		if self.sgFileCount!=0 or self.cpFileCount!=0:
			if self.sgFileCount==1:
				controlDictFile.write("\n    #include \"singleGraph\"")
			elif self.sgFileCount>1:
				for i in range(0,self.sgFileCount):
					controlDictFile.write("\n    #include \"singleGraph"+str(i+1)+"\"")
			if self.cpFileCount==1:
				controlDictFile.write("\n    #include \"cuttingPlane\"")
			elif self.cpFileCount>1:
				for i in range(0,self.cpFileCount):
					controlDictFile.write("\n    #include \"cuttingPlane"+str(i+1)+"\"")
		controlDictFile.write("\n}")
		controlDictFile.write("\n\n// ******************************************************************* //")