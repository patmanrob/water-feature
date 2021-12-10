#!/usr/bin/python2.7

#import libraries
import requests
import json
from datetime import datetime, time, timedelta
from time import sleep
from gpiozero import LED, CPUTemperature, Button
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#initial constants and variables
from fountainvariables import *
fountain_off=time(23,00,21)
off1=time(23,00,28)
off2=time(23,00,14)
off3=time(23,00,07)
off4=time(23,00,00)
#setup GPIO pins
fountain = LED(fountain_pin,False,False) #set fountain GPIO output pin
light1 = LED(light1_pin,False,False)    #set light1 GPIO output pin
light2 = LED(light2_pin,False,False) #set light 2 GPIO pin
light3 = LED(light3_pin,False,False) #set light 3 GPIO pin
light4 = LED(light4_pin,False,False) #set light4 GPIO pin
water_level=Button(3)       #set water level sensor pin

#function to get probe temperatures
def get_temp(probeID):
    tempfile= open("/sys/bus/w1/devices/"+probeID+"/w1_slave")
    thetext=tempfile.read()
    tempfile.close()
    tempdata = thetext.split("\n") [1].split(" ")[9]
    temp = float(tempdata[2:])
    temp = temp / 1000
    return temp
    
#function to send notification emails
def send_email(body):
    print "\nSending email at " + str(datetime.now()) + " with content:\n" + body
    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = email_send
    msg["Subject"] = "Alert from fountain at " + str(datetime.now())
    msg.attach(MIMEText(body,"plain"))
    text = msg.as_string()
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email_user,email_password)
    server.sendmail(email_user,email_send,text)
    server.quit()
    body=""
    print "email sent successfully\n"


#function to get and parse sunrise-sunset data
def get_todays_data():
    global schedule
    global sunrise
    global status
    global sunrise_time
    global sunset_time
    global civil_time
    global nautical_time
    global astro_time
    print "Requesting data from web"
    r = requests.get(url) #load daylight data
    print "got data from web"
    data = json.loads(r.content)
    #print "Raw data:  "
    #print data
    sunrise = data['results']['sunrise']
    sunset = data['results']['sunset']
    civil = data['results']['civil_twilight_end']
    nautical = data['results']['nautical_twilight_end']
    astro = data['results']['astronomical_twilight_end']
    status = data['status']
    sunrise_time = time(int(sunrise[11:13]), int(sunrise[14:16]))
    sunset_time = time(int(sunset[11:13]), int(sunset[14:16]))
    civil_time = time(int(civil[11:13]), int(civil[14:16]))
    nautical_time = time(int(nautical[11:13]), int(nautical[14:16]))
    astro_time = time(int(astro[11:13]), int(astro[14:16]))
    schedule = "Fountain setup sequence for " +str(sunrise[0:10])
    schedule = schedule + "\nFountain On time = " + str(sunrise_time) + "  Fountain off time = " + str(fountain_off)
    schedule = schedule + "\nLight1 on time = " + str(sunset_time) + "Light1 off time = " + str(off1)
    schedule = schedule + "\nLight2 on time = " + str(civil_time) + "Light2 off time = " + str(off2)
    schedule = schedule + "\nLight3 on time = " + str(nautical_time) + "Light 3 off time = " + str(off3)
    schedule = schedule + "\nLight4 on time = " + str(astro_time) + "Light 4 off time = " + str(off4)
    schedule = schedule + "\nReceived data is " + status

#function to turn devices on
def switch_device_on(device):
    global body
    if not device.is_active:
        print "The " + d_name + " is off"
        device.on()
        print "and I turned the " + d_name +" on at " + str(time_now)
        body = body + "\nThe " + d_name + " was turned on at " + str(time_now)

#function to turn devices off
def switch_device_off(device):
    global body
    if device.is_active:
        print "The " + d_name + " is on"
        device.off()
        print "and I turned the " + d_name + " Off at " + str(time_now)
        body = body + "\nThe " + d_name + " turned off at " +str(time_now)
   
#function to set devices on and off
def on_off(device, on_time, off_time):
    if on_time < time_now and time_now < off_time:
        switch_device_on(device)
    else:
        switch_device_off(device)    
        
