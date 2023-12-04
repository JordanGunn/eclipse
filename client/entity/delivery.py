import entity_name
from .entity import Entity


class Delivery(Entity):

    def __init__(self):
        super().__init__()
        Entity.name = entity_name.DELIVERY

        self.receiver_name_ = ""
        self.time_stamp_ = ""
        self.comments_ = ""

    @property
    def receiver_name(self):
        return self.receiver_name_

    @receiver_name.setter
    def receiver_name(self, receiver_name):
        self.receiver_name_ = receiver_name

    @property
    def time_stamp(self):
        return self.time_stamp_

    @property
    def comments(self):
        return self.comments_

    @comments.setter
    def comments(self, comments):
        self.comments_ = comments

