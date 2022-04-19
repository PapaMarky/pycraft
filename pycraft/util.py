import time

class ElapsedTime:
    '''
    Utility class for managing elapsed time of long running functions so that logging can show how long the function took to complete.

    Usage:
      * Create a ElapsedTime object at the beginning of a long running function,
      * At the end of the function, print output of elapsed_time_str() to show how long it took
      OR
      * Create a ElapsedTime object at the beginning of a function
      * Call reset() before calling a long running function
      * Call elapsed_time_str() after function returns to get elapsed time string
    '''
    def __init__(self):
        self.reset()

    def reset(self):
        '''
        Reset the elapsed time timer
        '''
        self._start_time = time.time()

    def get_elapsed_time(self) -> int:
        '''
        Get the current elapsed time in seconds as an integer.
        '''
        return time.time() - self._start_time

    def elapsed_time_str(self) -> str:
        '''
        Get the current elapsed time as a string: HH:MM:SS
        '''
        h = m = s = 0
        seconds = self.get_elapsed_time()
        if seconds > 3600.0:
            h = int(seconds / 3600.0)
            seconds = seconds - (h * 3600.0)
        if seconds > 60.0:
            m = int(seconds / 60.0)
            seconds = seconds - (m * 60.0)
        s = int(seconds)

        return f'{h:02}:{m:02}:{s:02}'
