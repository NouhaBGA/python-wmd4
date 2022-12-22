class Flight:
    def __init__(self, src_code: str, dst_code: str, duration: float):
        self.src_code = src_code
        self.dst_code = dst_code
        self.duration = duration

    def __new__(cls, src_code, dst_code, duration):
        # create a new object
        flight = super().__new__(cls)

        # initialize attributes
        flight.src_code = src_code
        flight.dst_code = dst_code
        flight.duration = duration

        # inject new attribute
        flight.full_info = f'{src_code} {dst_code} {duration}'
        return flight

    def __str__(self):
        return f'{self.src_code} {self.dst_code} {self.duration}'