#function to get location based on external ip address
def get_url():
    global url
    findip = requests.get(ipapi)                # get fountain's web ip address
    ipdata = json.loads(findip.content)         #parse response 
    ipaddress= ipdata['ip']                     # extract ip address
    findloc = requests.get(latlongapi+ipaddress)#get location from ip
    locdata = json.loads(findloc.content)       #parse response
    lat= locdata['lat']                         #extract latitude
    lon=locdata['lon']                          #extract longitude
    
    print('lat Data ')
    print(lat)
    print('lon Data ')
    print(lon)
    url=url+str(lat)+'&lng='+str(lon)+'&formatted=0'    #create url to query sunrise/sunset data
    print url
    return url
    
#function to startup fountain    
def startup_sequence():
    global url
    #Starup sequence
    print "Startup sequence" #cycle everyting on and off
    fountain.on()
    light1.on()
    light2.on()
    light3.on()
    light4.on()
    print"All on"
    sleep(1)
    fountain.off()
    light1.off()
    light2.off()
    light3.off()
    light4.off()
    print "All off"
    url=get_url() #create url to query sunrise/sunset
    get_todays_data() # query sunrise/sunset and create schedule
    print schedule
    send_email(schedule)
    sleep(1)
    print "Setup complete"

#main loop
if __name__ == "__main__":
    try:
        startup_sequence()
        while True:
            while not water_level.is_pressed:
                print('water level is low')
                d_name="fountain"
                switch_device_off(fountain)
                body="The water level in the fountain is too low!"
                send_email(body)
                water_level.wait_for_press()
            else:
                print('Water Level is good')
            print(water_level.is_pressed)
            #update current time and date
            body = "" #empty email body
            d = datetime.now()
            today_date = d.date()
            time_now = d.time()
            time_now = time_now.replace(microsecond=0) # get rid of microseconds to shorten email lines
            temp1 = get_temp(probe1)
            temp2 = get_temp(probe2)
            

            
            #check for probe 1 (air)temperature change
            if temp1 >= (temp1_old+3):
                body = body + "The Air Probe temperature has risen over 3 c \nOld temperature " + str(temp1_old) + " \nNew Temperature " + str(temp1)
                print "temp 1 up from " + str(temp1_old) + " To " +str(temp1)
                temp1_old = temp1
            else:
                if temp1 <= (temp1_old-3):
                    body = body + "The Air Probe temperature has fallen over 3c\nOld temperature " + str(temp1_old) + " \nNew Temperature " + str(temp1)
                    print "temp 1 down from " + str(temp1_old) + " To " +str(temp1)
                    temp1_old = temp1
    
            #check for probe 2 (Water)temperature change
            if temp2 >= (temp2_old+3):
                body = body + "The Water Probe temperature has risen over 3 c \nOld temperature " + str(temp2_old) + " \nNew Temperature " + str(temp2)
                print "temp 2 up from " + str(temp2_old) + " To " +str(temp2)
                temp2_old = temp2
            else:
                if temp2 <=(temp2_old-3):
                    body = body + "The Water Probe temperature has fallen over 3c\nOld temperature " + str(temp2_old) + " \nNew Temperature " + str(temp2)
                    print "temp 2 down from " + str(temp2_old) + " To " +str(temp2)
                    temp2_old = temp2
    
        
        

            
            # fountain on from sunrise to fountain_off
            d_name="Fountain"
            on_off(fountain, sunrise_time, fountain_off)
            
            # Light 1 on from sunset to off1
            d_name = "Light 1"
            on_off(light1, sunset_time, off1)
            
            # Light 2 on from  civil sunset to off2
            d_name = "Light 2"
            on_off(light2, civil_time, off2)
            
            # Light 3 on from  Nautical sunset to off3
            d_name = "Light 3"
            on_off(light3, nautical_time, off3)
            
            # Light 4 on from Astronomical sunset to off4
            d_name = "Light 4"
            on_off(light4, astro_time, off4)

            #check for out of date sunrise-sunset data and update if neccessary
            if str(sunrise[0:10]) != str(today_date):
                print ("Date has changed")
                get_todays_data()
                body = body + "Data has been renewed\nNew schedule is: \n" + schedule
                send_email(body)

                
            #if there is any text in body email it to user
            if body != "":
                if send:
                    cpu=CPUTemperature()
                    cpu_temp=cpu.temperature
                    body = body + "\nPi Core temperature is " + str(cpu_temp) + " C."
                    body = body + "\nAir Temp is " + str(temp1) + " C."
                    body = body + "\nWater Temp is " + str(temp2) + " C."
                    send_email(body)
                else:
                    print("emails disabled")
                
            #run the loop every 6 seconds
            sleep(6)

    finally:
        fountain.close()
        light1.close()
        light2.close()
        light3.close()
        light4.close()

