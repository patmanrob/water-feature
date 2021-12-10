email_user = "[User name for email to be sent]"		#user name for account emails will be sent from		
email_password = "[Password for email to be sent]"	#password for account emails will be sent from
email_send = "[email to send to]"			#address notification emails will be sent to
ipapi="[url]"						#url for api to return WAN IP address
latlongapi="[url]"					#url for api to return latitude/longitude from WAP IP address
url = "[url]"						#first part of url construct to retrieve sunrise/sunset data from
send= True 						#True to send notification emails

probe1="28-xxxxxxxxxxxx"				#id of DS18B20 temperature probe 1
probe2="28-xxxxxxxxxxxx"				#id of DS18B20 temperature probe 2
fountain_pin = 26					#GPIO pin number fountain relay is controlled by
light1_pin = 6						#GPIO pin number light 1 is controlled by
light2_pin = 13						#GPIO pin number light 2 is controlled by
light3_pin = 19						#GPIO pin number light 3 is controlled by
light4_pin = 22						#GPIO pin number light 4 is controlled by
float_pin = 3						#GPIO pin number for float switch

body=""							#empty string for email body to be stored in
temp1=0							#global variable for temp 1
temp1_old=0						#global variable for previous temp 1
temp2=0							#global variable for temp 2
temp2_old=0						#global variable for previous temp 2
