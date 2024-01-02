from .entity import Entity
from .entity_attrs import EntityName


class Delivery(Entity):

    def __init__(self, receiver_name, date, comments):
        super().__init__()
        Entity.name = EntityName.DELIVERY
        self.receiver_name_ = receiver_name
        self.date_ = date
        self.comments_ = comments
        

    @property
    def _receiver_name(self):
        return self.receiver_name_

    @property
    def _date(self):
        return self.date_

    @property
    def _comments(self):
        return self.comments_
    
    @_receiver_name.setter
    def _receiver_name(self, receiver_name):
        self.receiver_name_ = receiver_name
    
    @_date.setter
    def _date(self, date):
        self.date_ = date

    @_comments.setter
    def _comments(self, comments):
        self.comments_ = comments

