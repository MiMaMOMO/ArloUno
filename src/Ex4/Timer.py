import time


class Timer:
    def __init__(self) -> None:
        self.start_time = time.perf_counter()
        
    def elapsed_time(self) -> float:
        '''
        The elapsed time since we initialized this object. 
        
        Returns:
            The elapsed time between initializen and now. 
        '''
        return (time.perf_counter() - self.start_time)
