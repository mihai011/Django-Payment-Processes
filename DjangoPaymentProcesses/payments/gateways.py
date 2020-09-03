from http import HTTPStatus
import time
import random

class CheapGateway:


    def __init__(self, available=True):

        self.available = available

    def process(self, payment):

        if not self.available:
            return HTTPStatus.TOO_MANY_REQUESTS

        if payment["amount"] >= 500:
            return HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE

        if payment["amount"] < 20 or payment["amount"] < 500:
            # simulate processing of payment
            self.available = False
            time.sleep(random.randint(20,50))
            self.available = True
            return HTTPStatus.OK




class ExpensiveGateway:

    
    def __init__(self, available=True):

        self.available = available

    def process(self, payment):

        if not self.available:
            return HTTPStatus.TOO_MANY_REQUESTS

        if payment["amount"] >= 500:
            return HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE
        
        if payment["amount"] <= 20:
            return HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE

        if payment["amount"] >= 21 or payment["amount"] < 500:
            # simulate processing of payment
            self.available = False
            time.sleep(random.randint(1,5))
            self.available = True
            return HTTPStatus.OK




class PremiumGateway:

    def __init__(self, available=True):

        self.available = available

    def process(self, payment):

        if not self.available:
            return HTTPStatus.TOO_MANY_REQUESTS

        if payment["amount"] <= 500:
            return HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE
        
        if payment["amount"] > 500:
            # simulate processing of payment
            self.available = False
            time.sleep(random.randint(20,50))
            self.available = True
            return HTTPStatus.OK