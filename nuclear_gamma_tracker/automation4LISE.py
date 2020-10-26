import time
import pyautogui as pag  
import matplotlib.pyplot as plt
import pyperclip as pc 
import pandas as pd 
import numpy as np
import csv
import os 
import platform 

"""
Roy Salinas
Module to control automation in LISE++ with NSCL configuration

Purpose: To retrive particular parameters from LISE++ such as beam intensity,
beam purity, wedge thickness, wedge angle, momentum acceptance, focal
plane slit width, and Image 2 slit width. 

All beam data comes from NSCL website: https://nscl.msu.edu/users/beams.html

Python version: 3.7.1 

Currently, this is set up to only works with a Windows OS.

"""

#path = os.path.expanduser("~\Desktop")
#print(path)

#check what system you are using
""""
useros = platform.system()
if useros == "Linux":
	print("Using a Linux OS...")
	desktop = os.path.expanduser("~/Desktop")
	print(f"Your desktop path is: {desktop}")
elif useros == "Windows":
	print("Using a Windows OS...")
	home = os.path.expanduser('~') #find your home directory 
	desktop = home + "\Desktop"
	print(f"Your desktop path is {desktop}")

"""
pag.PAUSE=1
pag.FAILSAFE=True
width, height = pag.size()
print(f"Scren size is: {width},{height}")


#put the path to my desktop to reduce amounts of click
def txt2csv(path): 
	with open(path, 'r') as in_file:
		stripped = (line.strip() for line in in_file)	#get rid of any spaces (by default)
		lines = (line.split() for line in stripped if line) 
		with open('junk.csv', 'w') as out_file:
			writer = csv.writer(out_file)
			writer.writerows(lines) #write each line


"""
pixel locations for each isotope based on my screen (Resolution: 1920x1080)

Note: This can be improved to contain images of the isotope that appears on the screen. Doing this rids the dependence 
on one's screen resolution and local pixel coordinates.

"""
pixel_locations = { "Mg_32":{"x":1121,"y":626},"Mg_33":{"x":1116,"y":626},\
"Mg_34":{"x":1116,"y":626} ,"Mg_35":{"x":1116,"y":626},"Mg_36":{"x":1136,"y":626},\
"Mg_37":{"x":1116,"y":626},"Mg_38":{"x":1116,"y":626},"Mg_40":{"x":1106,"y":626}}


"""
An array of dictionaries (c++ maps). "data" is the key for the corresponding isotope and its value is an array of data. 
Using zeros as place holders for intialization. 

"""
#array of maps, data is the key to the map, replace the zero's with arrays of data
#isotppe is one of the keys, data is the other key for that map with their corresponding values
isotope_info = [ \
{"isotope":"Mg_32", "data":0.0}, \
{"isotope":"Mg_33","data":0.0},  \
{"isotope":"Mg_34","data":0.0},  \
{"isotope":"Mg_35","data":0.0},  \
{"isotope":"Mg_36","data":0.0},  \
{"isotope":"Mg_37","data":0.0},  \
{"isotope":"Mg_38","data":0.0},  \
{"isotope":"Mg_40","data":0.0}   ]

#dictionary of dictionary
beam_info = {"O_16": {"Energy":150,"Intensity":175}, "O_18":{"Energy":120,"Intensity":150},\
"Ne_20": {"Energy":170,"Intensity":80},"Ne_22":{"Energy":150,"Intensity":100},  \
"Mg_24":{"Energy":170,"Intensity":60},"Si_28":{"Energy":160,"Intensity":10},   \
"S_32" : {"Energy":150,"Intensity":60}, "Ar_36":{"Energy":150,"Intensity":75}, \
"Ca_40":{"Energy":140,"Intensity":50}, "Ca_48":{"Energy":90,"Intensity":15},   \
"Ca_48":{"Energy":140,"Intensity":80}, "Ni_58":{"Energy":160,"Intensity":20},\
"Ni_64":{"Energy":140,"Intensity":7}, "Ge_76":{"Energy":130,"Intensity":25}
}


