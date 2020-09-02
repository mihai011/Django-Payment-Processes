from django.test import TestCase, RequestFactory
from payments.forms import PaymentForm
from payments.views import PaymentView
from django.test import Client

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

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'payment.html')

    def test_post_valid_payment(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "043"
        data["amount"] = 12


        response = self.client.post('/payment/', data)

        self.assertEqual(response.status_code,200)

    def test_post_invalid_payment(self):

        data = {}
        data["creditcardnumber"] = "4024007129931746"
        data["cardholder"] = "John Doe"
        data["expirationdate"] = datetime.date(2021,6,5)
        data["securitycode"] = "04" # invalid security code
        data["amount"] = 12

        response = self.client.post('/payment/', data)


        self.assertEqual(response.status_code,400)

