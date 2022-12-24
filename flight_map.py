import csv
import re
from flight import Flight
from airport import Airport
from typing import List, Tuple, Dict
from flight_path import FlightPath
from collections import deque


class FlightMap:

    def __init__(self):
        self.airport_list = {}
        self.flight_list = {}

    def import_flights(self, csv_file: str) -> None:
        with open(csv_file, 'r') as csvfile:
            flight_data = csv.reader(csvfile)

            for row in flight_data:
                src_code, dst_code, duration = row
                src_code = src_code.strip('" "')
                dst_code = dst_code.strip('" "')
                flight = Flight(src_code, dst_code, float(duration))
                # self.flight_list[dst_code] = flight
                self.flight_list[(src_code, dst_code, float(duration))] = flight
                # self.flight_list.append(flight)
                # print(flight)

    def import_airports(self, csv_file: str) -> None:

        with open(csv_file, 'r') as f:
            data = csv.reader(f)

            for row in data:
                name, code, lat, long = row
                code = code.strip('" "')
                lat_float = float(re.search(r'\d+(\.\d+)?', lat).group())
                long_float = float(re.search(r'\d+(\.\d+)?', long).group())
                # lat_float = float(lat)
                # long_float = float(long)
                airport = Airport(name, code, lat_float, long_float)
                self.airport_list[code] = airport
                # print(airport)

    def airports(self) -> List[Airport]:
        return self.airport_list.values()

    def flights(self) -> List[Flight]:
        return self.flight_list.values()

    def airport_find(self, airport_code: str) -> Airport:
        return self.airport_list.get(airport_code)

    def flight_exist(self, src_airport_code: str, dst_airport_code: str) -> bool:
        for i in self.flight_list:
            # print(i)
            # print(i[1])
            if i[0] == src_airport_code and i[1] == dst_airport_code:
                return True
        return False
        # return (src_airport_code, dst_airport_code) in self.flight_list

    def flights_where(self, airport_code: str) -> list[Flight]:
        # Retournez la liste des vols directs qui concernent l'aéroport airport_code
        flight_s = []
        for f in self.flight_list:
            if f[0] == airport_code or f[1] == airport_code:
                flight_s.append(f)
        print(flight_s)
        return flight_s
        # return [flight_s.append(f) for f in self.flight_list if f[0] == airport_code or f[1] == airport_code]

    def airports_from(self, airport_code: str) -> list[Airport]:
        # Retournez la liste des aéroports destination des vols en partance de l'aéroport airport_code
        destinations = set()
        for f in self.flight_list:
            if f[0] == airport_code:
                destinations.add(f[1])
        return destinations

    def paths(self, src_airport_code: str, dst_airport_code: str) -> List[FlightPath]:
        paths = []

        src_airport = self.airport_list.get(src_airport_code)
        dst_airport = self.airport_list.get(dst_airport_code)

        airports_not_visited = set(self.airport_list.values())
        airports_future = deque([src_airport])
        airports_visited = set()

        while airports_future:
            airport = airports_future.popleft()
            airports_not_visited.remove(airport)
            airports_visited.add(airport)

            if airport == dst_airport:
                paths.append(FlightPath(src_airport))
            else:
                for nearby_airport in self._find_nearby_airports(airport):
                    if nearby_airport not in airports_visited:
                        airports_future.append(nearby_airport)
                        airports_not_visited.remove(nearby_airport)
                        airports_visited.add(nearby_airport)

        return paths

    def _find_nearby_airports(self, airport: Airport) -> List[Airport]:
        nearby_airports = []
        for code, airport in self.airport_list.items():
            if (airport.code, code) in self.flight_list:
                nearby_airports.append(airport)
        return nearby_airports

    def paths_shortest_length(self, src_airport_code: str, dst_airport_code: str) -> List[FlightPath]:
        paths = []

        src_airport = self.airport_list.get(src_airport_code)
        dst_airport = self.airport_list.get(dst_airport_code)

        # Initialise la liste des aéroports à visiter et la distance de chaque aéroport
        airports_future = deque([(src_airport, 0)])
        distances = {src_airport: 0}
        # Initialise la liste des aéroports visités et non visités
        airports_visited = set()
        airports_not_visited = set(self.airport_list.values())

        # Tant qu'il reste des aéroports à visiter
        while airports_future:
            # Récupère l'aéroport et sa distance
            airport, distance = airports_future.popleft()
            # Si l'aéroport courant est la destination, ajoute un nouveau chemin à la liste et continue la recherche
            if airport == dst_airport:
                path = self.construct_path(src_airport, dst_airport, distances)
                paths.append(path)
            # Sinon, récupère les aéroports accessibles depuis l'aéroport courant
            next_airports = self.get_next_airports(airport, distance, dst_airport)
            # Met à jour la liste des aéroports à visiter et la distance de chaque aéroport
            for next_airport, next_distance in next_airports:
                if next_airport not in airports_visited:
                    airports_future.append((next_airport, next_distance))
                    distances[next_airport] = next_distance
            # Marque l'aéroport courant comme visité
            airports_not_visited.remove(airport)
            airports_visited.add(airport)

        # Garde seulement les chemins de longueur minimale
        if paths:
            min_length = min(len(path) for path in paths)
            paths = [path for path in paths if len(path) == min_length]
        else:
            paths = []

        # Retourne la liste des chemins trouvés
        return paths

        # Retourne la liste des chemins trouvés
        return paths

    def get_next_airports(self, airport: Airport, distance: int, dst_airport: Airport) -> List[Tuple[Airport, int]]:
        next_airports = []
        for code, next_airport in self.airport_list.items():
            if (airport.code, code) in self.flight_list:
                next_airports.append((next_airport, distance + 1))
        return next_airports

    def construct_path(self, src_airport: Airport, dst_airport: Airport, distances: Dict[Airport, int]) -> FlightPath:
        path = [dst_airport]
        current_airport = dst_airport
        while current_airport != src_airport:
            for code, airport in self.airport_list.items():
                if (code, current_airport.code) in self.flight_list and distances[airport] == distances[current_airport] \
                        - 1:
                    path.insert(0, airport)
                    current_airport = airport
                    break
        return FlightPath(path)


flight_map = FlightMap()
flight_map.import_airports("aeroports.csv")
flight_map.import_flights("flights.csv")

# Question D
for airport in flight_map.airports():
    print(f"{airport.name} {airport.code} {airport.lat} {airport.long}")

for flight in flight_map.flights():
    print(f"[{flight.src_code} {flight.dst_code} {flight.duration}]")

# Question E
airport = flight_map.airport_find("CDG")
if airport is not None:
    print(f"Aéroport trouvé: {airport.name} {airport.code} {airport.lat} {airport.long}")
else:
    print("Aéroport non trouvé")


# Question F
print(flight_map.flight_exist("SYD", "NBO"))  # True
print(flight_map.flight_exist("MIA", "DFW"))  # False

# Question G
flights = flight_map.flights_where("ICN")

for my_flight in flights:
    print(f"Le vol de {my_flight[0]}-{my_flight[1]} dure {my_flight[2]}h ")

airports = flight_map.airports_from("CDG")
print(airports)

print(flight_map.paths("BNE", "BNO"))
print(flight_map.paths_shortest_length("BNE", "BNO"))






