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


class genfvSolutionFile:
	def __init__(self, parameters):
		self.timeDerivative = parameters["timeDerivative"]
		self.flowType = parameters["flowType"]
		self.consistent = parameters["consistent"]

	def writefvSolutionFile(self):        
		fvSolutionFile = open("fvSolution", "w") #open the file and overwrite in it
		fvSolutionFile.write("/*--------------------------------*-C++-*------------------------------*\\")
		fvSolutionFile.write("\n| ==========                |                                           |")
		fvSolutionFile.write("\n| \\\\      /  F ield         | OpenFoam: The Open Source CFD Tooolbox    |")
		fvSolutionFile.write("\n|  \\\\    /   O peration     | Version: check the installation           |")
		fvSolutionFile.write("\n|   \\\\  /    A nd           | Website: www.openfoam.com                 |")
		fvSolutionFile.write("\n|    \\\\/     M anipulation  |                                           |")
		fvSolutionFile.write("\n\\*---------------------------------------------------------------------*/")
		fvSolutionFile.write("\nFoamFile")
		fvSolutionFile.write("\n{")
		fvSolutionFile.write("\n	version		2.0;")
		fvSolutionFile.write("\n	format		ascii;")
		fvSolutionFile.write("\n	class		dictionary;")
		fvSolutionFile.write("\n	location	\"system\";")
		fvSolutionFile.write("\n	object		fvSolution;")
		fvSolutionFile.write("\n}")
		fvSolutionFile.write("\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //")
		###########
		# SOLVERS #
		###########
		fvSolutionFile.write("\n\nsolvers")
		fvSolutionFile.write("\n{")
		fvSolutionFile.write("\n    // Solver information for each solution variable")
		########## STEADY OR UNSTEADY (LAMINAR OR RAS) ##########
		fvSolutionFile.write("\n    p")
		fvSolutionFile.write("\n    {")
		fvSolutionFile.write("\n        solver          GAMG;")
		fvSolutionFile.write("\n        smoother        GaussSeidel;") # or DICGaussSeidel (GaussSeidel --> Symmetric or asymmetric // DICGaussSeidel --> Symmetric matrices)
		fvSolutionFile.write("\n        tolerance       1e-06;") # we should specify a value: 10^-4<tolerance<10^-8
		fvSolutionFile.write("\n        relTol          0.01;") # we should specify a value: 0.01 < relTol < 0.1
		fvSolutionFile.write("\n    }")
		fvSolutionFile.write("\n\n    \"(U|nuTilda|k|epsilon|omega)\"")
		fvSolutionFile.write("\n    {")
		# fvSolutionFile.write("\n        solver            smoothSolver;") # or solver          PBiCGStab;
		# fvSolutionFile.write("\n        smoother          GaussSeidel;") #  or preconditioner  DILU
		# fvSolutionFile.write("\n        nSweeps           2;")
		fvSolutionFile.write("\n        solver            PBiCG;")
		fvSolutionFile.write("\n        preconditioner    DILU;")		
		fvSolutionFile.write("\n        tolerance         1e-06;") # PBiCG is fast but not stable, smoothsolver is stable but slow.
		fvSolutionFile.write("\n        relTol            0.01;") # I want it to be quite fast. So I use PBiCG. But it blows up! But smoothsolver runs smoothly!
		fvSolutionFile.write("\n    }")
		######### STEADY AND TURBULENT ##########
		if self.timeDerivative == "steady" and self.flowType == "RAS": # for potenfialFoam when using a steady state RAS model
			fvSolutionFile.write("\n\n    Phi")
			fvSolutionFile.write("\n    {")
			fvSolutionFile.write("\n        $p;")
			fvSolutionFile.write("\n    }")
		########## UNSTEADY (LAMINAR OR RAS) ##########
		if self.timeDerivative == "unsteady":
			fvSolutionFile.write("\n\n    pFinal")
			fvSolutionFile.write("\n    {")
			fvSolutionFile.write("\n        $p;")
			fvSolutionFile.write("\n        relTol          0;")
			fvSolutionFile.write("\n    }")
			fvSolutionFile.write("\n\n    \"(U|nuTilda|k|epsilon|omega)Final\"")
			fvSolutionFile.write("\n    {")
			fvSolutionFile.write("\n        $U;")
			fvSolutionFile.write("\n        relTol          0;")
			fvSolutionFile.write("\n    }")
			fvSolutionFile.write("\n\n    \"pcorr.*\"") 
			fvSolutionFile.write("\n    {")
			fvSolutionFile.write("\n        $p;")
			fvSolutionFile.write("\n        tolerance       0.02;")
			fvSolutionFile.write("\n        relTol          0;")
			fvSolutionFile.write("\n    }")
		fvSolutionFile.write("\n}")
		##############################
		# SIMPLE/POTENTIAL OR PIMPLE #
		##############################
		if self.timeDerivative == "steady":
			fvSolutionFile.write("\n\nSIMPLE")
			fvSolutionFile.write("\n{")
			fvSolutionFile.write("\n    // SIMPLE pressure-velocity algorithm controls")
			fvSolutionFile.write("\n    nNonOrthogonalCorrectors    2;")
			if self.consistent == "no":
				fvSolutionFile.write("\n    consistent                  no;")
			elif self.consistent == "yes":
				fvSolutionFile.write("\n    consistent                  yes;")
			fvSolutionFile.write("\n\n    residualControl")
			fvSolutionFile.write("\n    {")
			fvSolutionFile.write("\n        p                              1e-5;")
			fvSolutionFile.write("\n        U                              1e-5;")
			fvSolutionFile.write("\n        \"(nuTilda|k|epsilon|omega)\"    1e-5;")
			fvSolutionFile.write("\n    }")
			fvSolutionFile.write("\n}")
			if self.flowType == "RAS":
				fvSolutionFile.write("\n\npotentialFlow")
				fvSolutionFile.write("\n{")
				fvSolutionFile.write("\n    // Potential flow algorithm controls")
				fvSolutionFile.write("\n    nNonOrthogonalCorrectors    10;")
				fvSolutionFile.write("\n}")
		elif self.timeDerivative == "unsteady":
			fvSolutionFile.write("\n\nPIMPLE")
			fvSolutionFile.write("\n{")
			fvSolutionFile.write("\n    // PIMPLE pressure-velocity algorithm controls")
			fvSolutionFile.write("\n    nNonOrthogonalCorrectors    2;")
			fvSolutionFile.write("\n    nCorrectors                 2;")
			fvSolutionFile.write("\n    nOuterCorrectors            100;")
			if self.consistent == "no":
				fvSolutionFile.write("\n    consistent                  no;")
			elif self.consistent == "yes":
				fvSolutionFile.write("\n    consistent                  yes;")
			fvSolutionFile.write("\n    pRefCell                    0;")
			fvSolutionFile.write("\n    pRefValue                   0;")
			fvSolutionFile.write("\n    turbOnFinalIterOnly         yes;")
			fvSolutionFile.write("\n\n    residualControl")
			fvSolutionFile.write("\n    {")
			fvSolutionFile.write("\n        p")
			fvSolutionFile.write("\n        {")
			fvSolutionFile.write("\n            tolerance       1e-4;")
			fvSolutionFile.write("\n            relTol          0;")
			fvSolutionFile.write("\n        }")
			fvSolutionFile.write("\n        U")
			fvSolutionFile.write("\n        {")
			fvSolutionFile.write("\n            tolerance       1e-4;")
			fvSolutionFile.write("\n            relTol          0;")
			fvSolutionFile.write("\n        }")
			fvSolutionFile.write("\n        \"(nuTilda|k|epsilon|omega)\"")
			fvSolutionFile.write("\n        {")
			fvSolutionFile.write("\n            tolerance       1e-4;")
			fvSolutionFile.write("\n            relTol          0;")
			fvSolutionFile.write("\n        }")
			fvSolutionFile.write("\n    }")
			fvSolutionFile.write("\n}")
		######################
		# RELAXATION FACTORS #
		######################
		### NON CONSISTENT ###
		if self.consistent== "no":
			fvSolutionFile.write("\n\nrelaxationFactors")
			fvSolutionFile.write("\n{")
			fvSolutionFile.write("\n    //Relaxation factors per field and equation (Inconsistent Algorithm)")
			fvSolutionFile.write("\n    fields")
			fvSolutionFile.write("\n    {")
			fvSolutionFile.write("\n        p    0.3;")
			fvSolutionFile.write("\n    }")
			fvSolutionFile.write("\n    equations")
			fvSolutionFile.write("\n    {")
			fvSolutionFile.write("\n        U                              0.7;")
			fvSolutionFile.write("\n        \"(nuTilda|k|epsilon|omega)\"    0.7;")
			fvSolutionFile.write("\n    }")
			fvSolutionFile.write("\n}")
		#### CONSISTENT ####
		elif self.consistent == "yes":
			fvSolutionFile.write("\n\nrelaxationFactors")
			fvSolutionFile.write("\n{")
			fvSolutionFile.write("\n    //Relaxation factors per equation (Consistent Algorithm)")
			fvSolutionFile.write("\n    equations")
			fvSolutionFile.write("\n    {")
			fvSolutionFile.write("\n        U                              0.9;")
			fvSolutionFile.write("\n        \"(nuTilda|k|epsilon|omega)\"    0.8;")
			fvSolutionFile.write("\n    }")
			fvSolutionFile.write("\n}")
		#########
		# CACHE #
		#########
		fvSolutionFile.write("\n\ncache")
		fvSolutionFile.write("\n{")
		fvSolutionFile.write("\n    grad(U);")
		fvSolutionFile.write("\n}")
		fvSolutionFile.write("\n\n// ******************************************************************* //")