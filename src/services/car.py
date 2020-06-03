from models import Car


class CarService:
    """
    Сервис для работы с автомобилями
    """
    def __init__(self, session):
        self.session = session

    def add_car(self, car):
        """
        Добавить автомобиль
        """
        new_car = Car(make=car['make'], model=car['model'], mileage=car['mileage'], num_owners=car['mileage'],
                      reg_number=car['reg_number'])
        self.session.add(new_car)
        self.session.commit()
        return new_car.as_dict()