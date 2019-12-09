from inputFiles import parameters
import numpy as np
from CoolProp.CoolProp import PropsSI as ps


def calculateTankCG(mdot, Tlist, mpl):
	CGl = []
	mlist = []
	mges = mdot * parameters.burntime  # Operational Propellant Mass
	mox = mges * (parameters.ofr / (1 + parameters.ofr))  # Operational Oxidizer Mass
	mdox = mdot * (parameters.ofr / (1 + parameters.ofr))  # Oxidizer Massflow
	mf = mges - mox  # Operational Fuel Mass
	mdf = mdot - mdox  # Fuel Mass Flow
	moxt = mox * (1 + parameters.deadof)  # Total Oxidizer Mass
	moxd = moxt - mox  # Oxidizer Dead Mass
	mft = mf * (1 + parameters.deadff)  # Total Fuel Mass
	mfd = mft - mf  # Fuel Dead Mass
	rhoox = ps('D', 'Q', parameters.Qtanko, 'T', parameters.Ttanko, parameters.Oxidizer)  # Oxidizer Density
	rhof = ps('D', 'P', parameters.Ptankf, 'T', parameters.Ttankf, parameters.Fuel)  # Fuel Density
	Atank = 0.25 * np.pi * parameters.dt ** 2  # Tank Area
	Voxt = moxt / rhoox  # Total Oxidizer Volume
	Vft = mft / rhof  # Total Fuel Volume
	ltox = Voxt / Atank  # Oxidizer Tank Length
	ltf = Vft / Atank  # Fuel Tank Length
	print(ltf, ltox)
	moxtank = ltox * mpl  # Oxidizer Tank Dry Mass
	mftank = ltf * mpl  # Fuel Tank Dry Mass
	if parameters.cox == 'l':  # Definition of Dead Mass Distribution (Even for gaseous, bottom for fluid)
		mox = moxt
	elif parameters.cox == 'g':
		moxtank += moxd
	else:
		print('cox input error')
	if parameters.cf == 'l':
		mf = mft
	elif parameters.cf == 'g':
		mftank += mfd
	else:
		print('cf input error')
	dist = 0  # Calculation of Dry Mass CG
	cgfrac = 0
	mdry = 0
	caf = 1
	cao = 1
	for n, i in enumerate(parameters.mar):
		if i == 'O':
			vmass = moxtank
			vlength = ltox
			vlox = dist  # distance to Oxidizer Tank Bottom
		elif i == 'F':
			vmass = mftank
			vlength = ltf
			vlf = dist  # distance to Fuel Tank Bottom
		elif i == 'C':  # Calculatin Coax Tank Assembly
			Di = np.sqrt((parameters.dt ** 2) / (1 + Vft / Voxt))
			l = Voxt / (0.25 * np.pi * Di ** 2)
			ma = l * parameters.mtl
			mi = l * parameters.mpl(Di)
			mgt = ma + mi
			vmass = mgt
			vlength = l
			vlf = dist
			vlox = dist
			cao = (np.pi * 0.25 * Di ** 2) / Atank
			caf = ((np.pi) * 0.25 * ((parameters.dt ** 2) - (Di ** 2))) / Atank
		else:
			vmass = i
			vlength = parameters.lar[n]
		cgfrac += vmass * (dist + vlength * 0.5)
		dist += vlength
		mdry += vmass
	ltot = dist  # Total Tank Length
	ml = mdry + mox + mf
	for i in Tlist:  # Generation of propellant mass list during operation
		mlist.append((ml - i * mdot) * 1000)
	cgdry = cgfrac / mdry
	for i in Tlist:  # Calculation of CG shift during operation
		moxs = mox - i * mdox
		lsox = (moxs / rhoox) / (Atank * cao)
		mfs = mf - i * mdf
		lsf = (mfs / rhof) / (Atank * caf)
		cgfrac = mdry * cgdry + moxs * (vlox + lsox * 0.5) + mfs * (vlf + lsf * 0.5)
		mt = mdry + moxs + mfs
		cgt = ltot - (cgfrac / mt)
		CGl.append(cgt)
	return CGl, mlist, ltot, ml, mdry