from django.test import TestCase, RequestFactory
from payments.forms import PaymentForm
from payments.views import PaymentView
from payments.gateways import CheapGateway, ExpensiveGateway, PremiumGateway
from payments.dispatcher import Dispatcher
from payments.models import Payment
from django.test import Client
from django.forms.models import model_to_dict

from http import HTTPStatus

import datetime
# Create your tests here.


class TestPaymentForm(TestCase):

    def test_valid_payment(self):
        
        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 12

        form = PaymentForm(data=data)

        self.assertTrue(form.is_valid())

        payment = form.save()

        self.assertEqual(payment.creditcardnumber, data["creditcardnumber"] )
        self.assertEqual(payment.cardholder, data["cardholder"])
        self.assertEqual(payment.expirationdate, data["expirationdate"])
        self.assertEqual(payment.securitycode, data["securitycode"], )
        self.assertEqual(payment.amount, data["amount"])
        
    def test_blank_payment(self):

        data = {}
        data["creditcardnumber"] = None
        data["cardholder"] = None
        data["expirationdate"] = None
        data["securitycode"] = None
        data["amount"] = None

        form = PaymentForm(data=data)
        
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
        'creditcardnumber': ['This field is required.'],
        'cardholder': ['This field is required.'],
        'expirationdate': ['This field is required.'],
        'amount':['This field is required.']
    })

    def test_invalid_fields_set_1(self):

        data = {}
        data["creditcardnumber"] = "40a"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2012,6,5)
        data["securitycode"] = "04"
        data["amount"] = -12

        form = PaymentForm(data=data)

        self.assertEqual(
            form.errors["creditcardnumber"], ['Card number must not contain letters!']
        )

        self.assertEqual(
            form.errors["expirationdate"], ['Expiry date must be set in the future!']
        )

        self.assertEqual(
            form.errors["securitycode"], ['Security code must be three numbers!']
        )
        
        self.assertEqual(
            form.errors["amount"], ['Amount must not be negative or zero!']
        )

    def test_invalid_fields_set_2(self):

        data = {}
        data["creditcardnumber"] = "403"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2022,6,5)
        data["securitycode"] = "04a"
        data["amount"] = 0

        form = PaymentForm(data=data)

        self.assertEqual(
            form.errors["creditcardnumber"], ['Invalid card number!']
        )

        self.assertEqual(
            form.errors["securitycode"], ['Security code must be all numbers!']
        )
        
        self.assertEqual(
            form.errors["amount"], ['Amount must not be negative or zero!']
        )