#Didn't include the rest of the beam list, intensity was too low to be significant.
"""
,   \
"Se_82":{"Energy":140,"Intensity":45}, "Kr_78":{"Energy":150,"Intensity":25},  \
"Kr_86":{"Energy":100,"Intensity":15},"Zr_96":{"Energy":120,"Intensity":3},    \
"Mo_92":{"Energy":140,"Intensity":10}, "Sn_112":{"Energy":120,"Intensity":4},  \
"Sn_124":{"Energy":120,"Intensity":1.5} #incomplete but enough for our purposes
 } 

"""


def _isotope_start():
	isotope_start= input("Which isotope would you like to start with? (Enter as 'Mg_32' for example.): ")
	print(f"Starting with {isotope_start}...")
	return isotope_start

def _isotope_end():
	isotope_end= input("Which isotope would you like to end with? (Enter as 'Mg_36' for example.): ")
	print(f"Ending with {isotope_end}...")
	return isotope_end

"""
If program is not open, look for the program image on deskotp, and click on it. 

Note: Could improve by having it go directly to the LISE++.exe file and executing it. Could do this 
with a shell script or here (in the python script).

"""

#to set beam
def set_projectile(projectile_name,energy,intensity,A):
	print("Setting projectile...")
	pag.moveTo(16,124) #projectile button 
	pag.click()
	pag.moveTo(262,213) #element text box
	pag.doubleClick()
	pag.write(projectile_name)
	pag.moveTo(231,211) # The mass number box
	pag.doubleClick()
	pag.write(str(A))
	pag.moveTo(519,213) #energy
	pag.doubleClick()
	pag.write(str(energy))
	pag.moveTo(523,421) #beam intensity 
	pag.doubleClick()
	pag.write(str(intensity))
	pag.moveTo(269,445)
	pag.click()
	time.sleep(1)

#to set the Focal Plane (FP) slits
def set_FP_slits(slit_width):
	print("Setting FP_Slits...")
	pag.moveTo(65,684) #move to slit button 
	pag.click()
	pag.moveTo(764,231)
	pag.click()
	pag.write(str(slit_width))
	pag.moveTo(238,447)
	pag.click()
	pag.moveTo(71,744)
	pag.click()

#to set the wedge thickness 
def set_I2_wedge(wedge_thickness):
	print("Setting I2_wedge...")
	pag.moveTo(60,461) #move to wedge button 
	pag.click()
	pag.write(str(wedge_thickness))
	pag.moveTo(926,223) #set spectrometer after block
	pag.click()
	time.sleep(2)
	pag.moveTo(397,398) #select wedge profile
	pag.click()
	pag.moveTo(881,394) #move to calculate angle 
	pag.click()
	time.sleep(10) #wait 
	pag.moveTo(371,479) #fit achromatic angle from LISE calc.
	pag.click()
	pag.moveTo(308,530) #select the angle and copy 
	pag.doubleClick()
	pc.copy("")
	time.sleep(2)
	pag.hotkey('ctrl','c') #done twice due to bug in not properly copying. This fixes that bug.
	time.sleep(1)
	pag.hotkey('ctrl','c')
	angle = pc.paste()
	pag.moveTo(168,622) #ok button 
	pag.click()
	pag.moveTo(152,535)
	pag.click()
	print(f"The angle for the wedge is -{angle}.")
	return str(angle)

def tune_spectrometer():
	print("Tuning spectrometer...")
	pag.moveTo(335,78)
	pag.click()
	time.sleep(1)

def set_fragment(fragment,A):
	print("Setting fragment...")
	pag.moveTo(20,170) #projectile button 
	pag.click()
	pag.moveTo(250,463) #element text box
	pag.doubleClick()
	#pag.press("delete")
	pag.write(str(A))
	pag.moveTo(309,470) #element text box
	pag.doubleClick()
	#pag.press("delete")
	pag.write(fragment)
	pag.moveTo(624,521) #energy
	pag.click()
	time.sleep(1)

