from dataclasses import dataclass
import datetime
from .coordinates import Coordinates
from .interval import parse
from .api import request as api_request
from typing import Dict, Any, List

api_endpoint = "adsb.php"
    
@dataclass
class Position:

    mode_s: str
    dt: datetime.datetime
    coordinates: Coordinates
    
    def __json__(self) -> Dict[str, Any]:

        return {
            "mode_s": self.mode_s,
            "dt": self.dt.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            "coordinates": self.coordinates
        }

def get(interval: str) -> Dict[str, List[Position]]:

    start, end = parse(interval)
    
    positions = {}
    current_page = 1
    
    while True:
        
        payload = {
            "from": start,
            "to": end,
            "page": str(current_page),
            "limit": 2500
        }
    
        response = api_request(api_endpoint, payload)
        json_response = response.json()
        
        for entry in json_response["data"]:
            
            mode_s = entry["mode_s"]
            year = entry["year"]
            month = entry["month"]
            day = entry["month"]
            hours = entry["hours"]
            minutes = entry["minutes"]
            seconds = entry["seconds"]
            microseconds = entry["microseconds"]
            latitude = entry["latitude"]
            longitude = entry["longitude"]
            altitude = entry["altitude"]
            
            dt = datetime.datetime(year=year, month=month, day=day, hour=hours, minute=minutes, second=seconds, microsecond=microseconds)
            coordinates = Coordinates.fromGeodetic(latitude, longitude, altitude)
            
            if mode_s not in positions:
                
                positions[mode_s] = []
                
            positions[mode_s].append(Position(mode_s, dt, coordinates))
        
        current_page = int(json_response["pagination"]["current_page"])
        total_pages = int(json_response["pagination"]["total_pages"])
        
        if current_page == total_pages:

            break       
        
        current_page += 1
        
    return positions
        
    


