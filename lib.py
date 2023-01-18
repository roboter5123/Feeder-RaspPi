import datetime
import json
import os
import time
import uuid

import schedule as schedule_module
from gpiozero import Motor

from Schedule import Schedule as Schedule
from Task import Task
from Weekday import Weekday

# Global variables
motor_forward_pin: int = 18
motor_backward_pin: int = 17
motor: Motor = Motor(motor_forward_pin, motor_backward_pin)
settings: dict[str, any]

current_time: datetime = datetime.datetime.now()
settings_path: str = "python/settings.json"
logs_path: str = "python/logs/log-"


def main() -> None:
    """
    Main loop for the device.
    Initiates the device and then checks once every minute for tasks that need doing.
    """

    while True:
        execute_current_tasks()
        time.sleep(60)


def execute_current_tasks():
    log("Checking for tasks to be done")
    schedule_module.run_pending()
    log("Current Tasks done")


"""================================================================================================================="""


def init() -> None:
    """
    Initializes the device by loading settings from the settings.json
    and setting up the schedule.
    """

    global current_time

    log("Initializing")
    loadSettings()
    saveSettings()
    init_schedule()


def loadSettings():
    """
    Loads the settings from settings.json parses it and saves it into the global settings variable.
    """

    global settings

    log("Loading settings")

    if os.path.exists(settings_path):

        json_settings = open(settings_path, "r")

        if os.path.getsize(settings_path) <= 0:
            settings = parse_settings()
            return

        settings = parse_settings(json.load(json_settings))
        json_settings.close()

    else:

        json_settings = open(settings_path, "w")
        json_settings.close()

    log("Settings loaded")


def parse_settings(new_settings=None):

    global settings
    if new_settings is None:
        new_settings = {}
    settings = {}

    if new_settings.get("uuid") is None:

        settings["uuid"] = str(uuid.uuid4())

    else:

        settings["uuid"] = new_settings.get("uuid")

    new_schedule: dict[str, any] = new_settings.get("schedule")

    if new_schedule is None:
        new_schedule = {"scheduleId": None, "name": None, "tasks": []}

    tasks = []

    for task in new_schedule.get("tasks"):

        weekday = Weekday(int(task.get("weekday")))
        time = task.get("time")
        amount = task.get("amount")
        taskId = task.get("taskId")
        task: Task = Task(weekday, time, amount, taskId)
        tasks.append(task)

    settings["schedule"] = Schedule(new_schedule["scheduleId"], new_schedule["name"], tasks)
    return settings


def saveSettings():
    if not os.path.exists(settings_path):
        log("Settings.json not found. Creating it.")
        _ = open(settings_path, "x")
        _.close()

    log("Dumping settings to settings.json")
    settings_file = open(settings_path, "w")
    json.dump(serializeSettings(), settings_file, indent=4)
    settings_file.close()
    log("Done dumping settings to settings.json")
    return


def serializeSettings():
    global settings
    serialize_settings = {}

    uuid = settings.get("uuid")

    if uuid == None:
        uuid = "null"

    serialize_settings["uuid"] = uuid

    schedule = settings.get("schedule")

    if schedule is None:
        schedule = Schedule()

    serialize_settings["schedule"] = schedule.to_json()
    return serialize_settings


def init_schedule():
    """
    Sets up the initial schedule with tasks from the settings.
    """

    global settings
    schedule: Schedule = settings.get("schedule")

    if schedule is None:
        settings["schedule"] = Schedule()
        schedule = settings.get("schedule")
        saveSettings()
        return

    tasks: list[Task] = schedule.tasks
    schedule_module.clear()

    for task in tasks:
        add_task_to_schedule_module(task)

    log("Done initialising schedule")


def add_task_to_schedule_module(task: Task):
    """
    Puts a new task on the current schedule.
    """

    log(f"Putting a new task on the schedule for {task.weekday}, {task.time} with amount = {task.amount}")

    attribute = None

    if task.weekday.value < 7:

        attribute = getattr(schedule_module.every(), task.weekday.name)

    elif task.weekday.value == 7:

        attribute = schedule_module.every().day

    attribute.at(task.time).do(dispense, amount=task.amount)
    log("Done adding task to schedule")


def add_task_to_schedule_object(task: Task):
    global settings

    schedule: Schedule = settings.get("schedule")
    schedule.add_task(task)
    init_schedule()
    saveSettings()


def remove_task_from_schedule_object(task: Task):
    global settings

    schedule: Schedule = settings.get("schedule")
    schedule.remove_task(task)
    init_schedule()
    saveSettings()


def dispense(dispense_seconds: int) -> None:
    """
    Turns the dispensing motor.
    """

    if dispense_seconds < 0 or not type(dispense_seconds) == int:
        raise ValueError("dispense_seconds must be a positive int or 0")

    log(f"Dispensing for {dispense_seconds} seconds")
    motor.forward()
    time.sleep(dispense_seconds)
    motor.stop()
    log(f"Done dispensing for {dispense_seconds} seconds")


"""================================================================================================================="""


def log(log_message: str):
    global logs_path

    if logs_path == "python/logs/log-":
        logs_path += f"{current_time.year}-{current_time.month}-{current_time.day}-{current_time.hour}-{current_time.minute}-{current_time.second}.txt"
        logs_file = open(logs_path, "x")
        logs_file.close()

    time = f"{current_time.day}-{current_time.month}-{current_time.hour}-{current_time.minute}-{current_time.second}:"
    log_file = open(logs_path, "a")
    log_file.write(f"{time} {log_message}\n")
    log_file.close()
