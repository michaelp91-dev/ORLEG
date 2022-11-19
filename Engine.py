from math import sqrt, pi
from engcoolprop.ec_fluid import EC_Fluid
from rocketcea.blends import makeCardForNewTemperature
from rocketcea.cea_obj_w_units import CEA_Obj
from rocketcea.cea_obj import add_new_fuel

g0 = 9.81


class Engine(object):
    def __init__(
        self,
        name,
        fuelType,
        fuelTemperature,
        oxidizerType,
        oxidizerTemperature,
        oxidizerFuelRatio,
        chamberPressure,
        referenceAmbientPressure,
        referenceThrust,
        engineEfficiency,
        waterFraction=0.0,
        contractionRatio=2.5,
    ):
        self.name = name
        self.fuelType = fuelType
        self.fuelTemperature = fuelTemperature
        self.oxidizerType = oxidizerType
        self.oxidizerTemperature = oxidizerTemperature
        self.oxidizerFuelRatio = oxidizerFuelRatio
        self.chamberPressure = chamberPressure
        self.referenceAmbientPressure = referenceAmbientPressure
        self.referenceThrust = referenceThrust
        self.engineEfficiency = engineEfficiency

        if fuelType == "EthanolWater":  # TODO: use cea.newFuelBlend()?
            card_str = (
                """
			fuel C2H5OH(L)   C 2 H 6 O 1   wt%="""
                + str(100.0 - waterFraction)
                + """
			h,cal=-66370.0     t(k)=298.15
			fuel water   H 2 O 1   wt%="""
                + str(waterFraction)
                + """
			h,cal=-68308.0     t(k)=298.15     rho,g/cc = 0.9998
			"""
            )
            add_new_fuel("EthanolWater", card_str)

        # set fuel temperature, see https://rocketcea.readthedocs.io/en/latest/temperature_adjust.html
        fuelStd = EC_Fluid(symbol=self.fuelType)
        fuelStd.setProps(
            T=536.7, Q=0
        )  # FIXME only correct for liquid storable fluids, others use boiling point as std temp
        fuel = EC_Fluid(symbol=self.fuelType)
        fuel.setProps(T=self.fuelTemperature * 9 / 5, Q=0)
        dT = fuel.T - fuelStd.T
        dH = fuel.H - fuelStd.H
        CpAve = abs(dH / dT)
        self.fuelCard = makeCardForNewTemperature(
            ceaName=self.fuelType, newTdegR=fuel.T, CpAve=CpAve, MolWt=16.04
        )

        # same for oxidizer
        oxidizerStd = EC_Fluid(symbol=self.oxidizerType)
        oxidizerStd.setProps(
            T=536.7, Q=0
        )  # FIXME only correct for liquid storable fluids, others use boiling point as std temp
        oxidizer = EC_Fluid(symbol=self.oxidizerType)
        oxidizer.setProps(T=self.oxidizerTemperature * 9 / 5, Q=0)
        dT = oxidizer.T - oxidizerStd.T
        dH = oxidizer.H - oxidizerStd.H
        CpAve = abs(dH / dT)
        self.oxidizerCard = makeCardForNewTemperature(
            ceaName=self.oxidizerType, newTdegR=oxidizer.T, CpAve=CpAve, MolWt=16.04
        )

        self.cea = CEA_Obj(
            oxName=self.oxidizerCard,
            fuelName=self.fuelCard,
            useFastLookup=0,
            makeOutput=0,
            fac_CR=contractionRatio,
            isp_units="m/sec",
            cstar_units="m/sec",
            pressure_units="Pa",
            temperature_units="K",
            sonic_velocity_units="m/sec",
            enthalpy_units="J/kg",
            density_units="kg/m^3",
            specific_heat_units="J/kg-K",
        )

        self.areaRatio = self.cea.get_eps_at_PcOvPe(
            Pc=self.chamberPressure,
            MR=self.oxidizerFuelRatio,
            PcOvPe=(self.chamberPressure / self.referenceAmbientPressure),
        )

        self.exhaustVelocity = self.getExhaustVelocity()

        self.referenceIsp = self.exhaustVelocity / g0

        self.massFlowRate = self.referenceThrust / self.exhaustVelocity

        self.fuelMassFlowRate = self.massFlowRate / (self.oxidizerFuelRatio + 1)

        self.oxMassFlowRate = (
            self.massFlowRate / (self.oxidizerFuelRatio + 1) * self.oxidizerFuelRatio
        )

        self.combustionTemperature = self.cea.get_Tcomb(
            self.chamberPressure, self.oxidizerFuelRatio
        )
        self.cStar = (
            self.cea.get_Cstar(self.chamberPressure, self.oxidizerFuelRatio)
            * self.engineEfficiency
        )  # FIXME: improve?

        throatArea = self.massFlowRate * self.cStar / self.chamberPressure
        self.throatDiameter = 2 * sqrt(throatArea / pi)
        self.nozzleDiameter = 2 * sqrt(throatArea * self.areaRatio / pi)

    def printParameters(self):
        print(f"")
        print(f"Engine Input Parameters:")
        print(f"    Name: {self.name}")
        print(f"    fuelType: {self.fuelType}")
        print(f"    oxidizerType: {self.oxidizerType}")
        print(f"    oxidizerFuelRatio: {self.oxidizerFuelRatio}")
        print(f"    chamberPressure: {self.chamberPressure / 1e5} bar")
        print(f"    referenceThrust: {self.referenceThrust} N")
        print(
            f"    referenceAmbientPressure: {self.referenceAmbientPressure / 1e5} bar"
        )
        print(f"    engineEfficiency: {self.engineEfficiency}")
        print(f"Engine Output Parameters:")
        print(f"    throatDiameter: {self.throatDiameter * 1000:.1f} mm")
        print(f"    nozzleDiameter: {self.nozzleDiameter * 1000:.1f} mm")
        print(f"    areaRatio: {self.areaRatio:.2f}")
        print(f"    combustionTemperature: {self.combustionTemperature:.1f} K")
        print(f"    c*: {self.cStar:.1f} m/s")
        print(f"    referenceIsp: {self.referenceIsp:.1f} s")
        print(f"    massFlow: {self.massFlowRate:.3f} kg/s")
        print(f"    fuelMassFlow: {self.fuelMassFlowRate * 1e3:.2f} g/s")
        print(f"    oxidizerMassFlow: {self.oxMassFlowRate * 1e3:.2f} g/s")

    def getExhaustVelocity(
        self, ambientPressure=None, oxidizerFuelRatio=None, chamberPressure=None
    ):
        if ambientPressure is None:
            ambientPressure = self.referenceAmbientPressure
        if oxidizerFuelRatio is None:
            oxidizerFuelRatio = self.oxidizerFuelRatio
        if chamberPressure is None:
            chamberPressure = self.chamberPressure

        (ve, expansionMode) = self.cea.estimate_Ambient_Isp(
            chamberPressure, oxidizerFuelRatio, self.areaRatio, ambientPressure
        )
        if expansionMode == "Separated":
            print("WARNING: Flow separation in nozzle!")

        ve *= self.engineEfficiency  # FIXME: improve?

        return ve

    def getThrust(
        self,
        ambientPressure=None,
        massFlowRate=None,
        oxidizerFuelRatio=None,
        chamberPressure=None,
    ):
        if massFlowRate is None:
            massFlowRate = self.massFlowRate
        if chamberPressure is None:
            chamberPressure = (
                self.cStar * massFlowRate / ((self.throatDiameter / 2) ** 2 * pi)
            )

        return massFlowRate * self.getExhaustVelocity(
            ambientPressure, oxidizerFuelRatio, chamberPressure
        )
