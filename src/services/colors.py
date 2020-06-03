from models import Color


class ColorService:
    def __init__(self, session):
        self.session = session

    def get_colors(self):
        """
        Получить все цвета
        """
        colors_row = self.session.query(Color).all()
        return [color.as_dict() for color in colors_row]

    def get_color_by_name(self, name):
        """
        Получить цвет по имени
        """
        return self.session.query(Color).filter(Color.name == name).first()

    def add_color(self, name, hex):
        """
        Добавить новый цвет
        :param name: имя
        :param hex: цвет
        """
        new_color = Color(name=name, hex=hex)
        self.session.add(new_color)
        self.session.commit()
        return new_color.as_dict()


