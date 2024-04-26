from __future__ import annotations

try:

    from types import NoneType

except ImportError:

    NoneType = type(None)

from typing import Any, Dict, Optional, Union, List
import json_fix # type: ignore
import os
import json
from . import locations
from . import systems
from .wav import Wav
from .signal import Signal
from .api import request as api_request
from .http import get as get_request
from .cache import Cache
from .interval import parse

use_brams_archive = False
api_endpoint = "file.php"

class File:

    def __init__(self, year: int, month: int, day: int, hours: int, minutes: int, samplerate: float,
                 pps_count: int, duration: int, precise_start: int, precise_end: int, system_code: str,
                 location_code: str, location_url: str, system_url: str, wav_url: str, wav_name: str, png_url: str,
                 png_name: str, signal_properties: Optional[float] = None):

        self.year: int = year
        self.month: int = month
        self.day: int = day
        self.hours: int = hours
        self.minutes: int = minutes
        self.samplerate: float = samplerate
        self.pps_count: int = pps_count
        self.duration: int = duration
        self.precise_start: int = precise_start
        self.precise_end: int = precise_end
        self.system_code: str = system_code
        self.location_code: str = location_code
        self.location_url: str = location_url
        self.system_url: str = system_url
        self.wav_url: str = wav_url
        self.wav_name: str = wav_name
        self.png_url: str = png_url
        self.png_name: str = png_name
        self.signal_properties: Optional[dict[str, Any]] = signal_properties

        self.signal: Optional[Signal] = None

        self.corrected_wav_name = f"{self.wav_name[:-4]}.corrected.wav" if self.wav_name else None
        self.corrected_wav_content = None
        self.type = "AR" if "BEHUMA" in self.system_code else "RSP2" if self.samplerate == 6048 else "ICOM"
        self.wav: Optional[Wav] = None
    

    def __json__(self) -> Dict[str, Any]:

        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hours": self.hours,
            "minutes": self.minutes,
            "sample_rate": self.samplerate,
            "pps_count": self.pps_count,
            "duration": self.duration,
            "precise_start": self.precise_start,
            "precise_end": self.precise_end,
            "system_code": self.system_code,
            "location_code": self.location_code,
            "location_url": self.location_url,
            "system_url": self.system_url,
            "wav_url": self.wav_url,
            "wav_name": self.wav_name,
            "png_url": self.png_url,
            "png_name": self.png_name,
            "signal_properties": self.signal
        }
    
    def system(self) -> Union[systems.System, None]:

        return systems.get(self.system_code) 


    def location(self) -> Union[locations.Location, None]:

        return locations.get(self.location_code) 


    def load(self) -> None:

        wav_content = Cache.get(self.wav_name, False)

        if use_brams_archive:

            from . import archive

            wav_content = archive.get(self.system_code, self.year, self.month, self.day, self.hours, self.minutes)

        if not wav_content:

            while not wav_content or not len(wav_content):

                response = get_request(self.wav_url)
                wav_content = response.content

            Cache.cache(self.wav_name, wav_content, False)

        self.wav = Wav(wav_content)
        self.signal = Signal(self.wav, self.type, self.location())


    def save(self, path: str = ".") -> None:

        self.load() if not self.wav else None

        if self.wav:

            with open(os.path.join(path, self.wav_name), "wb") as file:

                file.write(self.wav.write())


    def process(self) -> None:

        self.corrected_wav_content = Cache.get(self.corrected_wav_name, False)
        
        if not self.corrected_wav_content:

            self.load() if not self.wav else None
            self.signal = Signal(self.wav, self.type, self.location())
            self.signal.process()

            self.corrected_wav_content = self.wav.write()
            Cache.cache(self.json_string(), json.dumps(self, indent=4))
            Cache.cache(self.corrected_wav_name, self.corrected_wav_content, False)

        else:
            
            self.wav = Wav(self.corrected_wav_content)
            self.signal = Signal(self.wav, self.type, self.location(), self.signal_properties)
            self.signal.compute_fft()


    def clean(self) -> None:

        self.process() if not self.corrected_wav_content else None
        self.signal.clean()


    def json_string(self) -> str:

        return f"{self.system_code}.{str(self.year).zfill(4)}{str(self.month).zfill(2)}{str(self.day).zfill(2)}_{str(self.hours).zfill(2)}{str(self.minutes).zfill(2)}"


    def __add__(self, other: File) -> Union[File, None]:

        if self.system_code == other.system_code and self.type == other.type:

            import numpy as np

            samplerate = np.mean([self.samplerate, other.samplerate])
            pps_count = self.pps_count + other.pps_count
            duration = self.duration + other.duration
            pps_index = np.concatenate((self.pps.index, other.pps.index))
            pps_time = np.concatenate((self.pps.time, other.pps.time))
            beacon_frequency = np.mean([self.beacon_frequency, other.beacon_frequency])
            file = File(-1, -1, -1, -1, -1, samplerate, pps_count, duration, self.precise_start, other.precise_end, self.system_code, self.location_code, self.location_url, self.system_url, None, None, None, None, beacon_frequency)
            file.pps = PPS(pps_index, pps_time)
            return file


            #WIP
            #file.signal = Signal(samplerate, np.concatenate((self.signal.data, other.signal.data)), file.beacon_frequency)

        return None


    def __eq__(self, other: File) -> bool:

        if isinstance(other, File):

            return (
                self.year == other.year and
                self.month == other.month and
                self.day == other.day and
                self.hours == other.hours and
                self.minutes == other.minutes and
                self.samplerate == other.samplerate and
                self.pps_count == other.pps_count and
                self.duration == other.duration and
                self.precise_start == other.precise_start and
                self.precise_end == other.precise_end and
                self.system_code == other.system_code and
                self.location_code == other.location_code and
                self.location_url == other.location_url and
                self.system_url == other.system_url and
                self.wav_url == other.wav_url and
                self.wav_name == other.wav_name and
                self.png_url == other.png_url and
                self.png_name == other.png_name and
                self.corrected_wav_name == other.corrected_wav_name and
                self.type == other.type and
                self.signal == other.signal
            )

        return False


