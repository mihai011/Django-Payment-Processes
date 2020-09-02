from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import TemplateView

from payments.forms import PaymentForm

# Create your views here.


class PaymentView(TemplateView):
    
    form_class = PaymentForm
    template_name = "payment.html"
    
    def get(self, request):

        form = self.form_class()

        return render(request, self.template_name, {'form':form}, status=200)

    def post(self, request):
        
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            
            # send amount to Dispatcher

            form = self.form_class()
            return render(request, self.template_name, {'form':form}, status=200)
        else:
            return render(request, self.template_name, {'form':form}, status=400)
    