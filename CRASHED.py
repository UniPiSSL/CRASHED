#!/usr/bin/python3

import csv

EnterpriseAttacksFile = 'enterprise_capec.csv'
ICSAttacksFile = 'ics_capec.csv'
MobileAttacksFile = 'mobile_capec.csv'

def LoadComponents():
	Components = []
	with open('components.csv',  newline='') as f:
		reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
		for row in reader:
			Components.append(row)
		return Components	

def ImportImpactScores():
	Impacts = []
	with open('impact_scores.csv', newline='') as f:
		reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
		for row in reader:
			Impacts.append(row)
	return Impacts

def ImportImpactInfo():
	ImpactInfo = []
	with open('impact_info.csv', newline='') as f:
		reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
		for row in reader:
			ImpactInfo.append(row)
	return ImpactInfo

def LoadAttacks(file):
	Attacks = []
	with open(file, newline='') as f:
		reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
		for row in reader:
			tactics = row[2].split(",")			
			for tactic in tactics:
				temp = []
				temp = row
				temp[2] = tactic.replace("[","").replace("]","").replace(" ","").replace("'","").replace('"','')
				Attacks.append(list(temp))
	return Attacks

def WriteToFile(outputData, filename):
	with open(filename, 'w') as f:
		f.write(outputData)

def MatchVulnerabilities(capecid):

	vulnerabilities = ""

	with open('capec.csv', newline='') as f:
		reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
		for row in reader:
			if capecid in row[0]:
				vulnerabilities = row[3]
				break				
	
	return vulnerabilities

def GetVulnerabilities(input_string):	

	lstVulnerabilities = []
	
	if input_string != "[]":
		elements = input_string[1:-1].split(",")
		output_list = list(elements)    
		
		for item in output_list:
			capecId = item[7:-1]
			vulnerabilities = MatchVulnerabilities(capecId)
			if vulnerabilities != "":
				lstVulnerabilities.append(vulnerabilities)

	return lstVulnerabilities

def MatchLikelihood(capecid):
    
	retString = ""
	retValue = 0
	
	with open('capec.csv', newline='') as f:
		reader = csv.reader(f, delimiter=';', quoting=csv.QUOTE_NONE)
		for row in reader:
			if capecid in row[0]:
				retString = row[2]
				break	
	
	if retString == "":
		retValue = 0
	elif retString == "Low": 
		retValue = 0.25
	elif retString == "Medium": 
		retValue = 0.5
	elif retString == "High": 
		retValue = 0.75
	
	return retValue  

