from models import Ad, Car, AdTag, Image, Color, CarColor
import time


class AdsService:
    """Сервис для работы с изображениями"""
    def __init__(self, session):
        self.session = session

    def get_all_ads(self):
        """
            Получить все объявления
        """
        ads = self.session.query(Ad, Car).join(Car, Ad.car_id == Car.id).all()
        return [{**ad.as_dict(), **car.as_dict()} for ad, car in ads]

    def get_all_users_ads(self, seller_id):
        """
            Получить все объявления пользователя
        :param seller_id: айди пользователя
        """
        ads = self.session.query(Ad, Car).join(Car, Ad.car_id == Car.id).filter(Ad.seller_id == seller_id).all()
        return [{**ad.as_dict(), **car.as_dict()} for ad, car in ads]

    def add_ad(self, title, seller_id, car_id):
        """
            Добавить объявление
        :param title: Тайтл объявления
        :param seller_id: айди пользователя-продавца
        :param car_id: айди автомобиля в системе
        :return: Type dict: новое объявление
        """
        new_ad = Ad(title=title, date=time.time(), seller_id=seller_id, car_id=car_id)
        self.session.add(new_ad)
        self.session.commit()
        return new_ad.as_dict()

    def get_ad_by_id(self, id):
        """
            Получить объявление по id
        """
        _ad = self.session.query(Ad, Car).join(Car, Ad.car_id == Car.id).filter(Ad.id == id).all()
        return [{**ad.as_dict(), **car.as_dict()} for ad, car in _ad][0]

    def delete_ad(self, id):
        self.session.query(Ad).filter(Ad.id == id).delete()
        self.session.commit()

    def is_ad_belong_user(self, user_id, ad_id):
        ad = self.session.query(Ad).filter(Ad.id == ad_id).first()
        return ad.as_dict()['seller_id'] == user_id

