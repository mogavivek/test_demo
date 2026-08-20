class MachineSystem:

    def __init__(self, temperature, pressure, position):
        self.temperature = temperature
        self.pressure = pressure
        self.position = position

    def is_temperature_valid(self):
        return 0 <= self.temperature <= 80

    def is_pressure_valid(self):
        return 90 <= self.pressure <= 110

    def is_position_valid(self):
        return 0 <= self.position <= 100

    def system_status(self):
        return (
            self.is_temperature_valid()
            and self.is_pressure_valid()
            and self.is_position_valid()
        )