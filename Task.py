from Weekday import Weekday as Weekday
import json

class Task:
    
    weekday:Weekday
    time:str
    amount:int
    taskId:int
    
    def __init__(self, w:Weekday, t:str, a:int, ti:int) -> None:
        
        self.weekday = w
        self.time = t
        self.amount = a
        self.taskId = ti
    
    def same_task(task1, task2) -> bool:
        """
        Checks if two tasks are at the same time.
        """
        
        return task1.time == task2.time
    
    def toJson(self):
        
        return {"weekday": self.weekday.value, "time":self.time, "amount": self.amount, "taskId": self.taskId}
        
