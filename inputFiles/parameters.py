########################################################################################################################
# Engine Parameters (Exhaust gas composition and Chamber Temperature can be calculated with NASA CEA)
########################################################################################################################

# Data input choice ('F' for File, 'M' for Manual)
ceaDataSource = 'F'

# Name of CEA data input file (CEA-Settings: T in Kelvin, P in Bar, Mole Fractions)
ceaDataFileName = 'inputFiles/ceainput.txt'
# Input definition ('mole' for mole fraction, 'mass' for massfraction)
exhaustCompositionRatioType = 'mole'

# Manual Definition of Chamber Temperature
chamberTemperature = 2870.81  # K
# Manual Definition of Chamber Pressure
chamberPressure = 25 * 10 ** 5  # Pa
# Manual definition of exhaust gas composition, Input: Substancename:Massfraction/Molefraction
exhaustComposition = {  'H2O': 2.3579 * 10 ** -1,
						'CO2': 5.5019 * 10 ** -2,
						'CO': 1.7712 * 10 ** -1,
						'Oxygen': 0,
						'Nitrogen': 4.3 * 10 ** -1,
						'Hydrogen': 1.0656 * 10 ** -1,
						'Methane': 0,
						'NH3': 0}

# Fuel
fuelType = "Ethanol"
# Oxidizer
oxidizerType = "N2O"
# Mixture Ratio (O/F Mass)
oxidizerFuelRatio = 3.4

# Ambient Pressure
ambientPressure = 10 ** 5  # Pa
# Optimal expansion altitude ratio (hoptimal/hmax)
overexpansionRatio = 0.333

# Engine Thrust at ambient pressure
seaLevelThrust = 500  # N
# Burntime
burnDuration = 8  # s
# Combustion Chamber Velocity
chamberVelocity = 40  # m/s
# Ispcorrection (1 for standard, scaling factor in case of reduced isp)
ispCorrectionFactor = 1

# Nozzle Simulation Cell Numbers
nozzleSimCellCount = 50  # Nodimension


########################################################################################################################
# Tank Parameters
########################################################################################################################

# Tank Diameter
tankDiameter = 0.09  # m

# Tank (and other stuff) Mass Arrangement (from bottom to top, for fueltank: 'F', for oxidizer: 'O','C' for Coax, mass in kg for other)
massArrangement = (2, 'O', 0.9, 'F', 0.8)  # kg
# Tank (and other stuff) Length Arrangement (from bottom to top, for fueltank: 'F', for oxidizer: 'O','C' for Coax, length in m for other)
lengthArrangement = (0.3, 'O', 0.35, 'F', 0.3)  # m

# Tank type ('c' for carbon, 'a' for aluminium)
tankType = 'a'

# Reference Carbon Tank Diameter
referenceCarbonTankDiameter = 0.20  # m
# Reference Carbon Tank mass per length
referenceCarbonTankMassPerLength = 2.5  # kg/m
# Density Carbon
carbonDensity = 1600  # kg/m^3

# Aluminium Tank Endcap Mass
aluminiumTankEndcapMass = 0.25  # kg
# Aluminium Yield Strength
aluminiumYieldStrength = 310 * 10 ** 6  # Pa
# Density Aluminium
aluminiumDensity = 2810  # kg/m^3
# Aluminium Tank Safety Factor
aluminiumTankSafetyFactor = 2
# Aluminium Tank minimum wall thickness
aluminiumTankMinWallThickness = 0.002

# Dead Fuel Mass Fraction
deadFuelMassFraction = 0.05
# Dead Oxidiser Mass Fraction
deadOxidizerMassFraction = 0.05
# Dead Propellant Conditions ('g' for gaseous,'l' for liquid)
deadOxidizerState = 'g'
deadFuelState = 'l'

# Propellant Storage Conditions
fuelTankTemperature = 25 + 273.15  # K
fuelTankPressure = 30 * 10 ** 5  # Pa
oxidizerTankTemperature = 25 + 273.15  # K
oxidizerTankPressure = 50 * 10 ** 5  # Pa
oxidizerTankGasFraction = 0


########################################################################################################################
# Input Data Settings
########################################################################################################################

# Name of OpenRocket output file
orDataFileName = "inputFiles/pressuredata.csv"
# Data Strip Factor (Rawdatapoints/Outputdatapoints)
orDataStripFactor = 15


########################################################################################################################
# Output Data Settings
########################################################################################################################

# Output File Name
engineFileName = 'outputFiles/Amalia_8s.rse'
# Rocket Engine Name
engineName = 'Amalia 8s'
# Producer
engineManufacturer = 'TXV'
# Displayed System Diameter
displayedSystemDiameter = 0.1  # m
# Automatic Mass Calculation
automaticMassCalculation = 0
