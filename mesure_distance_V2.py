# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 10:21:18 2018

@author: Vincent
"""

import itertools
import numpy
import time
import sys
import select

import pypot.dynamixel

from numpy import sin, cos, sqrt, pi

AMP = 10
FREQ = 15.

rotation_factor =  60. / (2. * numpy.pi * 1.339)

LEFT_WHEEL = 1
RIGHT_WHEEL = 2
wheel_speeds = {LEFT_WHEEL : 0 , RIGHT_WHEEL : 0}
wheel_goal_position = {LEFT_WHEEL : 0 , RIGHT_WHEEL : 0}


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
    
    dxl_io.disable_torque(wheel_ids) # I don't know what it means
    dxl_io.set_wheel_mode(wheel_ids)    
    
    print('Wheels initialized')



def position_origine():
    origine = dxl_io.get_present_position(wheel_ids)
    
def shutdown_wheels():
    dxl_io.disable_torque(wheel_ids)
    print('Wheels shut down')


def print_if_input(x, y,theta):

    if sys.stdin not in select.select([sys.stdin], [], [], 0)[0]:
        return
        
    
    line = sys.stdin.readline()   # we could do more than just shuting down by reading this line

    print('x :')
    print(x/10.)
    
    print('y : ')
    print(y/10.)
    
    print('theta : ')
    if theta > pi:
        print((theta - 2.*pi)*180./pi)
    else:
        print(theta*180./pi)


def boucle_mesure_distance():
    distance_parcourue=[0,0,0]
    dg=0.
    dd=0.
    rayon_roues=26
    L=133.9
    dteta=0.
    R=0.
    c=0.
    dxr=0.
    dyr=0.
    
    
    position2=list(dxl_io.get_present_position(wheel_ids))
    
    if(position2[0]<0):
        position2[0]+=360
        
    if(position2[1]<0):
        position2[1]+=360
        
        
    position2[0]=position2[0]*numpy.pi/180
    position2[1]=position2[1]*numpy.pi/180
        
    while(1):
        time.sleep(0.1)
        position1=position2
        position2=list(dxl_io.get_present_position(wheel_ids))

        if(position2[0]<0):
            position2[0]+=360
            
        if(position2[1]<0):
            position2[1]+=360            
            
        position2[0]=position2[0]*numpy.pi/180
        position2[1]=position2[1]*numpy.pi/180
        
        
        dg=((position2[0]-position1[0])%(2*numpy.pi))
        
        if dg > pi:
            dg -= 2. * pi
            
        dg *= rayon_roues
            
        #if abs(dg) < 0.05:
          #   dg = 0.            
            
        dd=((position2[1]-position1[1])%(2*numpy.pi))
        
        if dd > pi:
            dd -= 2. * pi
        
        dd *= -rayon_roues
        
      #  if abs(dd) < 0.05:
       #     dd = 0.  
        
        dteta=(dg-dd)/L
        if dteta==0:
            dxr=0.
            dyr=dg
        else:
            R=L/2+dd/dteta
            dxr = R * (1 - cos(dteta))
            dyr = R * sin(dteta)
            #c=sqrt(2*(R**2)*(1-cos(dteta)))
            #dxr=(c**2)/(2*R)
            #dyr=sqrt((c**2)-(c**4)/(4*(R**2)))
        distance_parcourue[2]-=dteta
        distance_parcourue[2]=distance_parcourue[2]%(2*numpy.pi)
        teta=distance_parcourue[2]
        distance_parcourue[0]+=dxr*sin(teta)+dyr*cos(teta)
        distance_parcourue[1]+=-dxr*cos(teta)+dyr*sin(teta)
        
        
        print_if_input(distance_parcourue[0], distance_parcourue[1], distance_parcourue[2]) 
        

init_wheels()
boucle_mesure_distance()
