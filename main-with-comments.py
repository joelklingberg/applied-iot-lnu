import machine # Import of library "machine" which it used to read data from A0 and pins on the pycom board
from time import sleep # Sleep when that is used, e.g. between every loop
from machine import Pin # Pins that are being used for the LED lights
adc = machine.ADC() # ADC are being used with machine, to read data from A0
sensor = adc.channel(pin='P15', attn=machine.ADC.ATTN_11DB) # Reads from pin 15 on the pycom board
p_out_green = Pin('P9', mode=Pin.OUT) # P9 where the green LED light is connected to the pycom board
p_out_orange = Pin('P10', mode=Pin.OUT) # P10 where the orange LED light is connected to the pycom board
p_out_red = Pin('P11', mode=Pin.OUT) # P11 where the red LED light is connected to the pycom board
def blink(): # 10 loops (blinks) if else is reached, then all LED:s blinks with 1 sec pause between blinks
    for _ in range(10):
        p_out_green.value(1)
        p_out_orange.value(1)
        p_out_red.value(1)
        sleep(1)
        p_out_green.value(0)
        p_out_orange.value(0)
        p_out_red.value(0)
        sleep(1)
def read_sensor(sensor):
    # Take multiple readings and take the average to get a more reliable reading
    print("Moisture value: {0}" .format(sensor())) # 0 is being replaced with the sensor value
    READING_DELAY_IN_S = 1 # Reading delay in one second
    NUM_READINGS = 10 # Number of readings (10)
    total = 0 # The sum of all readings
    for i in range(0, NUM_READINGS): # Do 10 sensor readings, return the average value
        sleep(READING_DELAY_IN_S) # One second sleep between every reading
        sensor_reading = sensor() # Grabs the sensor value
        print('Moisture value: {0}'.format(sensor())) #Prints every sensor value in the loop
        total += sensor_reading # Total variable (first 0), then sum with its pre value
    average_reading = int(total/NUM_READINGS) # All read values divided by number of readings (i.e 10)
    print("Average moisture: {0}" .format(sensor())) # Prints average read sensor value
    return average_reading # Returns the average reading
def check_plant(sensor_reading): # Defintions of break points values from the soil moist sensor
    LOW_VALUE = 1000
    HIGH_VALUE = 2000
    if sensor_reading >= LOW_VALUE and sensor_reading <= HIGH_VALUE: # If value is between 1000-2500, print text below and activate green LED
        print("Woooa! Perfect, between {0}-{1} is the target range, you have green fingers my old friend!".format(LOW_VALUE, HIGH_VALUE))
        p_out_green.value(1)
        p_out_orange.value(0)
        p_out_red.value(0)
    elif LOW_VALUE > sensor_reading: # If value is below 1000, print text below and activate yellow LED
        print("Hmm! Below {0} is too wet, drink the water instead of poring it over your flowers, else you will get blisters on your fingers.".format(LOW_VALUE))
        p_out_orange.value(1)
        p_out_red.value(0)
        p_out_green.value(0)
    elif HIGH_VALUE < sensor_reading: # If value is over 2500, print text below and activate red LED
        print("Ooof! Over {0} is perhaps too dry, you should water your poor flowers.".format(HIGH_VALUE))
        p_out_red.value(1)
        p_out_green.value(0)
        p_out_orange.value(0)
    else: # If an error is suspected, blink all LED lights and print text below
        print("Man, This is a tricky one, it might be a bit too dry or a bit too wet, or something spooky's happening. I have no idea what you should do.")
        blink()
while True: # Continue as long as true, with 5 seconds paus between every loop
    average_reading = read_sensor(sensor)
    pybytes.send_signal(2, average_reading)
    check_plant(average_reading) #Check plant average reading
    sleep(5)