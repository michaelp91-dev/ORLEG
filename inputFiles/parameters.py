# ENGINE GENERATOR INPUT FILE

# NOZZLE INPUT DATA (Exhaust gas composition and Chamber Temperature can be calculated with NASA CEA)

# Data input choice ('F' for File, 'M' for Manual)
datainput = 'F'

# Name of CEA data input file (CEA-Settings: T in Kelvin, P in Bar, Mole Fractions)
ceainput = 'inputFiles/ceainput.txt'
# Input definition ('mole' for mole fraction, 'mass' for massfraction)
ratioflag = 'mole'

# Manual Definition of Chamber Temperature
Tch = 2870.81  # K
# Manual Definition of Chamber Pressure
Pch = 25 * 10 ** 5  # Pa
# Manual definition of exhaust gas composition, Input: Substancename:Massfraction/Molefraction
sw = {  'H2O': 2.3579 * 10 ** -1,
		'CO2': 5.5019 * 10 ** -2,
		'CO': 1.7712 * 10 ** -1,
		'Oxygen': 0,
		'Nitrogen': 4.3 * 10 ** -1,
		'Hydrogen': 1.0656 * 10 ** -1,
		'Methane': 0,
		'NH3': 0}

# Fuel
Fuel = "Ethanol"
# Oxidizer
Oxidizer = "N2O"
# Mixture Ratio (O/F Mass)
ofr = 3.4

# Ambient Pressure
Ps = 10 ** 5  # Pa
# Optimal expansion altitude ratio (hoptimal/hmax)
overexp = 0.333

# Engine Thrust at ambient pressure
Thrust = 5000  # N
# Burntime
burntime = 30  # s
# Combustion Chamber Velocity
vch = 40  # m/s
# Ispkorection (1 for standard, scaling factor in case of reduced isp)
ispkor = 1

# NOZZLE SIMULATION SETUP

# Cell Numbers
cells = 50  # Nodimension

# INPUT DATA PROCESSING

# Name of OpenRocket output file
inputfile = "inputFiles/pressuredata.csv"
# Data Strip Factor (Rawdatapoints/Outputdatapoints)
stripfactor = 15

# CGDETERMINATION
# Tankdiameter
dt = 0.20  # m
# Tankstructuremass per unit length for reference diameter
mtlref = 2.5  # kg/m
# Referencediameter
dtref = 0.20
# Density Carbon
rhoc = 1600  # kg/m^3
# Dead Propellant Mass Fraction
deadff = 0.05
# Dead Oxidiser Mass Fraction
deadof = 0.05
# Systemarrangement mass (from bottom to top, for fueltank: 'F', for oxidizer: 'O','C' for Coax)
mar = (1, 3.5, 'O', 'F', 3.5)  # kg
# Systemarrangement length (from bottom to top, for fueltank: 'F', for oxidizer: 'O','C' for Coax)
lar = (0.41, 0.3, 'O', 'F', 0.3)  # m
# Propellant Storage Conditions
Ttankf = 25 + 273.15  # K
Ptankf = 30 * 10 ** 5  # Pa
Ttanko = 25 + 273.15  # K
Qtanko = 0
Ptanko = 50 * 10 ** 5  # Pa
# Deadpropellantcondition ('g' for gaseous,'l' for liquid)
cox = 'g'
cf = 'l'

# OUTPUT DATA PROCESSING

# Output File Name
outputfile = 'outputFiles/Amalia.rse'
# Rocket Engine Name
Enginename = 'Amalia'
# Producer
Prod = 'TXV'
# Displayed System Diameter
Ddis = 0.1  # m
# Autocalcmass
am = 0