from entity import Delivery
from copy import EclipseCopy
from eclipse_request import EclipseRequest


class delivery:

    def __init__(self, receiver_name="", date="", comments=""):
        self.receiver_name = receiver_name
        self.date = date
        self.comments = comments

        self.addDelivery()

    def addDelivery(self):

        if self.checkDuplicates() == True:
            raise ValueError('Delivery record already exists!')
        
        deliveryEntity = Delivery(self.receiver_name, self.date, self.comments)
        ereq = EclipseRequest("POST", deliveryEntity, url_params=None)
        res = ereq.send()

    def checkDuplicates(self):
        partialEntity = Delivery(self.receiver_name, self.date, self.comments, True)
        ereq = EclipseRequest("GET", partialEntity, url_params=None)
        res = ereq.send()

        if res != []:
            return True
        
    