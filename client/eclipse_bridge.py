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

        deliveryEntity = Delivery(self.receiver_name, self.date, self.comments)
        if self.checkDuplicates(deliveryEntity) == True:
            raise ValueError('Delivery record already exists!')
        
        ereq = EclipseRequest("POST", deliveryEntity)
        ereq.send()

    def checkDuplicates(self, entity):
        
        ereq = EclipseRequest("GET", entity)
        res = ereq.send()

        tempDict = {
                'receiver_name': self.receiver_name, 
                'date': self.date
                    }
        for resDict in res:
            resFiltered = {k:v for k,v in resDict.items() if k not in 'comments'}

            if tempDict == resFiltered:
                return True
        
    