#to retrive the thickness 
def get_thickness():
	target_thickness = 0
	pc.copy("") #clear clipboard
	print("Retrieving thickness...")
	pag.moveTo(453,38) #calculations 
	pag.click()
	pag.dragTo(504, 151,.5) #Optimum target
	time.sleep(.6)
	pag.moveTo(381,485) # first ok 
	pag.click()
	pag.moveTo(326,655) # second ok 
	pag.click()
	time.sleep(20)
	pag.moveTo(260,451) #load thickness
	pag.click()
	pag.moveTo(1629,160) #exit first plot
	pag.click()
	pag.moveTo(1600,93) #exit second plot
	pag.click()
	pag.moveTo(24,196) #target button 
	pag.click()
	pag.moveTo(477,286) #box containing info 
	time.sleep(1)
	pag.doubleClick()
	time.sleep(1)
	pag.hotkey('ctrl' , 'c') #copy 
	time.sleep(1)
	target_thickness = pc.paste() #paste it to a variable 
	print(f"Thickness is {target_thickness} microns")
	"""
	for i,m in enumerate(isotope_info):
		if isotope_info[i]["isotope"] == isotope_select:
			isotope_info[i]["thickness"] = s
			iso_name, iso_t = isotope_info[i]["isotope"] , isotope_info[i]["thickness"]
			print(iso_name,iso_t)
	"""
	pag.moveTo(456,459) #ok button to close
	pag.click()
	return target_thickness 

#to retrive intensity
def get_intensity(isotope,beam_element,beam_mass):
	flag = False
	print(isotope)
	#get pixel location of isotope on screen
	print("Retrieving intensity...")
	x = pixel_locations[isotope]["x"]
	y = pixel_locations[isotope]["y"]
	#print(x,y)
	pag.position()
	pag.moveTo(x,y)
	pag.click(button="right")
	pag.moveTo(1483,417) #File save button 
	pag.click()

	"""
	pag.moveTo(532,121) #drop down 
	pag.click()
	#pag.press("d",presses=2,interval=1) #to save in desktop
	pag.press("d",interval=1) #to save in desktop
	pag.press("enter")
	"""
	pag.moveTo(531,339) #file save text box
	pag.click()
	filename = str(desktop) + "\data.txt" #desktop comes from top of the sript.
	print(f"The file is being saved at the following location: {filename}")
	pag.write(filename)
	#pag.write("junk.txt")
	pag.press("enter")
	pag.press("left")
	pag.press("enter") #this "enter" saves the file to desktop
	pag.moveTo(1563,44)
	pag.click()
	df = pd.read_csv(filename)
	#df = pd.read_csv("C:\\Users\Owner\Desktop\junk.txt") #path to temporary file. NEED TO UPDATE 
	#print(df)
	intensity_check=df.iloc[0,0]  #location of the intensity in the data frame. Usually included an extra line if it is zero
	intensity_check = intensity_check.split()
	print(intensity_check)
	if len(intensity_check) == 6:
		if intensity_check[5] == "0!":
			print("TRANSMISSION IS 0.0% WITH THIS PROJECTILE ")
			flag = True
			return 0,flag 
	else: 
		_intensity=df.iloc[6,0] #location of the intensity in the data frame 
		_intensity=_intensity.split()
		print(f"The intensity for {isotope} with {beam_element} {beam_mass} is {_intensity[4]}.") #intensity value
		return _intensity[4],flag

#retrieve the transmission in X-space 
def FP_slit_X_transmission_percent():
	#NEED TO WORK ON THIS
	print("Getting FP_Slits X space transmission...")
	filename = str(desktop) + "\data.txt" #desktop comes from top of the sript.
	df = pd.read_csv(filename)
	FP_x_space_transmission = df.iloc[39,0] #location in the .csv file
	FP_x_space_transmission = FP_x_space_transmission.split()
	#print(FP_x_space_transmission[4])
	return FP_x_space_transmission[4] #percent value 

