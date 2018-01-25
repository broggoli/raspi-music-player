#!/usr/bin/env python

# battery_control.py

# Example python script that uses the LiPoPi circuitry to handle the safe shutdown of
# a Raspberry Pi in response to user request or low battery

# 2016 - Robert Jones - Freely distributed under the MIT license

# based on Daniel Bull's LiPoPi project - https://github.com/NeonHorizon/lipopi

import os
import RPi.GPIO as GPIO
import time

class Battery_Control():

    def __init__(self, pins, shutdown_callback):
        lipopi = {}

        # Specify which GPIO pins to use
        self.low_battery_pin = pins['LOW_BATTERY_PIN']

        self.shutdown_pin = pins['SHUTDOWN_BUTTON_PIN']

        self.logfile = '/home/pi/battery_control.log'  # FULL path to the log file

        self.shutdown_wait = 1  # seconds - how long to wait before actual shutdown - can be 0

        # Configure the GPIO pins
        GPIO.setmode(GPIO.BCM)

        # setup the pin to check the shutdown switch - use the internal pull down resistor
        GPIO.setup(self.shutdown_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # setup the low battery check pin
        GPIO.setup(self.low_battery_pin, GPIO.IN)

        # create a trigger for the shutdown switch and low battery pins

        GPIO.add_event_detect(self.shutdown_pin, GPIO.RISING, callback=shutdown_callback, bouncetime=300)
        GPIO.add_event_detect(self.low_battery_pin, GPIO.FALLING, callback=shutdown_callback, bouncetime=300)