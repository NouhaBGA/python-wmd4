from flight import Flight
from airport import Airport
from typing import List


class FlightPathBroken(Exception):
    pass


class FlightPathDuplicate(Exception):
    pass


class FlightPath:
    def __init__(self, src_airport: Airport):
        self.l_flights = []
        self.l_airports = [src_airport]

    def add(self, dst_airport: Airport, via_flight: Flight):
        if self.l_airports[-1] != via_flight.src_airport:
            raise FlightPathBroken("Error: flight does not depart from last airport in the path")
        self.l_flights.append(via_flight)
        self.l_airports.append(dst_airport)

    def flights(self) -> List[Flight]:
        return self.l_flights

    def airports(self) -> List[Airport]:
        return self.l_airports

    def steps(self) -> int:
        return len(self.l_flights)

    def duration(self) -> float:
        return sum(flight.duration for flight in self.l_flights)