def purity_percent(fragment_isotope):
	print(f"Retrieving beam purity for {fragment_isotope}...")
	pag.moveTo(832,83) #run all nucleo buttom (red lightning bolt)
	pag.click()
	time.sleep(40)
	pag.moveTo(999,77) #x spatial distribution 
	pag.click()
	pag.dragTo(1110, 629,.5) #FP_PIN detector
	pag.click(interval=.5) 
	time.sleep(4)
	pag.moveTo(14,316) #stats box
	pag.click()
	pag.press("enter") #accept
	time.sleep(1)
	pag.moveTo(1609,201) #file save button
	pag.click()
	"""
	pag.moveTo(365,195) #drop down 
	pag.click()
	#pag.press("d",presses=2,interval=1) #to save in desktop
	pag.press("d",interval=1) #to save in desktop
	pag.press("enter")
	"""
	pag.moveTo(389,413) #file save text box
	pag.click()

	filename = str(desktop) + "\pps_data.txt" #desktop comes from top of the sript.
	print(f"The file is being saved at the following location: {filename}")
	pag.write(filename)

	#pag.write("pps_junk.txt")
	pag.press("enter") #save file
	pag.press("left")
	pag.press("enter") #this "enter" saves the file to desktop
	pag.moveTo(1682,122)
	pag.click()
	pag.moveTo(1877,13)
	pag.click()
	df = pd.read_csv(filename,error_bad_lines=False)
	#df = pd.read_csv("C:\\Users\Owner\Desktop\pps_junk.txt",error_bad_lines=False) #path to temporary file. NEED TO UPDATE
	print(f"Size of data frame is {df.size}.")
	_string = df.iloc[5,0] #get the pps for isotope in question
	_string = _string.split()
	isotope_fragment = _string[13] #grab pps value
	total = 0.
	for i in range(5,df.size): 
		string = df.iloc[i,0]
		string = string.split()
		val = float(float(string[13])) #to get it to correct scientific notation
		total = total + val
	print(f"The total amount of pps is {total}.")
	frag_val = float(float(isotope_fragment))
	print(f"Percent of {fragment_isotope} in beam is {(float(float(frag_val))/total)*100.} %")
	percent =(float(float(frag_val))/total)*100.
	return percent

#This loop is used to find the best beam for each isotope. However, it has already been determined that the best beam is Ca 48.
def isotope_loop():
	beam_data = []
	start = time.time()
	df = pd.DataFrame(None) #create our data frame
	for i,dic in enumerate(isotope_info): #loop for fragments
		df = df[0:0]
		df = pd.DataFrame(columns=["Beam element","A (u)","Beam energy (MeV/u)","Beam Intensity (pnA)","Target thickness (microns)","Fragment Intensity (pnA)"])
		data = [] 
		iso=dic['isotope'].replace("_"," ") #get rid of the underscore in the isotope name
		print(f"You are looking at the {iso} isotope.")  #returns the name of the isotope
		iso = iso.split()
		set_fragment(iso[0],iso[1]) #fragment name, mass number
		for i,beam_element in enumerate(beam_info): #now loop for all the provided beams
			print(f"You are using {beam_element} as your primary beam at {beam_info[beam_element]['Energy']} MeV/u with {beam_info[beam_element]['Intensity']} pnA.")
			beam_energy= beam_info[beam_element]["Energy"]
			beam_intensity=beam_info[beam_element]["Intensity"]
			beam_element=beam_element.replace("_"," ")
			beam_element=beam_element.split()
			if beam_element[1] <= iso[1]:
				print(f"Skipping {beam_element[0]} {beam_element[1]}. Not greater than {iso[1]} nucleons.")
				continue
			#				name, energy, intensity, mass number A
			set_projectile(beam_element[0],beam_energy,beam_intensity,beam_element[1])
			thickness = get_thickness() #thickness with that particular beam for a particular fragment 
			tune_spectrometer()
			frag_intensity,flag = get_intensity(dic['isotope'],beam_element[0],beam_element[1]) #pass the isotope name to get intensity and save it to the map with the frag info
			if flag == True:
				continue
			print(f"Data being appended in the following format -> beam element, A,beam energy, beam intensity, thickness, fragment intensity: {beam_element[0]},{beam_element[1]} ,{beam_energy},{beam_intensity},{thickness}, {frag_intensity}")
			df.loc[i] = [beam_element[0],beam_element[1],beam_energy,beam_intensity,thickness,frag_intensity]
			print(df)
		print(f"DATA FRAME FOR {iso[0]} {iso[1]} ISOTOPE.")
		print(df)
		df.to_csv(f"{iso[0]}_{iso[1]}_data_LISE++.csv")
		print(f"File saved as: {iso[0]}_{iso[1]}_data_LISE++.csv")
	end = time.time()
	print(f"It took {end-start} to run everything.")



