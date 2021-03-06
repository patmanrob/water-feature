# Raspberry Pi controlled Water Feature

<img alt="Water Feature HRG1" title="HRG1" src="https://github.com/patmanrob/water-feature/blob/main/images/IMG_1175.JPG" width="280" />

 Water feature consists of water reservoir, pump, tube and a cascade.

Control consists of Raspberry Pi. 

4 Relays ( 1 for pump and 3 for lights).

2 DS18b20 temperature probes.

1 floating level switch.

The water feature control was written in python and took advantage of the Raspberry Pi's GPIO pins for controling the physical elements,Requests library for interrogating the internet for data, email libraries for sending information and time / datetime libraries for handing the times the water feature operates.


**The HRG1 is named in honour of Heath-Robinson and Rube Goldberg.**  

It's just a water feature but I an working to make it as unnecessarily complicated as possible, in a style similar to both Heath-Robinson and Goldberg.

## Phase 0
Before starting on this project I had already constructed a water feature. It had no control other than plugging the pump in.

## Phase 1
The first phase was to **control the power of the pump via a relay** using a Raspberry Pi.

Once this was achieved a float switch was added to the reservoir, switching the pump off if the water level fell too low and holding it off until the reservior was filled.

## Phase 2
The second phase was **to have the pump operate during set hours** during the day and switching off at night.

This was achieved by hard coding on and off times and comparing to the Raspberry Pi's internal time.

## Phase 3
The third phase was **to have the pump switch on at sunrise.** 

This was initially achieved by hard coding the latitude and longitude of the water feature's location in an API request at statup and once the data had become out of date.

## Phase 4
There was lots of data about different sunrise, sunset and twilight times in the response from the API.

I decided to **add some timed lights to the water feature** which come on at sunset, the end of civil twilight, the end of nautical twilight and the end of astronomical twilight.

## Phase 5
To have an indication of what was happening when away from the computer I **set up email alerts reporting what the water feature was doing.**

Initially every event generated an email but there were a lot. So I added an enable/disable test for the debugging messages.  Low water alerts and new schedules always send.
