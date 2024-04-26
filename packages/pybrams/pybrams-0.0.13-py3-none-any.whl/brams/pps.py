from __future__ import annotations
from .timestamps import Timestamps
import numpy as np
import datetime

class PPS:

    def __init__(self, index: np.ndarray, time: np.ndarray):

        self.index = index
        self.time = time
        self.timestamps = Timestamps(self.time)
        self.datetime = [datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=int(x)) for x in self.time]
        self.dt = np.diff(self.time)
        self.di = np.diff(self.index)

    
    def correct(self, file_type: str) -> None:
            
        if file_type == "RSP2":
 
            indices = self.index
            times = self.timestamps.get_us()
            p = np.polyfit(indices, times - times[0], 1)
            new_timestamps = times[0] + np.polyval(p, indices)

            self.timestamps.set_us([int(round(new_timestamp)) for new_timestamp in new_timestamps])
            self.time = self.timestamps.get_us()