def CalculateMedian(values):
    # Sort the list of values
    sorted_values = sorted(values)
    
    # Find the number of elements in the list
    n = len(sorted_values)
    
    # Find the median
    if n % 2 == 0:
        # If even, average the two middle numbers
        median = (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2
    else:
        # If odd, take the middle number
        median = sorted_values[n//2]
    
    return median

def GetLikelihood(input_string):

	totalLikehood = 0	
	
	if input_string == "[]":
		return 0
    
	elements = input_string[1:-1].split(",")
	output_list = list(elements)   

	likelihood_list = []
	
	for item in output_list:
		capecId = item[7:-1]
		likelihood = MatchLikelihood(capecId)
		likelihood_list.append(likelihood)
		
	totalLikehood = CalculateMedian(likelihood_list)
	
	return totalLikehood

def GetImpact(i, comp, ImpactScores, ImpactInfo, Matrix):	

	ImpactScore = 0

	Cyber_Factor = 1
	Physical_Factor = 1
	DirectConsequences_Factor = 1
	UserExperiences_Factor = 1
	Emotional_Factor = 1

	Cyber_Criticality_Index = 1
	Physical_Criticality_Index = 2
	DirectConsequences_Criticality_Index = 3
	UserExperience_Criticality_Index = 4
	Emotional_Criticality_Index = 5	

	Cyber_Criticality_CounterSubCategories = 0
	Physical_Criticality_CounterSubCategories = 0
	DirectConsequences_Criticality_CounterSubCategories = 0
	UserExperience_Criticality_CounterSubCategories = 0
	Emotional_Criticality_CounterSubCategories = 0
	
	for impactCategory in ImpactInfo:
		if impactCategory[0] == "Cyber":
			Cyber_Criticality_CounterSubCategories = int(impactCategory[1])
			W_Cyber = float(impactCategory[2].replace(",", "."))
		elif impactCategory[0] == "Physical":
			Physical_Criticality_CounterSubCategories = int(impactCategory[1])
			W_Physical = float(impactCategory[2].replace(",", "."))
		elif impactCategory[0] == "DirectConsequences":
			DirectConsequences_Criticality_CounterSubCategories = int(impactCategory[1])
			W_DirectConsequences = float(impactCategory[2].replace(",", "."))
		elif impactCategory[0] == "UserExperience":
			UserExperience_Criticality_CounterSubCategories = int(impactCategory[1])
			W_UserExperience = float(impactCategory[2].replace(",", "."))
		elif impactCategory[0] == "Emotional":
			Emotional_Criticality_CounterSubCategories = int(impactCategory[1])
			W_Emotional = float(impactCategory[2].replace(",", "."))
		else:
			print("error")

	if Matrix == "ICS" and "impact" in i[2] and i[1] == "Damage to Property":				

		W_Cyber = 0.2
		W_Physical =  0.2
		W_DirectConsequences = 0.4
		W_UserExperience = 0.1
		W_Emotional = 0.1

	elif Matrix=="ICS" and "impact-ics" in i[2] and i[1]== "Loss of Availability":

		W_Cyber = 0.4
		W_Physical =  0.2
		W_DirectConsequences = 0.2
		W_UserExperience = 0.1
		W_Emotional = 0.1

	elif Matrix=="Mobile" and "impact" in i[2] and i[1]== "Data Encrypted for Impact":		

		W_Cyber = 0.4
		W_Physical =  0.2
		W_DirectConsequences = 0.2
		W_UserExperience = 0.1
		W_Emotional = 0.1

	elif Matrix=="Enterprise" and "impact" in i[2] and (i[1]== "Data Encrypted for Impact" or i[1]==  "Defacement" or i[1]=="Internal Defacement" or i[1]=="External Defacement"):		

		W_Cyber = 0.4
		W_Physical =  0.2
		W_DirectConsequences = 0.2
		W_UserExperience = 0.1
		W_Emotional = 0.1

	elif Matrix=="Enterprise" and "impact" in i[2] and (i[1]== "Data Destruction" or i[1]== "Data Manipulation" or  i[1]== "Disk Wipe" or i[1]== "Disk Content Wipe" or i[1]== "Disk Structure Wipe" or i[1]== "Runtime Data Manipulation" or i[1]== "Stored Data Manipulation" or i[1]== "Runtime Data Manipulation"  or i[1]=="Transmitted Data Manipulation"):

		W_Cyber = 0.4
		W_Physical =  0.2
		W_DirectConsequences = 0.2
		W_UserExperience = 0.1
		W_Emotional = 0.1

	elif Matrix=="Mobile" and "network-effects" in i[2] and i[1]== "Manipulate Device Communication":

		W_Cyber = 0.4     # Manupilation affects the Integrity
		W_Physical =  0.2
		W_DirectConsequences = 0.2
		W_UserExperience = 0.1
		W_Emotional = 0.1

	elif Matrix=="Mobile" and "remote-service-effects" in i[2] and i[1]== "Remotely Wipe Data Without Authorization":

		W_Cyber = 0.4     # Manupilation affects the Integrity
		W_Physical =  0.2
		W_DirectConsequences = 0.2
		W_UserExperience = 0.1
		W_Emotional = 0.1

	elif Matrix=="ICS" and "execution-ics" in i[2]:

		W_Cyber = 0.2     
		W_Physical =  0.4  # execution affects P-UA Unathorized Actuation, P-IA incorrect actuation
		W_DirectConsequences = 0.2
		W_UserExperience = 0.1
		W_Emotional = 0.1

	elif Matrix=="Enterprise" and "impact" in i[2] and (i[1]== "Account Access Removal" or i[1]==  "Resource Hijacking"):

		W_Cyber = 0.4     # resource hijacking impact availability, account access removal may impact access to accounts
		W_Physical =  0.2
		W_DirectConsequences = 0.2
		W_UserExperience = 0.1
		W_Emotional = 0.1

	elif Matrix=="ICS" and "impact-ics" in i[2] and (i[1]== "Loss of Productivity and Revenue" or i[1]=="Loss of Safety"):		

		W_Cyber = 0.3     # loss of productivy and revenue through diruption and even damage to availability and integrity
		W_Physical =  0.2
		W_DirectConsequences = 0.3  # loss of revenue
		W_UserExperience = 0.1
		W_Emotional = 0.1

	elif Matrix=="Enterprise" and "impact" in i[2] and (i[1]== "Endpoint Denial of Service" or  i[1]== "Firmware Corruption" or i[1]==  "Inhibit System Recovery" or  i[1]== "Network Denial of Service" or i[1]=="Service Stop" or i[1]=="System Shutdown/Reboot" or i[1]== "Direct Network Flood" or i[1]=="Reflection Amplification" or i[1]=="OS Exhaustion Flood" or i[1]=="Service Exhaustion Flood" or i[1]=="Application Exhaustion Flood" or i[1]=="Application or System Exploitation" ):

		W_Cyber = 0.4     # Endpoint Denial of Service impact availability, denial of Service and all types of flood impact cyber
		W_Physical =  0.2
		W_DirectConsequences = 0.2 
		W_UserExperience = 0.1
		W_Emotional = 0.1	

	elif Matrix=="ICS" and "inhibit-response-function" in i[2]:

		W_Cyber = 0.2
		W_Physical =  0.2
		W_DirectConsequences = 0.4 # inhibit-response-function tries to prevent your safety, protection, quality assurance & operation intervetion
		W_UserExperience = 0.1
		W_Emotional = 0.1	

	elif Matrix=="Mobile" and "network-effects" in i[2] and i[1]== "Jamming or Denial of Service":

		W_Cyber = 0.4     #  Denial of Service impacts Cyber-Availability (C-A)
		W_Physical =  0.2
		W_DirectConsequences = 0.2 
		W_UserExperience = 0.1
		W_Emotional = 0.1	

	elif Matrix=="Mobile" and "impact" in i[2] and i[1]== "Delete Device Data":

		W_Cyber = 0.4     #  Delete Device Data impacts Cyber-Integrity and Cyber-Availability (C-I and C-A)
		W_Physical =  0.2
		W_DirectConsequences = 0.2 
		W_UserExperience = 0.1
		W_Emotional = 0.1			

	elif Matrix=="Mobile" and "network-effects" in i[2] and i[1]== "Downgrade to Insecure Protocols":

		W_Cyber = 0.2     #  Downgrade to Inssecure = Adversary-in-the-Middle --> C-C, C-I,
		W_Physical =  0.1   # P-BPP
		W_DirectConsequences = 0.2  # DC-F, DC-I, DC-LC
		W_UserExperience = 0.1 # UX-N1
		W_Emotional = 0.4 # E-A, E-AT, E-B, E-Ex, E-SF

	elif Matrix=="Mobile" and "execution" in i[2]:

		W_Cyber = 0.3 
		W_Physical =  0.2
		W_DirectConsequences = 0.3
		W_UserExperience = 0.1
		W_Emotional = 0.1 

	elif Matrix=="Enterprise" and "execution" in i[2]:

		W_Cyber = 0.3 
		W_Physical =  0.2
		W_DirectConsequences = 0.3
		W_UserExperience = 0.1
		W_Emotional = 0.1 

	elif Matrix=="Mobile" and "network-effects" in i[2] and (i[1]== "Rogue Cellular Base Station" or i[1]=="Rogue Wi-Fi Access Points"):

		W_Cyber = 0.3  # C-C, C-I, C-A
		W_Physical =  0.2   # P-BPP, P-UA, P-IA, P-DA, P-PA
		W_DirectConsequences = 0.3 # DC-F, DC-V, DC-S, DC-P, DC-LC, DC-I
		W_UserExperience = 0.1 # UX-N1, UX-N2, UX-NN
		W_Emotional = 0.1 # E-A, E-AT, E-B, E-E, E-SF

	elif Matrix=="Mobile" and "impact" in i[2] and i[1]== "SMS Control":

		W_Cyber = 0.3 
		W_Physical =  0.2
		W_DirectConsequences = 0.3
		W_UserExperience = 0.1
		W_Emotional = 0.1 

	elif Matrix=="Mobile" and "network-effects" in i[2] and i[1]== "SIM Card Swap":

		W_Cyber = 0.3 
		W_Physical =  0.3
		W_DirectConsequences = 0.2
		W_UserExperience = 0.1
		W_Emotional = 0.1 

	elif Matrix=="Mobile" and "impact" in i[2] and i[1]== "Clipboard Modification" :

		W_Cyber = 0.3  
		W_Physical =  0
		W_DirectConsequences = 0.3 
		W_UserExperience = 0
		W_Emotional = 0.4

	elif Matrix=="Mobile" and "impact" in i[2] and i[1]==  "Device Lockout":

		W_Cyber = 0.2
		W_Physical =  0
		W_DirectConsequences = 0.4 
		W_UserExperience = 0
		W_Emotional = 0.4

	elif Matrix=="Mobile" and "impact" in i[2] and  i[1]== "Input Injection":

		W_Cyber = 0.3  
		W_Physical =  0.2
		W_DirectConsequences = 0.3 
		W_UserExperience = 0
		W_Emotional = 0.3

	elif Matrix=="Mobile" and "network-effects" in i[2] and i[1]== "Exploit SS7 to Redirect Phone Calls/SMS":

		W_Cyber = 0.2
		W_Physical =  0
		W_DirectConsequences = 0.4
		W_UserExperience = 0
		W_Emotional = 0.4

	elif Matrix=="ICS" and "impact-ics" in i[2] and i[1]== "Manipulation of Control":

		W_Cyber = 0.2
		W_Physical =  0.3
		W_DirectConsequences = 0.3
		W_UserExperience = 0
		W_Emotional = 0.2

	elif Matrix=="ICS" and "impair-process-control" in i[2]:

		W_Cyber = 0.2
		W_Physical =  0.2
		W_DirectConsequences = 0.2
		W_UserExperience = 0.2
		W_Emotional = 0.2

	elif Matrix=="ICS" and "impact-ics" in i[2] and (i[1]== "Denial of Control" or  i[1]== "Loss of Control"):

		W_Cyber = 0.2
		W_Physical =  0.2
		W_DirectConsequences = 0.4
		W_UserExperience = 0
		W_Emotional = 0.2

	elif Matrix=="ICS" and "collection" in i[2]:

		W_Cyber = 0.2
		W_Physical =  0.2
		W_DirectConsequences = 0.2
		W_UserExperience = 0.2
		W_Emotional = 0.2

	elif Matrix=="Mobile" and "collection" in i[2]:

		W_Cyber = 0.2
		W_Physical =  0.2
		W_DirectConsequences = 0.2
		W_UserExperience = 0.2
		W_Emotional = 0.2

	elif Matrix=="Enterprise" and "collection" in i[2]:

		W_Cyber = 0.2
		W_Physical =  0.2
		W_DirectConsequences = 0.2
		W_UserExperience = 0.2
		W_Emotional = 0.2

	elif Matrix=="Mobile" and "network-effects" in i[2] and i[1]== "Exploit SS7 to Track Device Location":	

		W_Cyber = 0.2
		W_Physical =  0.1
		W_DirectConsequences = 0.4
		W_UserExperience = 0
		W_Emotional = 0.3

	elif Matrix=="Mobile" and "remote-service-effects" in i[2] and i[1]== "Remotely Track Device Without Authorization": 

		W_Cyber = 0.3
		W_Physical =  0
		W_DirectConsequences = 0.4
		W_UserExperience = 0
		W_Emotional = 0.3

	elif Matrix=="Enterprise" and "exfiltration" in i[2]:

		W_Cyber = 0.2
		W_Physical =  0.2
		W_DirectConsequences = 0.2
		W_UserExperience = 0.2
		W_Emotional = 0.2

	elif Matrix=="ICS" and "impact-ics" in i[2] and i[1]== "Theft of Operational Information":

		W_Cyber = 0.3
		W_Physical =  0.1
		W_DirectConsequences = 0.4
		W_UserExperience = 0
		W_Emotional = 0.2

	elif Matrix=="Mobile" and "exfiltration" in i[2]:

		W_Cyber = 0.2
		W_Physical =  0.2
		W_DirectConsequences = 0.2
		W_UserExperience = 0.2
		W_Emotional = 0.2

	elif Matrix=="Mobile" and "network-effects" in i[2] and i[1]== "Eavesdrop on Insecure Network Communication":

		W_Cyber = 0.3
		W_Physical =  0.1
		W_DirectConsequences = 0.3
		W_UserExperience = 0
		W_Emotional = 0.3	

	elif Matrix=="Mobile" and "remote-service-effects" in i[2] and i[1]== "Obtain Device Cloud Backups":

		W_Cyber = 0.4
		W_Physical =  0.1
		W_DirectConsequences = 0.3
		W_UserExperience = 0
		W_Emotional = 0.2			

	elif Matrix=="Mobile" and "impact" in i[2] and i[1]== "Carrier Billing Fraud":

		W_Cyber = 0.4
		W_Physical =  0.1
		W_DirectConsequences = 0.4
		W_UserExperience = 0
		W_Emotional = 0.1

	elif (Matrix=="Enterprise" or Matrix=="Mobile")  and (("defense-evasion" in i[2]) or ("persistence" in i[2]) or ("privilege-escalation" in i[2])):		

		W_Cyber = 0.4
		W_Physical =  0
		W_DirectConsequences = 0.4
		W_UserExperience = 0
		W_Emotional = 0.2			

	elif (Matrix=="Enterprise" or Matrix=="Mobile")  and (("command-and-control" in i[2]) or ("credential-access" in i[2]) or ("discovery" in i[2]) or ("initial-access" in i[2]) or ("lateral-movement" in i[2])):

		W_Cyber = 0.4
		W_Physical =  0.2
		W_DirectConsequences = 0.4
		W_UserExperience = 0
		W_Emotional = 0

	elif Matrix=="ICS" and (("command-and-control-ics" in i[2]) or ("discovery-ics" in i[2]) or ("initial-access" in i[2]) or ("lateral-movement-ics" in i[2])): 

		W_Cyber = 0.4
		W_Physical =  0.2
		W_DirectConsequences = 0.4
		W_UserExperience = 0
		W_Emotional = 0	

	elif Matrix=="ICS" and (("evasion-ics" in i[2]) or ("persistence-ics" in i[2])):

		W_Cyber = 0.4
		W_Physical =  0
		W_DirectConsequences = 0.3
		W_UserExperience = 0
		W_Emotional = 0.3

	elif Matrix=="Mobile" and "impact" in i[2] and (i[1]== "Generate Fraudulent Advertising Revenue" or i[1]==  "Manipulate App Store Rankings or Ratings"): 

		W_Cyber = 0.5
		W_Physical =  0
		W_DirectConsequences = 0.5
		W_UserExperience = 0
		W_Emotional = 0

	else: 

		W_Cyber = 0.2
		W_Physical =  0.2
		W_DirectConsequences = 0.2
		W_UserExperience = 0.2
		W_Emotional = 0.2

	for Index in ImpactScores:

		if comp[1] == Index[0]:
			
			Cyber_Criticality = float(Index[Cyber_Criticality_Index].replace(",", ".")) / \
				                Cyber_Criticality_CounterSubCategories
			Physical_Criticality = float(Index[Physical_Criticality_Index].replace(",", ".")) / \
				                Physical_Criticality_CounterSubCategories
			DirectConsequences_Criticality = float(Index[DirectConsequences_Criticality_Index].replace(",", ".")) / \
				 				DirectConsequences_Criticality_CounterSubCategories
			UserExperience_Criticality = float(Index[UserExperience_Criticality_Index].replace(",", ".")) / \
				 				UserExperience_Criticality_CounterSubCategories
			Emotional_Criticality = float(Index[Emotional_Criticality_Index].replace(",", ".")) / \
				 				Emotional_Criticality_CounterSubCategories

			ImpactScore = W_Cyber * (Cyber_Factor * Cyber_Criticality) + \
				          W_Physical * (Physical_Factor * Physical_Criticality) + \
						  W_DirectConsequences * (DirectConsequences_Factor * DirectConsequences_Criticality) + \
						  W_UserExperience * (UserExperiences_Factor * UserExperience_Criticality) + \
						  W_Emotional * (Emotional_Factor * Emotional_Criticality)

			ImpactScore = round(ImpactScore,4)

	return ImpactScore

def main():	

	Components = []	
	Components = LoadComponents()

	ImpactScores = ImportImpactScores()
	ImpactInfo = ImportImpactInfo()

	Attacks = []
	EnterpriseAttacks = LoadAttacks(EnterpriseAttacksFile)
	ICSAttacks = LoadAttacks(ICSAttacksFile)
	MobileAttacks = LoadAttacks(MobileAttacksFile)
	
	output_details = ""
	output = ""
	Matrix = ''
	devices = 0
	TotalNormalizedRisk = 0

	for comp in Components:
		print()
		print(comp)

		if comp[0] == 'Gadgets and Appliances':
			Attacks = MobileAttacks
			Matrix = 'Mobile'			

		if comp[0] == 'Sensors':
			Attacks = ICSAttacks
			Matrix = 'ICS'

		if comp[0] == 'Electronics and Controllers':
			Attacks = EnterpriseAttacks
			Matrix = 'Enterprise'

		j = 0
		TotalRisk  = 0
		NormalizedRisk = 0		

		for attack in Attacks:
			capecs = attack[13].lstrip().replace(' ', '')
			Likelihood = GetLikelihood(capecs)
			Vulnerabilities = GetVulnerabilities(capecs)
			Impact = GetImpact(attack, comp, ImpactScores, ImpactInfo, Matrix)
			Risk = round(Likelihood * Impact, 4)
			
			TotalRisk = TotalRisk + Risk
					
			if Likelihood != 0: 		
				output_details = output_details + f"{comp[1]} | {comp[0]} | {Matrix} | {attack[1]} | {attack[2]} | {capecs} | {Vulnerabilities} | {Likelihood} | {Impact} | {Risk}" + "\n" 
				j = j +1
			
		TotalRisk = round(TotalRisk,4)
		NormalizedRisk = (TotalRisk * 100 ) / (j * 0.75)
		NormalizedRisk = round(NormalizedRisk, 4)
		TotalNormalizedRisk = TotalNormalizedRisk + NormalizedRisk
		devices = devices + 1

		output = output + f"{comp[0]} | {comp[1]} | {j} | {TotalRisk} | {NormalizedRisk}" + "\n" 

	TotalNormalizedRisk = round(TotalNormalizedRisk, 4)
	RiskSmartHome = (TotalNormalizedRisk*100) / (devices * 100)
	RiskSmartHome = round(RiskSmartHome, 4)

	output = output + f"TotalNormalizedRisk = {TotalNormalizedRisk}" + "\n" 
	output = output + f"Devices = {devices}" + "\n" 
	output = output + f"RiskSmartHome = {RiskSmartHome}" + "\n" 
	
	WriteToFile(output_details, "output_with_details.txt")
	WriteToFile(output, "output.txt")

if __name__ == "__main__":

    main()
