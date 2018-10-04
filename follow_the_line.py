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
from RSL_vision import *





def cut_program_if_input():

    if sys.stdin not in select.select([sys.stdin], [], [], 0)[0]:
        return

    line = sys.stdin.readline()   # we could do more than just shuting down by reading this line
    shutdown_wheels()
    exit(0)



def update_movement(initial_speed, error, correction_coef = 5.):
    
    dv = correction_coef * error
    set_wheel_speed(LEFT_WHEEL, initial_speed + dv)
    set_wheel_speed(RIGHT_WHEEL, initial_speed - dv)

#def get_and_analyse_frame():
 #   return -0.25


def start_interaction_loop(initial_speed, frequence, duration, correction_coef):

    if frequence != 0.:
        period = 1./frequence

    loop_start = time.time()

    while (time.time() - loop_start < duration):

        start = time.time()
        cut_program_if_input()
        pict_analyse = get_and_analyse_frame()
        print(pict_analyse)
        update_movement(initial_speed, pict_analyse, correction_coef)
        stop = time.time()
        
        if frequence != 0.:
            time.sleep(max(0., period - (stop - start))) # send warning ?
            

    
def follow_the_line(initial_speed, acquisition_freq, duration, correction_coef):
    
    init_wheels()
    set_wheel_speeds(initial_speed)
    start_interaction_loop(initial_speed, acquisition_freq, duration, correction_coef)
    shutdown_wheels()



def main():
    
    argv = sys.argv
    
    if len(argv) != 5:
        print('Usage : initial_speed acquisition_freq duration correction_coef')
        exit(0)
        
    initial_speed = float(argv[1])
    acquisition_freq = float(argv[2])
    duration = float(argv[3])
    correction_coef = float(argv[4])
    follow_the_line(initial_speed, acquisition_freq, duration, correction_coef)


main()



