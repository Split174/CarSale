from models import City, ZipCode


class CityService:
    """
    Сервия для работы с городами
    """
    def __init__(self, session):
        self.session = session

    def get_cities(self):
        """
        Получить все города
        """
        cities_row = self.session.query(City).all()
        return [city.as_dict() for city in cities_row]

    def get_city_by_name(self, name):
        """
        Получить город по имени
        :param name: Имя
        :return: Город в формате Row
        """
        return self.session.query(City).filter(City.name == name).first()

    def get_city_by_id(self, id):
        """
        Получить город по id
        """
        return self.session.query(City).filter(City.id == id).first()

    def add_city(self, name):
        """
        Добавить город
        :param name: имя
        :return: Город в формате dict
        """
        new_city = City(name=name)
        self.session.add(new_city)
        self.session.commit()
        return new_city.as_dict()

    def get_zipcode(self, zip_code):
        """
        Получить зип-код
        """
        return self.session.query(ZipCode).filter(ZipCode.zip_code == zip_code).first()

    def add_zipcode(self, zip_code, city_id):
        """
        Добавить зипкод
        :param zip_code: зипкод
        :param city_id: id города
        """
        new_zipcode = ZipCode(zip_code=zip_code, city_id=city_id)
        self.session.add(new_zipcode)
        self.session.commit()
        return new_zipcode.as_dict()

