from .celery import app
from http import HTTPStatus


from payments.gateways import CheapGateway, ExpensiveGateway, PremiumGateway



class Dispatcher():

    cheap_gateway = CheapGateway(True)
    expensive_gateway = ExpensiveGateway(True)
    premium_gateway = PremiumGateway(True)

    @staticmethod
    @app.task(bind=True, ignore_result=True)
    def dispatch(self, payment):

        try:
            self.update_state(state="STARTED", meta={"resolver":"Not decided!"})
        except:
            pass

        resolver, status = None, HTTPStatus.UNAVAILABLE_FOR_LEGAL_REASONS

        if payment["amount"] <= 20:

            resolver, status = Dispatcher.cheap_gateway.process(payment)
        

        if payment["amount"] >= 21 and payment["amount"] <= 500:

            resolver, status = Dispatcher.expensive_gateway.process(payment)

            if status != HTTPStatus.OK:
                
                resolver, status = Dispatcher.cheap_gateway.process(payment)

    
        if payment["amount"] >= 501:

            for _ in range(3):

                resolver, status = Dispatcher.premium_gateway.process(payment)

                if status == HTTPStatus.OK:
                    break
        try:
            if status == HTTPStatus.OK :
                self.update_state(state="SUCCESS", meta={"resolver":resolver})
            else:
                self.update_state(state="FAILURE", meta={"resolver":resolver})
        except:
            pass

        
        return resolver, status


        
