from models import Account, Seller
import sqlite3


class UserService:
    """
    Сервис для работы с пользователями и продавцами
    """
    def __init__(self, session):
        self.session = session

    def add_account(self, user, password_hash):
        """
        Добавить пользователя
        :param Dict user: пользователь
        :param password_hash: пароль
        """
        new_acc = Account(email=user['email'], password=password_hash, first_name=user['first_name'],
                          last_name=user['last_name'])
        self.session.add(new_acc)
        self.session.commit()
        return new_acc.as_dict()

    def is_user_a_seller(self, account_id):
        """
        Является ли пользователь продавцом
        """
        if self.session.query(Seller).filter(Seller.account_id == account_id).first() is None:
            return False
        return True

    def add_seller(self, seller, user_id):
        """
        Добавить продавца
        :return:
        """
        new_seller = Seller(zip_code=seller['zip_code'], street=seller['street'], home=seller['home'],
                            phone=seller['phone'], account_id=user_id)
        self.session.add(new_seller)
        self.session.commit()
        return new_seller.as_dict()

    def get_user(self, user_id): # TODO плохой метод, надо бы разделить пользователей от продавцов
        """
        Получить пользователя-продавца
        """
        user = self.session.query(Account).filter(Account.id == user_id).first()
        seller = self.session.query(Seller).filter(Seller.account_id == user_id).first()
        if seller is not None:
            seller_dict = seller.as_dict()
            seller_dict.pop('account_id')
            return {**user.as_dict(), **{'is_seller': True}, **seller_dict}
        return {**user.as_dict(), **{'is_seller': False}}

    def get_user_by_email(self, email):
        """
        Получить пользователя по email
        """
        return self.session.query(Account).filter(Account.email == email).first()
