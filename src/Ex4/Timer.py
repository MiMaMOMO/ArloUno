import time

from settings import * 


class Timer:
    def __init__(self) -> None:
        self.start_time = time.perf_counter() - TIME_ERROR
        
    def elapsed_time(self) -> float:
        '''
        The elapsed time since we initialized this object. 
        
        Returns:
            The elapsed time between initializen and now. 
        '''
        return (time.perf_counter() - self.start_time)
    
    def sleep(self, val) -> None:
        '''
        Sleeps a certain amount of time. 
        '''
        
        # Sleep val time in seconds 
        time.sleep(val)
