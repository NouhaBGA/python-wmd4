import csv
import re
from flight import Flight
from airport import Airport
from typing import List


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


flight_map = FlightMap()
flight_map.import_airports("aeroports.csv")
flight_map.import_flights("flights.csv")

# Question D
# for airport in flight_map.airports():
#     print(f"{airport.name} {airport.code} {airport.lat} {airport.long}")

# for flight in flight_map.flights():
#     print(f"[{flight.src_code} {flight.dst_code} {flight.duration}]")

# Question E
# airport = flight_map.airport_find("CDG")
# if airport is not None:
#     print(f"Aéroport trouvé: {airport.name} {airport.code} {airport.lat} {airport.long}")
# else:
#     print("Aéroport non trouvé")


# Question F
print(flight_map.flight_exist("SYD", "NBO"))  # True
print(flight_map.flight_exist("MIA", "DFW"))  # False

# Question G
flights = flight_map.flights_where("ICN")

for my_flight in flights:
    print(f"Le vol de {my_flight[0]}-{my_flight[1]} dure {my_flight[2]}h ")

airports = flight_map.airports_from("CDG")
print(airports)






