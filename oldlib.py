from gpiozero import Motor
from Weekday import Weekday
import json
import time
from Task import Task
import os
import schedule as schedulemodule
from Schedule import Schedule as Schedule
import threading
import datetime
import re
from uuid6 import uuid7

#Type aliases
Json_task = dict[str, any]
Json_day = list[Json_task]
Json_sched = dict[int,Json_day]

#Global variables
motor_forward_pin: int = 18
motor_backward_pin: int = 17
motor: Motor = Motor(motor_forward_pin, motor_backward_pin)
sched: Schedule = Schedule()
settings: dict[str,any] = {"schedule" : sched}
current_time :datetime = datetime.datetime.now()
settings_path: str = "python/settings.json"
logs_path: str = "python/logs/log-"
      
    


    """
    Puts a new task on the current schedule.
    """

    
    
    #Equivilant to schedule.every()."insert day"..at(task.time).do(dispense,dispense_seconds = task.dispense_seconds)
    dispense_seconds: int = task.dispense_seconds
    time: str = task.time
    day_name: str = day.name
    getattr(schedulemodule.every(), day.name).at(task.time).do(dispense,dispense_seconds = task.dispense_seconds)

    
    global logs_path
    
    time = f"{current_time.day}-{current_time.month}-{current_time.hour}-{current_time.minute}-{current_time.second}:"
    log_file = open(logs_path, "a")
    log_file.write(f"{time} {log_message}\n")
    log_file.close()