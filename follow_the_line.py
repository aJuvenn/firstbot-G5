# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 10:27:34 2018

@author: juven
"""


import itertools
import numpy
import time
import sys
import select


from pypot_wheel_speed import *


def cut_program_if_input():

    if sys.stdin not in select.select([sys.stdin], [], [], 0)[0]:
        return

    line = sys.stdin.readline()   # we could do more than just shuting down by reading this line
    shutdown_wheels()
    exit(0)


def get_and_analyse_frame(): #stub : TODO
    return 0.
    

def update_movement(d_theta, correction_coef = 0.01):
    
    dv = correction_coef * d_theta
    
    increase_wheel_speed(LEFT_WHEEL, dv)
    increase_wheel_speed(RIGHT_WHEEL, -dv)



def start_interaction_loop(frequence, duration):

    if frequence != 0.:
        period = 1./frequence

    loop_start = time.time()

    while (time.time() - loop_start < duration):

        start = time.time()
        cut_program_if_input()
        pict_analyse = get_and_analyse_frame()
        update_movement(pict_analyse)
        stop = time.time()
        
        if frequence != 0.:
            time.sleep(max(0., period - (stop - start))) # send warning ?
            

    
def follow_the_line(initial_speed, acquisition_freq, duration):
    
    init_wheels()
    set_wheel_speeds(initial_speed)
    start_interaction_loop(acquisition_freq, duration)
    shutdown_wheels()



#follow_the_line(10., 10., 100.)






