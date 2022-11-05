import time

from settings import * 


class Timer:
    def __init__(self) -> None:
        self.start_time = time.perf_counter()           # The timers start time 
        
    def elapsed_time(self) -> float:
        '''
        The elapsed time since we initialized this object. 
        
        Returns:
            The elapsed time between initializen and now. 
        '''
        
        # Return the elapsed time between intialization and now 
        return (time.perf_counter() - self.start_time)
    
    def custom_sleep(self, val) -> None:
        '''
        Sleeps a certain amount of time. 
        '''
        
        # Sleep val time in seconds 
        time.sleep(val)
