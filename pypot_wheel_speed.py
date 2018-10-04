# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 09:41:44 2018

@author: juven
"""

import itertools
import numpy
import time

import pypot.dynamixel

rotation_factor =  60. / (2. * numpy.pi * 1.339) # TODO : adapt value to be exact

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
    
    dxl_io.enable_torque(wheel_ids)
    dxl_io.set_wheel_mode(wheel_ids)    
    
    print('Wheels initialized')



def shutdown_wheels():
    dxl_io.disable_torque(wheel_ids)
    print('Wheels shut down')

def set_wheel_speed(wheel_name, w):
    wheel_speeds[wheel_name] = rotation_factor * w * ((-1)**(1 + wheel_name))
    dxl_io.set_moving_speed({wheel_name : wheel_speeds[wheel_name]})
    
    
def set_wheel_speeds(w):
    wheel_speeds[LEFT_WHEEL] = rotation_factor * w
    wheel_speeds[RIGHT_WHEEL] = -rotation_factor * w
    dxl_io.set_moving_speed(wheel_speeds)
    
        
def increase_wheel_speed(wheel_name, dw):
    wheel_speeds[wheel_name] += rotation_factor * dw * ((-1)**(1 + wheel_name))
    dxl_io.set_moving_speed({wheel_name : wheel_speeds[wheel_name]})


def increase_wheel_speeds(dw):
    wheel_speeds[LEFT_WHEEL] += rotation_factor * dw
    wheel_speeds[RIGHT_WHEEL] -= rotation_factor * dw
    dxl_io.set_moving_speed(wheel_speeds)
    

def get_wheel_speed(wheel_name):
    return ((-1)**(1 + wheel_name)) * wheel_speeds[wheel_name] / rotation_factor
    
