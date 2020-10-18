INFORMATION ABOUT RUNNING SCRIPT:
----------------------------------

* Currently, only set up to work on Windows OS.

* The automation scripts were written in python 3. If you do not have python 3 installed, you will need to install it as
certain functions are only available in python 3. A quick gooogle search on how to install python 3 for windows will provide 
the information you need.
	> To check if you have python installed, go to your windows terminal and type:
		python 
	> This should open python. If nothing or error is invoked, you will need to install python 3. 

* The following modules are required to run:

	- pyautogui 
	- matplotlib 
	- pyperclip
	- pandas
	- os 
	- platform 
	- time 

 > If they are not installed, they can be installed via the following command in 
 your windows terminal:
 	  * pip install MODULE (ex. pip install pyautogui)
 > If that does not work, try the following:
 	  * py -m pip install MODULE 
 > If you do not have pip installed, proceed to the following link to donwload pip:
	  * https://phoenixnap.com/kb/install-pip-windows

* There are two scripts required to produce the .csv files with configuration information: 
	- automation4LISE.py 
	- auto4LISE.py 
	
	automation4LISE.py
	------------------
		> This is the implementation module with all of the functions implemented. 
	auto4LISE.py 
	------------
		> This is the script that calls the implementation module; the "interface".
		
* Once you have the moduled installed, python 3 installed, and 

DATA STORAGE 
------------

* The data is saved in individual .csv files for each corresponding Magnesium isotope in the same folder the scripts are in.
 It is then required from there that the user visually inspects the .csv files to find best compromise between intensity and purity.

* The intermediate files "data.txt" and "pps_data.txt" are files that are created with the sole purpose of being reused. They are 
created when the script is originally executed and keeps being updated corresponding to each isotope. It is safe to delete these 
two files once you are done with the program. 

GENERAL INFORMATION
-------------------

> This folder contains preliminary LISE++ files for optimal configurations using NSCL and FRIB facilities
to study isotopes Mg 32 through Mg 40. 

> All NSCL and FRIB files have been set to dp/p = 1%; at the I2_Slits and the pre-separator focal
plane (O4_PS_FP), respectively.

> To allow for largest intenisty possible on the FRIB LISE++ configuration, the pre-separator 
slits (PS_Wedge_Slits) are set to the aperture limit, 135 mm. Wedges and momentum acceptances were 
later adjusted downstream to yield optimal purity results without large comprimise to intensity.

> All NSCL files have FP_Slits set to 10 mm and have purity greater than 91%.

> All FRIB files have purity greater than 92%. 

> FRIB intensities are all 2-3 orders of magnitude greater than NSCL intensities.  

> For isotopes Mg 38 and Mg 40, there are 2-3 LISE++ files for each isotope. Each file is a 
different compromise on purity and intensity for the corresponding isotope. The intensities 
that are used in the UPDATE presentation are from Mg_40_FRIB_3 and Mg_38_FRIB_3. 

> As of now, an update is ensuing that will work with Linux machines (Mac OS, for example). This will be updated when that is completed. 

> If there are any errors, please contact me at salinas@frib.msu.edu
 