#to "slice" an array of dictionaries and return slided array  
def slice_array(arr,start):
	new_array = []
	index =0
	for i,dic in enumerate(arr):
		temp_dic = arr[i] #grab individual dictionary in that specific array index
		if temp_dic["isotope"] == str(start): #if starting isotope is found, save the index location
			index =i
			break
	for t in range(index,len(arr)):
		new_array.append(arr[t])
	return new_array #return a sliced array containing dictionaries from starting isotope

#function to find the best configuration using a Ca 48 beam
def isotope_tuning_values(FP_slit_width,isotope_start,isotope_end,wedge_range):
	set_projectile("Ca",140,80,48) #set the beam here with element name, energy, intensity, atomic number 
	start = time.time()
	set_FP_slits(FP_slit_width)
	#if bool_value == True: #if you want to start from  a particular isotope
	new_isotope_dic = slice_array(isotope_info,isotope_start)
	for i,dic in enumerate(new_isotope_dic): #loop for each fragment
		df = pd.DataFrame(None) #create our data frame
		df = pd.DataFrame(columns=["I_2 slit width (mm) ","Intensity (pps) ","Target thickness (microns) ","Horizontal FP Slit width (mm)","Purity transmission % ","Mom. Accpetance % ", "Wedge thickness (microns) ","wedge angle (mrad)"])
		iso=dic['isotope'].replace("_"," ") #get rid of the underscore in the isotope name
		print(f"You are looking at the {iso} isotope.")  #returns the name of the isotope
		iso = iso.split()
		set_fragment(iso[0],iso[1])
		#wedge_thickness = 2300 #wedge thickness to start with 
		for count,wedge_thickness in enumerate(wedge_range): #loop over each wedge thickness
			print(f"Currently using {wedge_thickness} microns for {iso[0]} {iso[1]}")
			tune_spectrometer()
			preliminary_wedge_angle = set_I2_wedge(str(wedge_thickness))	# There is a dependence between target and wedge. Doing it twice gives best results 
			tune_spectrometer()
			preliminary_target_thickness = get_thickness()
			tune_spectrometer()
			wedge_angle = set_I2_wedge(str(wedge_thickness))
			wedge_angle = "-" + wedge_angle					
			tune_spectrometer()
			target_thickness = get_thickness()
			tune_spectrometer()
			frag_intensity,flag = get_intensity(dic['isotope'],"Ca",48) #pass the isotope name to get intensity and save it to the map with the frag info
			if flag == True: #if we have zero transmission, skip that wedge thickness
				continue
			#FP_x_space_transmission = FP_slit_X_transmission_percent()
			_purity_percent = purity_percent(iso[0] + iso[1]) #pass in the name of the fragment isotope
			print(f"Purity is {_purity_percent}")
			df.loc[count] = [29.5,frag_intensity,target_thickness,FP_slit_width,_purity_percent,1,wedge_thickness,wedge_angle] #harcode the 1% momentum acceptance
			wedge_thickness=wedge_thickness+100
			print(f"Have gone through {count} iterations")
			print(df)
		df.to_csv(f"{iso[0]}_{iso[1]}_finetune_{FP_slit_width}_data_LISE++.csv")
		print(f"File saved as: {iso[0]}_{iso[1]}_finetune_{FP_slit_width}_data_LISE++.csv")
		del df 
		if(dic['isotope'] == isotope_end):
			print(f"YOU HAVE REACHED {isotope_end}!")
			break
	end = time.time()
	print(f"It took {(end-start)/60.0} minutes to run everything.")

def save():
	with open("thickness.txt","w") as file:
		file.write(json.dumps(isotope_info))
	file.close()

#python 3 version 
def show_pixels():
	print('Press Ctrl-C to quit.')
	try:
		while True:
			x, y = pag.position()
			positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
			print(positionStr, end='')
			print('\b' * len(positionStr), end='', flush=True)
	except KeyboardInterrupt:
		print('\n')
    
    
   
  