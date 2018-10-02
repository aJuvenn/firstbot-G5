# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 09:41:44 2018

@author: juven
"""

import itertools
import numpy
import time

import pypot.dynamixel

AMP = 10
FREQ = 15.

rotation_factor =  60. / (2. * numpy.pi * 1.339)

LEFT_WHEEL = 1
RIGHT_WHEEL = 2
wheel_speeds = {LEFT_WHEEL : 0. , RIGHT_WHEEL : 0.}

wheel_ids = [LEFT_WHEEL, RIGHT_WHEEL]
dxl_io = 0

def init_wheels():
    
    global dxl_io  
    
    ports = pypot.dynamixel.get_available_ports()
    
    if len(ports) == 0:
        raise IOError('No port was found')
    
    dxl_io = pypot.dynamixel.DxlIO(ports[0])
    
    ids = dxl_io.scan([LEFT_WHEEL, RIGHT_WHEEL])

    if len(ids) != 2:
        raise IOError('Not exactly two wheels were found')
    
    dxl_io.enable_torque(wheel_ids) # I don't know what it means
    dxl_io.set_wheel_mode(wheel_ids)    
    
    print('Wheels initialized')



def shutdown_wheels():
    set_wheel_speed(LEFT_WHEEL, 0.)
    set_wheel_speed(RIGHT_WHEEL, 0.)


def set_wheel_speed(wheel_name, v):
    wheel_speeds[wheel_name] = rotation_factor * v
    dxl_io.set_moving_speed(wheel_speeds)
    
    
def increase_wheel_speed(wheel_name, dv):
    wheel_speeds[wheel_name] += rotation_factor * dv

def get_wheel_speed(wheel_name):
    return wheel_speeds[wheel_name]
    

     
     
init_wheels()     
t0 = time.time()

while True:
    t = time.time()
    if (t - t0) > 10:
        break
    
    v = AMP*numpy.sin(FREQ * (t - t0))
    set_wheel_speed(LEFT_WHEEL, v)
    set_wheel_speed(RIGHT_WHEEL, -v)

    time.sleep(0.02)

shutdown_wheels()