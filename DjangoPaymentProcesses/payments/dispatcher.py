from celery import shared_task
from http import HTTPStatus

from payments.gateways import CheapGateway, ExpensiveGateway, PremiumGateway

class Dispatcher():

    cheap_gateway = CheapGateway(True)
    expensive_gateway = ExpensiveGateway(True)
    premium_gateway = PremiumGateway(True)

    @staticmethod
    @shared_task
    def dispatch(payment):

        if payment["amount"] < 20:
            result = Dispatcher.cheap_gateway.process(payment)
        

        if payment["amount"] > 20 and payment["amount"] < 500:

            result = Dispatcher.expensive_gateway.process(payment)

            if result == HTTPStatus.TOO_MANY_REQUESTS:
                
                result = Dispatcher.cheap_gateway.process(payment)


        if payment["amount"] > 500:

            for _ in range(3):
                result = Dispatcher.premium_gateway.process(payment)
                if result == HTTPStatus.OK:
                    break

        return result


        