def get(interval: str, system: Union[str, systems.System, List[Union[str, systems.System]], None] = None, load: bool = False, save: bool = False, process: bool = False, clean: bool = False) -> Union[File, List[File], Dict[str, File], Dict[str, List[File]], None]:

    def fetch_file(system_code, key: str):

        cached_file = Cache.get(key)

        if cached_file:
            file = File(*json.loads(cached_file).values())
            file.load() if load else None
            file.save() if save else None
            file.process() if process else None
            file.clean() if clean else None
            return file

        payload = {
            "start": start,
            "system_code": system_code
        }
        
        response = api_request(api_endpoint, payload)
        json_file = response.json()

        if json_file:

            file = File(*json_file.values())
            file.load() if load else None
            file.save() if save else None
            file.process() if process else None
            file.clean() if clean else None
            Cache.cache(key, json.dumps(file, indent=4))
            return file
    
        return None

    try:

        start, end = parse(interval)
    
    except TypeError:

        return None

    if isinstance(system, (str, systems.System)):

        # Handle a single system or system code
        system_code = system if isinstance(system, str) else system.system_code
    
    elif isinstance(system, (list, type(None))):
        
        if isinstance(system, list):

            if isinstance(system[0], systems.System):

                system_code = [s.system_code for s in system]
        
        elif isinstance(system, NoneType):

            system_code = [system.system_code for system in systems.all().values()]


    if end:

        files: Dict[str, List[File]] = {}

        payload = {
            "from": start,
            "to": end,
            "system_code[]": system_code
        }

        response = api_request(api_endpoint, payload)

        for file in response.json():

            system_code = file.get("system_code")
            file = File(*file.values())
            key = f"{system_code}.{str(file.year).zfill(4)}{str(file.month).zfill(2)}{str(file.day).zfill(2)}_{str(file.hours).zfill(2)}{str(file.minutes).zfill(2)}"

            cached_file = Cache.get(key)
        
            if cached_file:

                file = File(*json.loads(cached_file).values())
                file.load() if load else None
                file.save() if save else None
                file.process() if process else None
                file.clean() if clean else None
                files.setdefault(system_code, []).append(file)

            else:

                file.load() if load else None
                file.save() if save else None
                file.process() if process else None
                file.clean() if clean else None
                files.setdefault(system_code, []).append(file)
                Cache.cache(key, json.dumps(file, indent=4))

        if isinstance(system, (str, systems.System)):

            return files.get(system_code)
        
        else:

            return files

         
    else:

        if isinstance(system, (str, systems.System)):
            
            key = f"{system_code}.{str(start.year).zfill(4)}{str(start.month).zfill(2)}{str(start.day).zfill(2)}_{str(start.hour).zfill(2)}{str(start.minute).zfill(2)}"
            return fetch_file(system_code, key)

        elif isinstance(system, (list, type(None))):

            files: Dict[str, File] = {}

            if isinstance(system, list):

                if isinstance(system[0], systems.System):

                    system = [s.system_code for s in system]
            
            elif isinstance(system, NoneType):

                system = [system.system_code for system in systems.all().values()]
            
            # Iterate through system codes to fetch files
            for system_code in system.copy():
                
                key = f"{system_code}.{str(start.year).zfill(4)}{str(start.month).zfill(2)}{str(start.day).zfill(2)}_{str(start.hour).zfill(2)}{str(start.minute).zfill(2)}"
                file = fetch_file(system_code, key)

                if file:

                    files[system_code] = file
                    files[system_code].system = systems.get(system_code=system_code)
                    system.remove(system_code)
            
            if any(system):

                payload = {
                    "start": start,
                    "system_code[]": system
                }

                response = api_request(api_endpoint, payload)
                json_files = response.json()
                
                if json_files:
                    
                    if isinstance(json_files, dict):

                        json_files = [json_files]
                
                json_files = {file["system_code"]: file for file in json_files}
                
                for system_code, json_file in json_files.items():

                    key = f"{system_code}.{str(start.year).zfill(4)}{str(start.month).zfill(2)}{str(start.day).zfill(2)}_{str(start.hour).zfill(2)}{str(start.minute).zfill(2)}"
                    files[system_code] = File(*json_file.values())
                    files[system_code].load() if load else None
                    files[system_code].save() if save else None
                    files[system_code].process() if process else None
                    files[system_code].clean() if clean else None
                    files[system_code].system = systems.get(system_code=system_code)
                    Cache.cache(key, json.dumps(files[system_code], indent=4))
            
            return files if files else None