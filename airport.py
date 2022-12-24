class Airport:
    def __init__(self, name: str, code: str, lat: float, long: float):
        self.name = name
        self.code = code
        self.lat = lat
        self.long = long

    def __str__(self):
        return f'{self.name} {self.code} {self.lat} {self.long}'

    def __new__(cls, name, code, lat, long):
        # create a new object
        airport = super().__new__(cls)

        # initialize attributes
        airport.name = name
        airport.code = code
        airport.lat = lat
        airport.long = long

        # inject new attribute
        airport.full_info = f'{name} {code} {lat} {long}'
        return airport


# airport = Airport('LA', 'LAA')
# print(airport.name)
