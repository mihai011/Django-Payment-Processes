from http import HTTPStatus
import time
import random

class CheapGateway:
    

    def __init__(self, available=True):

        self.available = available
        self.name = "Cheap Gateway"

    def process(self, payment):
        
        status = HTTPStatus.OK

        if not self.available:
            status = HTTPStatus.TOO_MANY_REQUESTS
            return self.name, status

        if payment["amount"] >= 500:

            status = HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE

        if payment["amount"] < 500:
            # simulate processing of payment
            self.available = False
            time.sleep(random.randint(1,2))
            self.available = True
            status = HTTPStatus.OK

        return self.name, status

class ExpensiveGateway:


    def __init__(self, available=True):

        self.available = available
        self.name = "Expensive Gateway"

    def process(self, payment):

        status = HTTPStatus.OK

        if not self.available:
            status = HTTPStatus.TOO_MANY_REQUESTS
            return self.name, status

        if payment["amount"] >= 500:
            status = HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE
        
        if payment["amount"] <= 20:
            status = HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE

        if payment["amount"] >= 21 and payment["amount"] < 500:
            # simulate processing of payment
            self.available = False
            time.sleep(random.randint(1,2))
            self.available = True
            status = HTTPStatus.OK

        return self.name, status

class PremiumGateway:

   

    def __init__(self, available=True):

        self.available = available
        self.name = "Premium Gateway"

    def process(self, payment):

        status = HTTPStatus.OK

        if not self.available:
            status = HTTPStatus.TOO_MANY_REQUESTS
            return self.name, status

        if payment["amount"] < 500:
            status = HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE
        
        if payment["amount"] >= 500:
            # simulate processing of payment
            self.available = False
            time.sleep(random.randint(1,2))
            self.available = True
            status = HTTPStatus.OK

        return self.name, status