class TestViewClass(TestCase):

    client = Client()

    def test_get_payment(self):

        response = self.client.get('/payment/')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'payment.html')

    def test_post_valid_payment(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 12


        response = self.client.post('/payment/', data)

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_invalid_payment(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "04" # invalid security code
        data["amount"] = 12

        response = self.client.post('/payment/', data)


        self.assertEqual(response.status_code,HTTPStatus.BAD_REQUEST)

class TestGateways(TestCase):

    def test_available_cheap_gateway(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 12

        payment = PaymentForm(data)
        payment = payment.save()
        payment = model_to_dict(payment)

        gateway = CheapGateway()
        name, status = gateway.process(payment)

        self.assertEqual(status,HTTPStatus.OK)

        gateway = CheapGateway(False)
        name , status = gateway.process(payment)

        self.assertEqual(status,HTTPStatus.TOO_MANY_REQUESTS)

    def test_unavailable_cheap_gateway(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 12

        payment = PaymentForm(data)
        payment = payment.save()
        payment = model_to_dict(payment)

        gateway = CheapGateway(False)
        name, status = gateway.process(payment)

        self.assertEqual(status,HTTPStatus.TOO_MANY_REQUESTS)

    def test_too_much_cheap_gateway(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 1000

        payment = PaymentForm(data)
        payment = payment.save()
        payment = model_to_dict(payment)

        gateway = CheapGateway()
        name, status = gateway.process(payment)

        self.assertEqual(status,HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)



    def test_available_expensive_gateway(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 25

        payment = PaymentForm(data)
        payment = payment.save()
        gateway = ExpensiveGateway()
        payment = model_to_dict(payment)
        name, status = gateway.process(payment)

        self.assertEqual(status,HTTPStatus.OK)

    def test_unavailable_expensive_gateway(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 25

        payment = PaymentForm(data)
        payment = payment.save()
        gateway = ExpensiveGateway(False)
        payment = model_to_dict(payment)
        name , status = gateway.process(payment)

        self.assertEqual(status,HTTPStatus.TOO_MANY_REQUESTS)

    def test_too_much_expensive_gateway(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 1000

        payment = PaymentForm(data)
        payment = payment.save()
        gateway = ExpensiveGateway()
        payment = model_to_dict(payment)
        name, status = gateway.process(payment)

        self.assertEqual(status, HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)

    def test_too_little_expensive_gateway(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 10

        payment = PaymentForm(data)
        payment = payment.save()
        gateway = ExpensiveGateway()
        payment = model_to_dict(payment)
        name, status = gateway.process(payment)

        self.assertEqual(status,HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
        

    def test_avaialble_premium_gateways(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 600

        payment = PaymentForm(data)
        payment = payment.save()
        gateway = PremiumGateway()
        payment = model_to_dict(payment)
        name, status = gateway.process(payment)

        self.assertEqual(status,HTTPStatus.OK)

    def test_unavaialble_premium_gateways(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 600

        payment = PaymentForm(data)
        payment = payment.save()
        gateway = PremiumGateway(False)
        payment = model_to_dict(payment)
        name, status = gateway.process(payment)

        self.assertEqual(status,HTTPStatus.TOO_MANY_REQUESTS)

    def test_too_little_premium_gateways(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 100

        payment = PaymentForm(data)
        payment = payment.save()
        gateway = PremiumGateway()
        payment = model_to_dict(payment)
        name, status = gateway.process(payment)

        self.assertEqual(status,HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)

    

        

class TestDispatchFunction(TestCase):

    def test_functionality_case_cheap(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 10

        payment = PaymentForm(data)
        payment = payment.save()
        payment = model_to_dict(payment)

        Dispatcher.cheap_gateway = CheapGateway(True)

        name, status = Dispatcher.dispatch(payment)

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(name, Dispatcher.cheap_gateway.name)

    def test_functionality_case_expensive(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 50

        payment = PaymentForm(data)
        payment = payment.save()
        payment = model_to_dict(payment)

        name, status = Dispatcher.dispatch(payment)

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(name, Dispatcher.expensive_gateway.name)

    def test_functionality_case_premium(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 501

        payment = PaymentForm(data)
        payment = payment.save()
        payment = model_to_dict(payment)

        name, status = Dispatcher.dispatch(payment)

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(name, Dispatcher.premium_gateway.name)

    def test_functionality_case_unavailable_cheap(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 15

        payment = PaymentForm(data)
        payment = payment.save()
        payment = model_to_dict(payment)

        Dispatcher.cheap_gateway = CheapGateway(False)

        name, status = Dispatcher.dispatch(payment)

        self.assertEqual(status, HTTPStatus.TOO_MANY_REQUESTS)
        self.assertEqual(name, Dispatcher.cheap_gateway.name)

    def test_functionality_case_unavailable_expensive(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 100

        payment = PaymentForm(data)
        payment = payment.save()
        payment = model_to_dict(payment)

        Dispatcher.cheap_gateway = CheapGateway(True)
        Dispatcher.expensive_gateway = ExpensiveGateway(False)

        name, status = Dispatcher.dispatch(payment)

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(name, Dispatcher.cheap_gateway.name)

    def test_functionality_case_available_expensive(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 100

        payment = PaymentForm(data)
        payment = payment.save()
        payment = model_to_dict(payment)

        Dispatcher.cheap_gateway = CheapGateway(False)
        Dispatcher.expensive_gateway = ExpensiveGateway(True)

        name, status = Dispatcher.dispatch(payment)

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(name, Dispatcher.expensive_gateway.name)

    def test_functionality_case_available_premium(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 1000

        payment = PaymentForm(data)
        payment = payment.save()
        payment = model_to_dict(payment)

        Dispatcher.premium_gateway = PremiumGateway(True)

        name, status = Dispatcher.dispatch(payment)

        self.assertEqual(status, HTTPStatus.OK)
        self.assertEqual(name, Dispatcher.premium_gateway.name)

    def test_functionality_case_unavailable_premium(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 1000

        payment = PaymentForm(data)
        payment = payment.save()
        payment = model_to_dict(payment)

        Dispatcher.premium_gateway = PremiumGateway(False)

        name, status = Dispatcher.dispatch(payment)

        self.assertEqual(status, HTTPStatus.TOO_MANY_REQUESTS)
        self.assertEqual(name, Dispatcher.premium_gateway.name)