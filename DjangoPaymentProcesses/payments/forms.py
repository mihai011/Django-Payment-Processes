from django import forms
from payments.models import Payment
from django.forms import ModelForm

class PaymentForm(ModelForm):
    
    class Meta:

        model = Payment
        fields = ['creditcardnumber', 'cardholder', 'expirationdate', 'securitycode', 'amount']

    def __init__(self, *args, **kwargs):

        super(PaymentForm, self).__init__(*args, **kwargs)

        self.fields['securitycode'].required = False

        self.fields["creditcardnumber"].label = "Card Number"
        self.fields["cardholder"].label = "Card Holder"
        self.fields["expirationdate"].label = "Expiration date card"
        self.fields["securitycode"].label = "Security Code"
        self.fields["amount"].label = "Amount"

