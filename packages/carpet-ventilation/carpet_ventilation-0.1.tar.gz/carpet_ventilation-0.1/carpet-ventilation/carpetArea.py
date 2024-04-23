class House:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

    def calculate_carpet_area(self):
        return self.length * self.width

    def calculate_airflow_ventilation(self):
        return self.length * self.width * self.height
