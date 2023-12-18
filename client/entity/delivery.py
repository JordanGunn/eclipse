from .entity import Entity
from .entity_attrs import EntityName


class Delivery(Entity):

    def __init__(self, receiver_name_, date_, comments_, validation = False):
        super().__init__()
        Entity.name = EntityName.DELIVERY

        if validation == False:
            self._receiver_name = receiver_name_
            self._date = date_
            self._comments = comments_
        else:
            self._receiver_name = receiver_name_
            self._date = date_

    @property
    def _receiver_name(self):
        return self.receiver_name

    @property
    def _date(self):
        return self.date

    @property
    def _comments(self):
        return self.comments
    
    @_receiver_name.setter
    def _receiver_name(self, receiver_name):
        self.receiver_name = receiver_name
    
    @_date.setter
    def _date(self, date):
        self.date = date

    @_comments.setter
    def _comments(self, comments):
        self.comments = comments

