import machine
from time import sleep
from machine import Pin

adc = machine.ADC()
sensor = adc.channel(pin='P15', attn=machine.ADC.ATTN_11DB)

p_out_green = Pin('P9', mode=Pin.OUT)
p_out_orange = Pin('P10', mode=Pin.OUT)
p_out_red = Pin('P11', mode=Pin.OUT)

def blink():
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
    # take multiple readings and take the average to get a more reliable reading
    print("Moisture value: {0}" .format(sensor()))
    READING_DELAY_IN_S = 1
    NUM_READINGS = 10

    total = 0

    for i in range(0, NUM_READINGS):
        sleep(READING_DELAY_IN_S)
        sensor_reading = sensor()
        print('Moisture value: {0}'.format(sensor()))
        total += sensor_reading

    average_reading = int(total/NUM_READINGS)
    print("Average moisture: {0}" .format(sensor()))
    return average_reading

def check_plant(sensor_reading):
    LOW_VALUE = 1000
    HIGH_VALUE = 2000
    if sensor_reading >= LOW_VALUE and sensor_reading <= HIGH_VALUE:
        print("Woooa! Perfect, between {0}-{1} is the target range, you have green fingers".format(LOW_VALUE, HIGH_VALUE))
        p_out_green.value(1)
        p_out_orange.value(0)
        p_out_red.value(0)
    elif LOW_VALUE > sensor_reading:
        print("Hmm! Below {0} is too wet, drink the water instead of poring it over your flowers".format(LOW_VALUE))
        p_out_orange.value(1)
        p_out_red.value(0)
        p_out_green.value(0)
    elif HIGH_VALUE < sensor_reading:
        print("Ooof! Over {0} is perhaps too dry, you should water your poor flowers".format(HIGH_VALUE))
        p_out_red.value(1)
        p_out_green.value(0)
        p_out_orange.value(0)
    else:
        print("Man, This is a tricky one, it might be a bit too dry or a bit too wet, or something spooky's happening. I have no idea what you should do")
        blink()

while True:
    average_reading = read_sensor(sensor)
    pybytes.send_signal(1, average_reading)
    check_plant(average_reading)
    sleep(5)
